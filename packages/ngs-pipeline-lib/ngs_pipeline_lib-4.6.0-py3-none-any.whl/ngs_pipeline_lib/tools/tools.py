import hashlib
from pathlib import Path
from shutil import copyfileobj

from pgzip import open as pgzip_open


def gzip_file(uncompressed_file: Path, compressed_file: Path | None = None) -> None:
    if not uncompressed_file:
        raise ValueError("Uncompressed file argument is mandatory")
    if not compressed_file:
        compressed_file = uncompressed_file.with_suffix(
            uncompressed_file.suffix + ".gz"
        )
    with open(file=uncompressed_file, mode="rb") as source:
        with pgzip_open(filename=str(compressed_file), mode="wb") as target:
            copyfileobj(fsrc=source, fdst=target)


def gunzip_file(compressed_file: Path, uncompressed_file: Path | None = None) -> Path:
    if not compressed_file:
        raise ValueError("Compressed file argument is mandatory")
    if not compressed_file.suffix == ".gz":
        raise ValueError("Only gz files are handled")
    if not uncompressed_file:
        uncompressed_file = compressed_file.with_name(name=compressed_file.stem)
    with pgzip_open(filename=str(compressed_file), mode="rb") as source:
        with open(
            file=uncompressed_file,
            mode="wb",
        ) as target:
            copyfileobj(fsrc=source, fdst=target)
    return uncompressed_file


def to_camel_case(snake_str: str):
    if "_" not in snake_str:
        return snake_str[0].lower() + snake_str[1:]
    else:
        # We capitalize the first letter of each component except the first one
        # with the 'capitalize' method and join them together.
        camel_string = "".join(x.capitalize() for x in snake_str.lower().split("_"))
        return snake_str[0].lower() + camel_string[1:]


def hash_sequence(sequence: str) -> str:
    """
    Different hashing function from the one in tools,
    kept for the sake of comparison with the current implementation
    """
    md5 = hashlib.md5(sequence.encode("utf-8"))
    max_bits_in_result = 56
    p = (1 << max_bits_in_result) - 1
    rest = int(md5.hexdigest(), 16)
    result = 0
    while rest != 0:
        result = result ^ (rest & p)
        rest = rest >> max_bits_in_result
    return str(result)
