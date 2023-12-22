import re
from pathlib import Path
from typing import Any

from pydantic import BaseModel, BaseSettings, Field, ValidationError, validator

from scripts.tests.models.common import ScenarioMetadata


class Resources(BaseModel):
    cpu: int
    ram: str

    @validator("cpu")
    def validate_cpu(cls, v: int):
        if v < 1 or v > 64:
            raise ValidationError("CPU Allocation must be between 1 & 64")
        return v

    @validator("ram")
    def validate_ram(cls, v: str):
        pattern = r"^\d+[mgMG]$"
        match = re.match(pattern, v)
        if match is None:
            raise ValidationError(
                "You must provide RAM allocation with the format xxxM/G Exemple : 128m, 1g, 4g"
            )
        return v


class IntegrationTestDescription(BaseModel):
    scenario: ScenarioMetadata
    resources_allocation: Resources | None
    ngs_run_args: list
    inputs: dict[str, Any]
    expected_outputs: dict[str, str | dict]


class IntegrationTestArgs(BaseModel):
    post_clean: bool = Field(
        description="Whether to clear test input/output files at the end of the test.",
        default=True,
    )
    name_filter: list[str] | None = Field(
        description="Filter tests scenarios by name (insensitive)"
    )


class IntegrationTestSettings(BaseSettings):
    use_docker_repo: bool = False

    docker_image_repo: str = Field(env="REMOTE_DOCKER_REPO")
    docker_image_prefix: str = Field(env="IMAGE_PREFIX")
    docker_image_name: str = Field(env="PROCESS_NAME")
    docker_image_tag: str = Field(default="latest", env="TAG")
    aws_profile: str = Field(env="PROFILE")

    test_scenarios_folder: Path = Field(
        env="TEST_SCENARIOS_FOLDER", default=Path("tests/integration/scenarios")
    )
    test_output_folder: Path = Field(
        env="TEST_OUTPUT_FOLDER", default=Path("tests/integration/outputs")
    )
    test_local_input_folder: Path = Field(
        env="TEST_LOCAL_INPUT_FOLDER", default=Path("tests/integration/inputs")
    )
    test_description_filename: str = Field(
        env="TEST_CONFIGURATION_FILENAME", default="test.json"
    )

    @property
    def docker_image(self):
        repo = self.docker_image_repo.removesuffix("/")
        prefix = self.docker_image_prefix
        name = self.docker_image_name

        if self.use_docker_repo:
            return f"{repo}/{prefix}{name}"
        else:
            return f"{prefix}{name}"

    class Config:
        env_file = ".env"
