import importlib
import importlib.util
from abc import ABCMeta, abstractmethod
from dataclasses import asdict
from datetime import datetime, timezone
from json import loads
from logging import getLogger
from typing import Generic, TypeVar, final

from ngs_pipeline_lib.base.inputs import BaseInputs
from ngs_pipeline_lib.base.outputs import BaseOutputs
from ngs_pipeline_lib.base.report import (
    ExecutionReport,
    ExecutionStatus,
    QCReport,
    Report,
)
from ngs_pipeline_lib.tools.quality_control import QCResult

InputType = TypeVar("InputType", bound=BaseInputs)
OutputType = TypeVar("OutputType", bound=BaseOutputs)

UNKNOWN_VERSION = "unknown"


class Algorithm(Generic[InputType, OutputType], metaclass=ABCMeta):
    def __init__(self, inputs: InputType):
        self.logger = getLogger("main").getChild(f"{self.name}@{self.version}")

        self.inputs = inputs
        self.outputs = self.outputs_class()
        self.report = Report(
            name=self.name,
            version=self.version,
            inputs=loads(inputs.inputs_as_string()),
            kbs=loads(inputs.kbs_as_string()),
            outputs=self.outputs.files_path,
        )
        self.qc_report = QCReport()
        self.result = dict()

    @property
    def name(self) -> str:
        return self.__class__.__name__

    @property
    def version(self) -> str:
        if importlib.util.find_spec("src"):
            version = importlib.import_module("src").__version__
        else:
            version = UNKNOWN_VERSION

        return version

    @property
    @abstractmethod
    def outputs_class(self) -> type[OutputType]:
        """
        Define the class used for Output
        It must be a subclass of BaseOutputs
        """

    @abstractmethod
    def execute_implementation(self):
        """
        Define the algorithm's logic that will be executed by `execute(self)` if not in stub mode
        """

    @abstractmethod
    def execute_stub(self):
        """
        Define the algorithm's stub mode
        Put fake data into result and/or output files
        """

    @final
    def execute(self):
        stub_info = " in stub mode" if self.inputs.stub else ""
        execute = self.execute_stub if self.inputs.stub else self.execute_implementation

        self.logger.info(f"Executing algorithm{stub_info}...")
        execution_report = ExecutionReport(start=datetime.now(tz=timezone.utc))

        try:
            execute()
        except Exception:
            self.qc_report.result = QCResult.NA
            execution_report.status = ExecutionStatus.ERROR
            self.logger.exception(f"Error while executing the process{stub_info}")

        execution_report.stop = datetime.now(tz=timezone.utc)
        self.report.execution = execution_report

        self.outputs._outputs.add_section("report", asdict(self.report))
        self.outputs._outputs.add_section("qc", asdict(self.qc_report))
        self.outputs._outputs.add_section("result", self.result)

        self.outputs.to_files()
        self.outputs.compress_files(logger=self.logger)
        self.logger.info("Execution of algorithm finished")
