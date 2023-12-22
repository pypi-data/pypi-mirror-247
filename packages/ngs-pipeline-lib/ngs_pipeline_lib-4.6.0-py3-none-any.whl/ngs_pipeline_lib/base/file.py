import logging
import shutil
import tarfile
from abc import ABC, abstractmethod
from csv import writer as csv_writer
from dataclasses import dataclass, field
from io import StringIO
from json import dumps
from pathlib import Path
from typing import Any

from ngs_pipeline_lib.tools.json import NGSJSONEncoder

logger = logging.getLogger("ngs_pipeline_lib.file")


@dataclass
class File(ABC):
    name: str
    extension: str | None = None
    content: Any = None
    compress: bool = True

    @property
    def path(self) -> Path:
        if self.extension:
            return Path(self.name).with_suffix(self.extension)
        return Path(self.name)

    @property
    def output_path(self) -> Path:
        """
        Return filepath with the ".gz" suffix if its `compress` attribute is True
        Otherwise, simply return its path
        """
        if self.compress:
            return self.path.parent / (self.path.name + ".gz")
        else:
            return self.path

    @abstractmethod
    def to_file(self) -> None:
        """
        Take either the content of the file and write it in its path.
        It must be implemented in subclasses as the process is different wether the file is a text or binary one.
        """


@dataclass
class TextFile(File):
    extension: str = ".txt"
    content: str | None = None

    def _prepare(self) -> str:
        return self.content

    def to_file(self) -> None:
        try:
            with open(self.path, mode="x", encoding="utf-8") as writer:
                to_be_written = self._prepare()
                if to_be_written:
                    writer.write(to_be_written)
        except FileExistsError:
            """
            Existing file are not overriden
            """


@dataclass
class ArchiveFile(File):
    content: list[Path] = field(default_factory=list)
    extension: str = ".tar"

    def to_file(self):
        with tarfile.open(self.path, "w") as f:
            for path in self.content:
                if path.exists():
                    f.add(path)
                    if path.is_dir():
                        shutil.rmtree(path)
                    else:
                        path.unlink()
                else:
                    raise ValueError(
                        f"Missing file while building the archive file {self.path}"
                    )


@dataclass
class CsvFile(TextFile):
    extension: str = ".csv"
    content: list | None = None

    def _prepare(self) -> str:
        if self.content is not None:
            output = StringIO()
            writer = csv_writer(output)
            writer.writerows(self.content)
            return output.getvalue()
        else:
            return ""


@dataclass
class JsonFile(TextFile):
    extension: str = ".json"
    content: dict | None = None

    def _prepare(self) -> str:
        return dumps(self.content, cls=NGSJSONEncoder)


@dataclass
class OutputsFile(JsonFile):
    name: str = "outputs"
    compress: bool = False
    content: dict[str, dict] = field(default_factory=dict)

    def add_section(self, section_name: str, section_value: dict):
        self.content[section_name] = section_value


@dataclass
class ReadFile(TextFile):
    extension: str = ".fastq"


@dataclass
class AssemblyFile(TextFile):
    extension: str = ".fasta"
