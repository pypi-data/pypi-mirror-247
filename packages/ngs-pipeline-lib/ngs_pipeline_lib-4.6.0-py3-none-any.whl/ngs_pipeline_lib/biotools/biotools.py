from gzip import open as gzip_open
from pathlib import Path
from typing import TextIO

_FASTA_EXTENSIONS = ["fna", "fasta", "fsa", "fas", "fa"]
_FASTQ_EXTENSIONS = ["fq", "fastq"]


def check_fasta(fasta_filepath: Path) -> bool:
    if not fasta_filepath.suffix:
        return False
    if fasta_filepath.suffix == ".gz":
        if not fasta_filepath.stem.split(".")[-1] in _FASTA_EXTENSIONS:
            return False
        with gzip_open(fasta_filepath, "rt", encoding="utf-8") as reader:
            first_character = reader.read(1)
    # suffix is guaranteed to be at least "."
    elif not fasta_filepath.suffix[1:] in _FASTA_EXTENSIONS:
        return False
    else:
        with open(file=fasta_filepath, encoding="utf-8") as reader:
            first_character = reader.read(1)
    if first_character != ">":
        return False
    return True


def check_fastq(fastq_filepath: Path) -> bool:
    def get_start_of_first_third_line(reader: TextIO) -> tuple[str, str]:
        """
        If the file is empty or too short; both or one returned value will be ''
        """
        start_of_first_line = reader.read(1)
        # skips the rest of the line
        reader.readline()
        # skipsthe 2nd line
        reader.readline()
        start_of_third_line = reader.read(1)
        return start_of_first_line, start_of_third_line

    if not fastq_filepath.suffix:
        return False
    if fastq_filepath.suffix == ".gz":
        if not fastq_filepath.stem.split(".")[-1] in _FASTQ_EXTENSIONS:
            return False
        with gzip_open(filename=fastq_filepath, mode="rt", encoding="utf-8") as reader:
            start_of_first_line, start_of_third_line = get_start_of_first_third_line(
                reader
            )
    # suffix is guaranteed to be at least "."
    elif not fastq_filepath.suffix[1:] in _FASTQ_EXTENSIONS:
        return False
    else:
        with open(file=fastq_filepath, encoding="utf-8") as reader:
            start_of_first_line, start_of_third_line = get_start_of_first_third_line(
                reader
            )
    if start_of_first_line != "@" or start_of_third_line != "+":
        return False
    return True
