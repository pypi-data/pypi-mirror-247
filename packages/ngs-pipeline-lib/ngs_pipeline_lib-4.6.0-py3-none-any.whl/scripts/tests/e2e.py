import logging

import boto3

from scripts.tests.exceptions import TestError
from scripts.tests.main import cli
from scripts.tests.models.e2e import E2ETestArgs, E2ETestSettings
from scripts.tests.utils.common import clean_files
from scripts.tests.utils.e2e import (
    check_published_files,
    check_sample_consistency,
    check_task_coherence,
    get_scenario,
    load_run_summary,
)

logger = logging.getLogger("ngs-test")


@cli.command()
def e2e(args: E2ETestArgs):
    run_settings = E2ETestSettings()

    boto3.setup_default_session(profile_name=run_settings.aws_profile)

    run_settings.test_output_folder.mkdir(parents=True, exist_ok=True)
    clean_files(path=run_settings.test_output_folder)

    try:
        scenario = get_scenario(args=args, settings=run_settings)

        run_summary = load_run_summary(args=args, settings=run_settings)

        check_sample_consistency(scenario=scenario, run_summary=run_summary)

        check_task_coherence(scenario=scenario, run_summary=run_summary)

        check_published_files(scenario=scenario, run_summary=run_summary, args=args)
    except TestError as e:
        logger.error(e)
