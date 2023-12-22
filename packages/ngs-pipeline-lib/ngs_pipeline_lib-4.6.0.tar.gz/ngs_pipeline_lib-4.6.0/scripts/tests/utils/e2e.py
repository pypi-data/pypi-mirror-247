import csv
import json
import logging
import shutil
from pathlib import Path

from botocore.exceptions import ClientError

from scripts.tests.exceptions import TestError
from scripts.tests.models.e2e import (
    E2ERunSample,
    E2ERunSummary,
    E2EScenario,
    E2ETestArgs,
    E2ETestSettings,
    NextflowTask,
)
from scripts.tests.utils.common import (
    download_s3_file,
    explore_local_folder,
    explore_s3_folder,
)

logger = logging.getLogger("ngs-test")

DEFAULT_EXECUTION_FILENAME = "execution.json"
DEFAULT_TASK_FILENAME = "trace.txt"
DEFAULT_HASH_MAPPING_FILENAME = "sample_to_hash_map.tsv"
OUTPUT_SCENARIO_FILENAME = "scenario.json"
OUTPUT_EXECUTION_FILENAME = "execution.json"
OUTPUT_TASK_FILENAME = "trace.txt"
OUTPUT_HASH_MAPPING_FILENAME = "sample_to_hash_map.tsv"


def import_file(
    source_file: str, destination_filename: str, settings: E2ETestSettings
) -> Path:
    destination_path = settings.test_output_folder / destination_filename
    if source_file.startswith("s3://"):
        download_s3_file(
            url=source_file,
            destination_folder=settings.test_output_folder,
            destination_filename=destination_filename,
        )
    else:
        shutil.copyfile(source_file, destination_path)

    return destination_path


def explore_folder(folder: str) -> list[str]:
    if folder.startswith("s3://"):
        files = explore_s3_folder(url=folder)
    else:
        local_path = Path(folder)
        files = [
            str(path.relative_to(local_path))
            for path in explore_local_folder(local_path=local_path)
        ]

    return files


def get_scenario(args: E2ETestArgs, settings: E2ETestSettings) -> E2EScenario:
    import_file(
        source_file=args.scenario_file,
        destination_filename=OUTPUT_SCENARIO_FILENAME,
        settings=settings,
    )

    with open(
        settings.test_output_folder / OUTPUT_SCENARIO_FILENAME,
        mode="rt",
        encoding="utf-8",
    ) as f:
        scenario_json = json.load(f)
        scenario_json["scenario"]["path"] = str(settings.test_output_folder)
        scenario = E2EScenario(**scenario_json)

    return scenario


def load_params(args: E2ETestArgs, settings: E2ETestSettings) -> dict:
    src_file = (
        args.output_path.removesuffix("/") + "/" + settings.nextflow_execution_file
    )
    import_file(
        source_file=src_file,
        destination_filename=OUTPUT_EXECUTION_FILENAME,
        settings=settings,
    )

    execution_path = settings.test_output_folder / OUTPUT_EXECUTION_FILENAME
    params = {}
    with open(execution_path, mode="rt", encoding="utf-8") as file:
        params = json.load(file)

    return params


def load_tasks(args: E2ETestArgs, settings: E2ETestSettings) -> list[NextflowTask]:
    src_file = args.output_path.removesuffix("/") + "/" + settings.nextflow_trace_file
    try:
        import_file(
            source_file=src_file,
            destination_filename=OUTPUT_TASK_FILENAME,
            settings=settings,
        )
    except FileNotFoundError:
        raise TestError(f"Impossible to retrieve local trace file ({src_file}) ")
    except ClientError as e:
        raise TestError(f"Impossible to retrieve S3 trace file ({src_file} : {e}")

    task_file_path = settings.test_output_folder / OUTPUT_TASK_FILENAME
    tasks = []
    with open(task_file_path, mode="rt", encoding="utf-8") as file:
        tsv_file = csv.DictReader(file, delimiter="\t")

        for line in tsv_file:
            tasks.append(NextflowTask(**line))

    return tasks


def load_hashed_id_mapping(
    args: E2ETestArgs, settings: E2ETestSettings
) -> dict[str, str]:
    """
    Import HASHED_ID Mapping file from local/s3 path
    And then return a hashmap [id]=[hashed_id]
    """
    src_file = (
        args.output_path.removesuffix("/") + "/" + settings.nextflow_hashed_id_file
    )
    import_file(
        source_file=src_file,
        destination_filename=OUTPUT_HASH_MAPPING_FILENAME,
        settings=settings,
    )

    hashed_id_file_path = settings.test_output_folder / OUTPUT_HASH_MAPPING_FILENAME
    mappings = {}
    with open(hashed_id_file_path, mode="rt", encoding="utf-8") as file:
        tsv_file = csv.DictReader(file, delimiter="\t")

        for line in tsv_file:
            mappings[line["id"]] = line["hashed_id"]

    return mappings


def load_published_files(args: E2ETestArgs) -> dict[str, dict[str, list[str]]]:
    """
    Return the list of published files grouped by sample_id (or hashed_id)
    {
        "sample_id": {
            "downloadReads": ["1.json", "outputs.json"],
            "classifyReads": ["1.json", "outputs.json"],
            "cleanupReads": ["1.json", "outputs.json"],
        }
    }
    """
    published_files = explore_folder(args.output_path)

    files = {}

    for published_file in published_files:
        file_parts = published_file.split(sep="/", maxsplit=2)

        if len(file_parts) < 3:
            # We ignore files that are not located in sample/task subfolders
            continue
        sample_id = file_parts[0]
        task_name = file_parts[1]
        filename = file_parts[2]

        if sample_id not in files.keys():
            files[sample_id] = {}

        if task_name not in files[sample_id].keys():
            files[sample_id][task_name] = [filename]
        else:
            files[sample_id][task_name].append(filename)

    return files


