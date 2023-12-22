from abc import ABCMeta
from logging import Logger

from ngs_pipeline_lib.base.file import File, OutputsFile
from ngs_pipeline_lib.tools.tools import gzip_file


class BaseOutputs(metaclass=ABCMeta):
    def __init__(self):
        self._outputs = OutputsFile()

    @property
    def files(self) -> list[File]:
        return [value for value in vars(self).values() if isinstance(value, File)]

    @property
    def files_path(self) -> list[str]:
        return [str(file.output_path) for file in self.files]

    def to_files(self):
        for file_ in self.files:
            file_.to_file()

    def compress_files(self, logger: Logger):
        for file_ in self.files:
            if file_.compress:
                logger.info(f"Compressing file: {file_.path}")
                gzip_file(file_.path)
                logger.info(f"Done compressing file: {file_.path}")
                file_.path.unlink()
