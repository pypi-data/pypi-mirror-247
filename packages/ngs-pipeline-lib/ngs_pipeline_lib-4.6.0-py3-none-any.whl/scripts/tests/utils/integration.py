import json
import logging
import os
import shutil
import tarfile
from pathlib import Path

import docker
import flatdict
from botocore.exceptions import ClientError
from docker.errors import APIError
from docker.models.containers import Container

from scripts.tests.exceptions import TestError
from scripts.tests.models.integration import (
    IntegrationTestDescription,
    IntegrationTestSettings,
)
from scripts.tests.utils.common import (
    clean_files,
    download_s3_file,
    download_s3_folder,
    get_json_file_content,
    hash_file,
)

logger = logging.getLogger("ngs-test")


def get_test_description(
    path: Path, run_settings: IntegrationTestSettings
) -> IntegrationTestDescription:
    """
    Construct a Test Scenario from a specific path
    It test.json (can be override in run_settings) to build the scenario

    Raises an exception if file is missing or if content doesn't fulfill model specification
    """
    try:
        with open(
            path / run_settings.test_description_filename, encoding="utf-8"
        ) as json_file:
            test_json = json.load(json_file)
            test_json["scenario"]["path"] = path
            return IntegrationTestDescription(**test_json)
    except Exception as e:
        logger.error(e)
        raise TestError("Impossible to parse test.json file")


def get_test_scenarios(
    run_settings: IntegrationTestSettings, name_filters: list[str]
) -> list[IntegrationTestDescription]:
    """
    Iterate over all subfolders in the run_settings.test_scenarios_folder to find test scenarios
    Filter scenarios based on their name and specified name filter
    """
    scenarios_path = [
        path for path in run_settings.test_scenarios_folder.iterdir() if path.is_dir()
    ]
    scenarios = [
        get_test_description(path=scenario_path, run_settings=run_settings)
        for scenario_path in scenarios_path
    ]

    filtered_scenarios = (
        [
            scenario
            for scenario in scenarios
            if all(
                filter.lower() in scenario.scenario.name.lower()
                for filter in name_filters
            )
        ]
        if name_filters
        else scenarios
    )
    return filtered_scenarios


def import_remote_input_files(
    test: IntegrationTestDescription, input_folder: Path
) -> dict[str, str]:
    """
    Iterate over all input files in the scenario and ignore non-dict value
    If downloads file/folder specified in the URL and drop them in the local input folder.
    The file/folder name used locally is the one specified in stage_as

    Return : dict of inputs files updated with local path

    Raise exception if type,url and stage_as are not in the dict
    Raise exception if url is not a S3 URL
    """
    local_input_files = {}
    for key, value in test.inputs.items():
        if not isinstance(value, dict):
            continue

        if "type" not in value or "url" not in value or "stage_as" not in value:
            raise TestError(
                f"Incompatible input file {key} : Missing information in remove input description. Please provide type(file/folder), url and stage_as"
            )

        if value["type"] not in ["file", "folder"]:
            raise TestError(
                f"Incompatible input file {key} : Only 'file' and 'folder' are supported for 'type' attribute."
            )

        if not isinstance(value["url"], str) or not value["url"].startswith("s3://"):
            raise TestError(
                f"Incompatible input file {key} : Only S3 is supported for remote input files"
            )

        if value["type"] == "file":
            local_filename = value["stage_as"]
            destination_file = Path(input_folder / local_filename)

            # Ignore existing input files
            if destination_file.exists():
                local_input_files[key] = str(destination_file)
                continue

            download_s3_file(
                url=value["url"],
                destination_folder=input_folder,
                destination_filename=local_filename,
            )
            local_input_files[key] = str(destination_file)
        else:
            local_folder = input_folder / str(value["stage_as"])

            # Ignore existing input files
            if local_folder.exists():
                local_input_files[key] = str(local_folder)
                continue

            download_s3_folder(url=value["url"], destination_folder=local_folder)
            local_input_files[key] = str(local_folder)

    return local_input_files


def run_test_container(
    test: IntegrationTestDescription, run_settings: IntegrationTestSettings
):
    """
    Run the container associated the current run settings.
    It uses the args & input specified in the scenario to construct the command to pass to Docker
    """
    docker_args = "ngs-run"
    for arg in test.ngs_run_args:
        docker_args += f" {arg}"

    for key, value in test.inputs.items():
        if value is True:
            docker_args += f" --{key}"
        elif value is False:
            docker_args += f" --no-{key}"
        else:
            docker_args += f" --{key} {value}"

    resources_allocation = {}
    if test.resources_allocation is not None:
        if test.resources_allocation.cpu:
            resources_allocation["nano_cpus"] = int(test.resources_allocation.cpu * 1e9)
        if test.resources_allocation.ram:
            resources_allocation["mem_limit"] = test.resources_allocation.ram

    client = docker.from_env()
    container: Container = client.containers.run(
        run_settings.docker_image,
        command=docker_args,
        detach=True,
        volumes={
            run_settings.test_local_input_folder.absolute(): {
                "bind": f"/app/{run_settings.test_local_input_folder}",
                "mode": "rw",
            }
        },
        **resources_allocation,
    )

    logger.info(f"\tWaiting for container completion ({run_settings.docker_image})")
    status = container.wait()
    logger.info("\tContainer terminated.")

    if status["StatusCode"] != 0:
        logger.warning(container.logs())
        raise TestError(
            f"The container execution exited with an error code : {status['StatusCode']}"
        )

    return container


