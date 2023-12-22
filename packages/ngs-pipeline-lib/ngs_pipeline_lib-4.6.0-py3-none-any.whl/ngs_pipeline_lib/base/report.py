from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from math import isnan
from typing import Any

from ngs_pipeline_lib.tools.tools import to_camel_case


class ExecutionStatus(str, Enum):
    SUCCESS = "success"
    ERROR = "error"


@dataclass
class ExecutionReport:
    start: datetime
    stop: datetime | None = None
    status: ExecutionStatus = ExecutionStatus.SUCCESS
    duration: int = field(init=False)

    @property
    def duration(self) -> int:
        if not self.stop:
            return 0
        else:
            delta = self.stop - self.start
            return int(delta.total_seconds() * 1000)

    @duration.setter
    def duration(self, value: int) -> None:
        """
        This setter does nothing as duration must be calculated
        """


@dataclass
class Report:
    name: str
    version: str
    inputs: dict[str, Any]
    kbs: dict[str, Any]
    outputs: list[str]
    execution: ExecutionReport | None = None


@dataclass
class QCReportIssue:
    sectionName: str
    organismName: str
    name: str
    status: str
    rules: list[dict[str, Any]]
    description: str


@dataclass
class QCReport:
    result: str = "PASS"
    metrics: dict[str, str | int | float | bool | None] = field(default_factory=dict)
    issues: list[QCReportIssue] = field(default_factory=list)

    def add_metrics(self, metrics: dict[str, str | int | float | bool]):
        for name, value in metrics.items():
            self.add_metric(metric_name=name, metric_value=value)

    def add_metric(self, metric_name: str, metric_value: str | int | float | bool):
        formatted_metric_name = to_camel_case(metric_name)

        if formatted_metric_name in self.metrics:
            raise ValueError(
                f"The metric {formatted_metric_name} is already set in the report metrics with the value {self.metrics[formatted_metric_name]}."
            )

        try:
            if isnan(metric_value):
                metric_value = None
        except TypeError:
            ...
        self.metrics[formatted_metric_name] = metric_value
