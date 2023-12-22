import importlib
import logging
import sys

from ngs_pipeline_lib.cli import cli
from scripts.run.models import RunSettings

logger = logging.getLogger("ngs-run")


def run():
    settings = RunSettings()
    sys.path.insert(0, ".")
    importlib.import_module(settings.process_package, package=".")

    try:
        cli()
    except ValueError as e:
        logger.error(
            "Specified module doesn't contain any @cli.command. Check your PROCESS_PACKAGE env var"
        )
        raise e