def get_test_container_output_files(
    container: Container,
    test_configuration: IntegrationTestDescription,
    output_folder: Path,
):
    """
    Iterate on all expected output files and try to retrieve it from the runned container.
    It assumes the files are produced at the /app/ folder in the container.
    Docker allow only to download as tar file. This method will extract the file from the archive
    And then it delete the temporary archive.

    Raise an exception if the expected file is missing within the container.
    """
    output_folder.mkdir(parents=True, exist_ok=True)
    clean_files(output_folder)
    for output_file in test_configuration.expected_outputs.keys():
        try:
            container_file_path = f"/app/{output_file}"
            bits, stat = container.get_archive(container_file_path)

            local_tar_path = output_folder / f"{output_file}.tar"
            # Handle subfolders creation
            local_tar_path.parent.mkdir(parents=True, exist_ok=True)
            with open(local_tar_path, "wb") as f:
                for chunk in bits:
                    f.write(chunk)

            with tarfile.open(local_tar_path, mode="r") as tar:
                tar.extractall(path=local_tar_path.parent)

            os.remove(local_tar_path)

        except APIError as e:
            raise TestError(
                f"The expected output file is missing in the container : {container_file_path}. Docker exception : {e}"
            )


def import_expected_output_files(
    test_configuration: IntegrationTestDescription,
    scenario_path: Path,
    output_folder: Path,
):
    """
    Iterate over all expected_output_files and import the corresponding value
    If value is
        - S3Url : it download the file into the output folder
        - Local URL : it copy the file into the output folder
        - Dict : it dumps the dict into a JSON file within the output folder

    Raise an exception if a dict value is used while the expected file is not a JSON file.
    """
    for key, value in test_configuration.expected_outputs.items():
        if isinstance(value, str):
            destination_path = output_folder / key
            destination_path = destination_path.with_name(
                f"expected_{destination_path.name}"
            )

            if value.startswith("s3://"):
                logger.info(f"\tDownloading S3 Expected Output File for {key}")
                try:
                    download_s3_file(
                        url=value,
                        destination_folder=destination_path.parent,
                        destination_filename=destination_path.name,
                    )
                except ClientError:
                    raise TestError(
                        f"Impossible to retrieve expected output file for {key}"
                    )
            else:
                logger.info(f"\tCopying local File for {key}")
                file_path = (scenario_path / value).resolve()
                shutil.copy(
                    file_path,
                    destination_path,
                )
        elif isinstance(value, dict):
            if key.endswith(".json"):
                json_object = json.dumps(value, indent=4)

                # Writing to JSON file
                with open(
                    f"{output_folder}/expected_{key}", "w", encoding="utf-8"
                ) as expected_output_file:
                    expected_output_file.write(json_object)
            else:
                raise TestError(
                    f"Only JSON files can contain JSON data. Change {key} name or value accordingly."
                )


def compare_output_files(
    test_configuration: IntegrationTestDescription,
    output_folder: Path,
) -> None:
    """
    Iterate over all expected_output_files and compare them
    The comparison mode is determined based on the expected file extension
    - *.json : compare key/value in the JSON content
    - others : compare file checksum
    """
    for output_file in test_configuration.expected_outputs.keys():
        logger.info(f"\tComparing output file {output_file}")
        output_file_path = output_folder / output_file

        expected_output_file_path = output_folder / output_file
        expected_output_file_path = expected_output_file_path.with_name(
            f"expected_{expected_output_file_path.name}"
        )

        extension = (
            output_file_path.suffixes[0] if len(output_file_path.suffixes) > 0 else None
        )
        if extension is None:
            raise TestError(f"Unknown extension for output_file {output_file_path}")

        if extension == ".json":
            compare_json_files(
                output_file=output_file_path,
                expected_output_file=expected_output_file_path,
            )
        else:
            compare_files(
                output_file=output_file_path,
                expected_output_file=expected_output_file_path,
            )


def order_dict(obj):
    if isinstance(obj, dict):
        return sorted((k, order_dict(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(order_dict(x) for x in obj)
    else:
        return obj


def compare_json_files(output_file: Path, expected_output_file: Path):
    """
    Compare two JSON file (can be gzipped)
    The JSON contents are flattened and then, we ensure every key from the
    expected output file is present and with the same value in the output_file
    If the expected value is "<<ONLY_CHECK_DEFINED>>" then we just ensure the key is present.
        Even a None value will be accepted in this case.
    """
    json_only_check_presence = "<<ONLY_CHECK_DEFINED>>"

    output_dict = order_dict(get_json_file_content(file=output_file))
    expected_output_dict = order_dict(get_json_file_content(file=expected_output_file))

    flat_output = flatdict.FlatterDict(output_dict)
    flat_expected_output = flatdict.FlatterDict(expected_output_dict)

    mismatch = False
    for expected_key, expected_value in flat_expected_output.items():
        if expected_key not in flat_output:
            logger.info(f"\tMissing information in {output_file} : {expected_key}")
            mismatch = True
            continue

        if type(expected_value) == str and expected_value == json_only_check_presence:
            continue

        if flat_output[expected_key] != expected_value:
            logger.info(
                f"\tDifferent information in {output_file.name} for {expected_key} : Expected={expected_value} ; Current={flat_output[expected_key]}"
            )
            mismatch = True
            continue

    if mismatch:
        raise TestError(f"Output file {output_file.name} is different than expected")


def compare_files(output_file: Path, expected_output_file: Path):
    output_checksum = hash_file(filepath=output_file)
    expected_output_checksum = hash_file(filepath=expected_output_file)

    if output_checksum != expected_output_checksum:
        raise TestError(
            f"Different files for {output_file.name}. Expected checksum={expected_output_checksum} ; Current checksum={output_checksum}"
        )
