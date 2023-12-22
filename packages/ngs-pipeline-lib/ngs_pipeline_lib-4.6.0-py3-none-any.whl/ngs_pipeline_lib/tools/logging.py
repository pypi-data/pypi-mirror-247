from logging import DEBUG, FileHandler, Formatter, Logger, StreamHandler, getLogger
from pathlib import Path

FORMATTER = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def setup_logging(logging_dir: Path) -> Logger:
    logging_dir.mkdir(parents=True, exist_ok=True)
    logger = getLogger("main")
    logger.setLevel(DEBUG)

    file_handler = FileHandler(logging_dir / "messages.log")
    file_handler.setLevel(DEBUG)
    file_handler.setFormatter(FORMATTER)

    stream_handler = StreamHandler()
    stream_handler.setLevel(DEBUG)
    stream_handler.setFormatter(FORMATTER)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.info("Logger initialized")

    return logger
