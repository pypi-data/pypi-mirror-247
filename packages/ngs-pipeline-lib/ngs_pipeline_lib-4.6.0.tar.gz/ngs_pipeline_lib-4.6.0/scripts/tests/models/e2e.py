import re
from pathlib import Path

from pydantic import BaseModel, BaseSettings, Field, ValidationError, validator

from scripts.tests.models.common import ScenarioMetadata


class E2ETestSettings(BaseSettings):
    aws_profile: str = Field(env="PROFILE", default="ADX_DEV")
    test_output_folder: Path = Field(
        env="TEST_OUTPUT_FOLDER", default=Path("tests/e2e/outputs")
    )
    nextflow_trace_file: str = Field(env="NEXTFLOW_TRACE_FILE", default="trace.txt")
    nextflow_execution_file: str = Field(
        env="NEXTFLOW_EXECUTION_FILE", default="execution.json"
    )
    nextflow_hashed_id_file: str = Field(
        env="NEXTFLOW_HASHED_ID_FILE", default="sample_to_hash_map.tsv"
    )

    class Config:
        env_file = ".env"


class E2ETestArgs(BaseModel):
    scenario_file: str = Field(
        description="Scenario to test the pipeline with (Local or S3 file)",
    )
    output_path: str = Field(
        description="Pipeline output_dir to test (Local or S3 Folder)",
    )

    @validator("scenario_file")
    def validate_scenario_file(cls, v: str):
        if v.startswith("s3://"):
            return v
        elif Path(v).exists() and (Path(v).is_file() or Path(v).is_symlink()):
            return v
        else:
            raise ValidationError(
                "Scenario File must be a S3 Path or an existing local file"
            )

    @validator("output_path")
    def validate_output_path(cls, v: str):
        if v.startswith("s3://"):
            return v
        elif Path(v).exists() and Path(v).is_dir():
            return v
        else:
            raise ValidationError(
                "Output Path must be a S3 Path or an existing local folder"
            )


class NextflowTask(BaseModel):
    task_id: int
    hash: str
    name: str
    status: str
    exit: int
    files: list[str] = Field(default_factory=list)

    @property
    def sample_id(self):
        return re.search(r".*\((.*)\)$", self.name).group(1)

    @property
    def process(self):
        return re.search(r"^.*:(.*) ", self.name).group(1)

    @property
    def workflow(self):
        return re.search(r"^(.*):.* ", self.name).group(1)


class E2ERunSample(BaseModel):
    sample_id: str = ""
    hashed_id: str = ""
    tasks: list[NextflowTask] = Field(default_factory=list)

    def get_task(self, process_name: str) -> NextflowTask | None:
        """
        Get NextflowTast for the given task name
        """
        return next(
            filter(lambda task: task.process == process_name, self.tasks),
            None,
        )


class E2ERunSummary(BaseModel):
    params: dict = Field(default_factory=dict)
    samples: list[E2ERunSample] = Field(default_factory=list)

    def get_sample(
        self, sample_id: str | None = None, hashed_id: str | None = None
    ) -> E2ERunSample:
        """
        Get or Create E2ERunSample for the given sample_id or hashed_id
        Provide sample_id or hashed_id, not both
        """
        assert sample_id is not None or hashed_id is not None
        assert not (sample_id is not None and hashed_id is not None)

        if sample_id is not None:
            sample = next(
                filter(lambda sample: sample.sample_id == sample_id, self.samples),
                None,
            )
            if sample is None:
                sample = E2ERunSample(sample_id=sample_id)
                self.samples.append(sample)
            return sample
        else:
            sample = next(
                filter(lambda sample: sample.hashed_id == hashed_id, self.samples),
                None,
            )
            if sample is None:
                sample = E2ERunSample(hashed_id=hashed_id)
                self.samples.append(sample)
            return sample

    def add_task(self, task: NextflowTask):
        sample = self.get_sample(sample_id=task.sample_id)
        sample.tasks.append(task)

    def set_hashed_id(self, sample_id: str, hashed_id: str):
        sample = self.get_sample(sample_id=sample_id)
        sample.hashed_id = hashed_id

    def add_published_files(self, sample_id: str, task_name: str, files: list[str]):
        """
        Add published file for a given sample and a given task
        sample_id can be sample_id or hashed_id, based on Run params
        """
        if self.params["use_sample_id"]:
            sample = self.get_sample(sample_id=sample_id)
        else:
            sample = self.get_sample(hashed_id=sample_id)
        task = sample.get_task(process_name=task_name)

        if task is not None:
            task.files.extend(files)
        else:
            raise ValueError(
                f"Cannot find task {task_name} for sample_id {sample_id} when adding published files. Check consistency between output_dir and trace file"
            )


class E2EScenarioTask(BaseModel):
    name: str
    status: str
    files: list[str]


class E2EScenarioSample(BaseModel):
    sample_id: str
    tasks: list[E2EScenarioTask]


class E2EScenario(BaseModel):
    scenario: ScenarioMetadata
    samples: list[E2EScenarioSample]
