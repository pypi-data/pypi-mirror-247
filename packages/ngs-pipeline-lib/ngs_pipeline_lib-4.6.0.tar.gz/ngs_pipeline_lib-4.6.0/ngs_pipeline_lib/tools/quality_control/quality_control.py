from enum import Enum
from json import loads
from typing import Any

from pydantic import BaseModel, Field

from ngs_pipeline_lib.base.inputs import OrganismInput
from ngs_pipeline_lib.base.report import QCReport, QCReportIssue
from ngs_pipeline_lib.tools.quality_control.rules import Rule


class QCResult(str, Enum):
    PASS = "PASS"
    WARN = "WARN"
    FAIL = "FAIL"
    NA = "NA"


class Check(BaseModel):
    name: str
    section_name: str
    organism_name: str
    description: str
    FAIL: list[Rule] = Field(default_factory=list)
    WARN: list[Rule] = Field(default_factory=list)

    def apply(self, observations: dict[str, Any]) -> QCReportIssue | None:
        for output, rules in {
            QCResult.FAIL: self.FAIL,
            QCResult.WARN: self.WARN,
        }.items():
            results = [rule.apply(observations) for rule in rules]
            if results and all(results):
                # dict() is not recursive, json() is + it supports encoders
                rules_as_dict = [loads(rule.json()) for rule in rules]
                return QCReportIssue(
                    sectionName=self.section_name,
                    organismName=self.organism_name,
                    name=self.name,
                    status=output,
                    rules=rules_as_dict,
                    description=self.description,
                )


class QualityControl:

    """
    This class is only in charge of creating the Checks
    The Algorithm is in charge of creating the object that will contain the values
    """

    def __init__(
        self, qc_dict: dict, report: QCReport, organism: OrganismInput | None = None
    ) -> None:
        self.qc_dict = qc_dict
        self.organism = organism
        self.report = report

    def _get_checks(self, section_name: str) -> list[Check]:
        checks: list[Check] = []

        try:
            section = self.qc_dict[section_name]
        except KeyError:
            self.report.result = QCResult.FAIL
            issue = QCReportIssue(
                sectionName=section_name,
                organismName="",
                name="",
                status=QCResult.FAIL,
                rules=[],
                description="The requested section does not exist",
            )
            self.report.issues.append(issue)
            return checks

        # full organism name
        if self.organism and self.organism.full_name in section:
            organism_name = self.organism.full_name
        # fallback to genus only
        elif self.organism and self.organism.genus in section:
            organism_name = self.organism.genus
        # fallback to default
        elif "DEFAULT" in section:
            organism_name = "DEFAULT"
        # undefined DEFAULT in the references
        else:
            self.report.result = QCResult.FAIL
            issue = QCReportIssue(
                sectionName=section_name,
                organismName="DEFAULT",
                name="",
                status=QCResult.FAIL,
                rules=[],
                description="The requested organism does not exist",
            )
            self.report.issues.append(issue)
            return checks

        definitions = section[organism_name]
        for definition in definitions:
            checks.append(
                Check(
                    section_name=section_name,
                    organism_name=organism_name,
                    **definition,
                )
            )

        return checks

    def apply(
        self,
        section_name: str,
        observations: dict[str, Any] = {},
    ) -> None:
        checks = self._get_checks(section_name)
        # if something wrong happened during the previous step
        if self.report.result == QCResult.FAIL:
            return
        for check in checks:
            issue = check.apply(observations)
            if issue:
                if (self.report.result == QCResult.PASS) or (
                    issue.status == QCResult.FAIL
                ):
                    self.report.result = issue.status
                self.report.issues.append(issue)
