import importlib
import logging

from clidantic import Parser  # type: ignore

cli = Parser()

FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("ngs-test")
logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(FORMATTER)

logger.addHandler(stream_handler)


def test():
    importlib.import_module("scripts.tests.e2e")
    importlib.import_module("scripts.tests.integration")
    cli()
