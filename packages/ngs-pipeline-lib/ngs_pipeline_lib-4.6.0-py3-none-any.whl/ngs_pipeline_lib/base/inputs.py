from json import load
from pathlib import Path

import pydantic
from pydantic import BaseModel, Field, root_validator, validator

from ngs_pipeline_lib.biotools.biotools import check_fasta, check_fastq


class BaseInputs(BaseModel):
    sample_id: str = Field(description="Sample ID")
    stub: bool = Field(
        description="Flag to activate the stub mode in the process execution.",
        default=False,
    )
    publish_dir: str = Field(
        description="Location where outputs are published (trailing slash enforced)."
    )
    n_threads: int = Field(description="Number of threads to use.", default=1)
    logging_dir: Path = Field(
        description="Location where logs are stored.", default=Path("logs")
    )

    @validator("publish_dir")
    def publish_dir_format(cls, v):
        # Remove surroundings square bracket sent by Nextflow
        if v[0] == "[":
            v = v[1:]
        if v[-1] == "]":
            v = v[:-1]

        # Add trailing slash if missing
        if v[-1] != "/":
            v = v + "/"

        return v

    def _get_kb_fields(self) -> set[str]:
        return {
            key
            for key, value in self.__fields__.items()
            if issubclass(value.type_, KnowledgeBase)
        }

    def inputs_as_string(self) -> str:
        return super().json(exclude=self._get_kb_fields())

    def kbs_as_string(self) -> str:
        return super().json(include=self._get_kb_fields())


class OrganismInput(BaseModel):
    genus: str = Field(description="Genus of the organism.", default=None)
    species: str = Field(description="Species of the organism.", default=None)

    @root_validator
    def check_genus_if_species(cls, values: dict):
        genus, species = values.get("genus"), values.get("species")
        if species and not genus:
            raise ValueError("Species was specified while genus was not.")
        return values

    @validator("genus")
    def _genus_to_upper(cls, v: str | None):
        return v.upper() if v is not None else None

    @validator("species")
    def _species_to_upper(cls, v: str | None):
        return v.upper() if v is not None else None

    @property
    def full_name(self) -> str | None:
        if self.genus and self.species:
            return f"{self.genus} {self.species}"
        if self.genus:
            return self.genus
        return None


class FilePath(pydantic.FilePath):
    """
    Replacement class for FilePath from pydantic to work with clidantic
    """

    _flavour = type(Path())._flavour


class DirectoryPath(pydantic.DirectoryPath):
    """
    Replacement class for DirectoryPath from pydantic to work with clidantic
    """

    _flavour = type(Path())._flavour


class FastaInput(FilePath):
    @classmethod
    def validate(cls, path: Path):
        super().validate(path)
        if not check_fasta(path):
            raise ValueError(f"{path} is not a fasta file ")
        return cls(path)


class FastqInput(FilePath):
    @classmethod
    def validate(cls, path: Path):
        super().validate(path)
        if not check_fastq(path):
            raise ValueError(f"{path} is not a fastq file ")
        return cls(path)


class JsonInput(FilePath):
    @classmethod
    def validate(cls, path: Path):
        super().validate(path)
        if not path.suffix == ".json":
            raise ValueError(f"{path} is not a json file ")
        return cls(path)

    def get_dict(self) -> dict:
        with open(self, encoding="utf-8") as reader:
            return load(reader)


class QCInput(JsonInput):
    ...


class KnowledgeBaseMeta(BaseModel):
    """
    Used only by the KnowledgeBase
    """

    name: str | None
    version: str | None


class KnowledgeBase(BaseModel):
    path: DirectoryPath
    meta: KnowledgeBaseMeta | None

    @classmethod
    def __init_subclass__(cls, **kwargs):
        cls.enforce_all_fields_optional()
        super().__init_subclass__(**kwargs)

    @classmethod
    def enforce_all_fields_optional(cls):
        # Validate that all fields in the subclass (but not the parent class) are optional
        for field in cls.__fields__.values():
            if field.required and field.name not in KnowledgeBase.__fields__.keys():
                raise TypeError(
                    f"All fields in {cls.__name__} must be optional. Field: {field.name} is not."
                )

    @root_validator(pre=True)
    def root_pre_validate(cls, values: dict):
        root_path = Path(values.get("path"))
        info_path = root_path / "info.json"
        with open(info_path, encoding="utf-8") as reader:
            info: dict = load(reader)

        # validate hard-coded path and meta attributes
        if "path" in info.keys():
            raise ValueError('"path" cannot be defined in info.json')
        if "meta" not in info.keys():
            raise ValueError('"meta" must be defined in info.json')

        # set additional defined info
        for key, value in info.items():
            if key not in cls.__fields__:
                continue
            if issubclass(cls.__fields__.get(key).type_, Path):
                values[key] = root_path / value
            else:
                values[key] = value

        return values

    @root_validator(pre=False)
    def root_post_validate(cls, values: dict):
        # check that all expected values have been set
        for key, value in values.items():
            if value is None:
                raise ValueError(f"KB field {key} is not set.")

        return values


class QCKnowledgeBase(KnowledgeBase):
    qc: QCInput | None = Field(
        description="Filepath to the quality control rules (.json)."
    )