def load_run_summary(
    args: E2ETestArgs, settings: E2ETestSettings
) -> dict[str, E2ERunSample]:
    # Init run summary object will all supervised sample_id
    run_summary = E2ERunSummary()

    tasks = load_tasks(args=args, settings=settings)
    for task in tasks:
        run_summary.add_task(task=task)

    params = load_params(args=args, settings=settings)
    run_summary.params = params

    hashed_id_mapping = load_hashed_id_mapping(args=args, settings=settings)
    for sample_id, hashed_id in hashed_id_mapping.items():
        run_summary.set_hashed_id(sample_id=sample_id, hashed_id=hashed_id)

    published_files = load_published_files(args=args)
    for sample_id in published_files.keys():
        for task_name, files in published_files[sample_id].items():
            run_summary.add_published_files(
                sample_id=sample_id, task_name=task_name, files=files
            )

    return run_summary


def check_sample_consistency(scenario: E2EScenario, run_summary: E2ERunSummary):
    expected_samples_id = [sample.sample_id for sample in scenario.samples]
    actual_samples_id = [sample.sample_id for sample in run_summary.samples]

    if (
        len(
            (
                missing_sample_ids := [
                    expected_sample_id
                    for expected_sample_id in expected_samples_id
                    if expected_sample_id not in actual_samples_id
                ]
            )
        )
        > 0
    ):
        raise TestError(
            f"Expected sample ids missing : {', '.join(missing_sample_ids)}"
        )

    if (
        len(
            (
                extra_sample_ids := [
                    actual_sample_id
                    for actual_sample_id in actual_samples_id
                    if actual_sample_id not in expected_samples_id
                ]
            )
        )
        > 0
    ):
        raise TestError(f"Extra sample ids missing : {', '.join(extra_sample_ids)}")

    """
    Throw error if one sample doesn't have hashed_id
    """
    if any(sample.hashed_id == "" for sample in run_summary.samples):
        missing_sample_id = [
            sample.sample_id for sample in run_summary.samples if sample.hashed_id == ""
        ]
        raise TestError(f"Missing hashed id for this sample_ids : {missing_sample_id}")


def check_task_coherence(scenario: E2EScenario, run_summary: E2ERunSummary):
    """
    Check for extra tasks or missing tasks, and different status
    """

    for scenario_sample in scenario.samples:
        run_sample = run_summary.get_sample(sample_id=scenario_sample.sample_id)

        expected_tasks = scenario_sample.tasks
        actual_tasks = run_sample.tasks

        if (
            len(
                (
                    missing_tasks := [
                        expected_task.name
                        for expected_task in expected_tasks
                        if expected_task.name
                        not in [task.process for task in actual_tasks]
                    ]
                )
            )
            > 0
        ):
            raise TestError(
                f"The following tasks are missing for sample_id {scenario_sample.sample_id} : {','.join(missing_tasks)}"
            )

        if (
            len(
                (
                    extra_tasks := [
                        extra_task.process
                        for extra_task in actual_tasks
                        if extra_task.process
                        not in [expected_task.name for expected_task in expected_tasks]
                    ]
                )
            )
            > 0
        ):
            raise TestError(
                f"The following tasks are not expected for sample_id {scenario_sample.sample_id} : {','.join(extra_tasks)}"
            )

        different_status = []
        for task in expected_tasks:
            corresponding_actual_task = run_sample.get_task(process_name=task.name)
            if task.status != corresponding_actual_task.status:
                different_status.append((task, corresponding_actual_task))

        if len(different_status) > 0:
            differences = "\n".join(
                [
                    f"{expected_task.name} - Expected : {expected_task.status} ; Current : {actual_task.status}"
                    for expected_task, actual_task in different_status
                ]
            )
            raise TestError(
                f"The following tasks have different status for sample {scenario_sample.sample_id} :\n{differences}"
            )


def check_published_files(
    scenario: E2EScenario, run_summary: E2ERunSummary, args: E2ETestArgs
):
    missing_files = []
    extra_files = []
    for scenario_sample in scenario.samples:
        run_sample = run_summary.get_sample(sample_id=scenario_sample.sample_id)

        scenario_tasks = scenario_sample.tasks

        for scenario_task in scenario_tasks:
            corresponding_actual_task = run_sample.get_task(
                process_name=scenario_task.name
            )

            missing = [
                file
                for file in scenario_task.files
                if file not in corresponding_actual_task.files
            ]
            if len(missing) > 0:
                missing_files.append(
                    (scenario_sample.sample_id, scenario_task.name, missing)
                )

            extra = [
                file
                for file in corresponding_actual_task.files
                if file not in scenario_task.files
            ]
            if len(extra) > 0:
                extra_files.append(
                    (scenario_sample.sample_id, scenario_task.name, extra)
                )

    if extra_files or missing_files:
        if extra_files:
            for sample_id, task, extra in extra_files:
                logger.error(
                    f"For sample {sample_id} in {task}, the following files are unknown : {','.join(extra)}"
                )
        if missing_files:
            for sample_id, task, missing in missing_files:
                logger.error(
                    f"For sample {sample_id} in {task}, the following files are missing : {','.join(missing)}"
                )

        raise TestError("Inconsistency in published files")
