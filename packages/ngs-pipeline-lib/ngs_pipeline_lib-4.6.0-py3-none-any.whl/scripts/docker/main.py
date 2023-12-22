import argparse
import logging
import os

import docker
from docker.errors import BuildError
from docker.models.images import Image

from scripts.docker.models import BuildSettings, PushSettings

logger = logging.getLogger("script")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

IMAGE_DEFAULT_PREFIX = "ngs-pipeline-process-"


def create_parser(description):
    # All the logic of argparse goes in this function
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-e",
        "--env-file",
        dest="env_file",
        default=".env",
        help="Specify which env file to use (default = .env)",
    )

    return parser


def build():
    args = create_parser("Helper script to build Process Docker image").parse_args()

    settings = BuildSettings(_env_file=args.env_file, _env_file_encoding="utf-8")
    client = docker.from_env()

    repository_name = f"{settings.image_prefix}{settings.process_name}"

    image_name = f"{repository_name}:{settings.tag}"
    logger.info(f"Building {image_name}")
    try:
        client.images.get(image_name)
        logger.info("Image already exists locally. Overwritting ...")
    except docker.errors.ImageNotFound:
        logger.info("Image does not exist locally.")

    if not os.path.isfile(settings.dockerfile):
        raise ValueError(
            f"The specified Dockerfile ({settings.dockerfile}) is not available. Please try with another path."
        )

    try:
        image, logs = client.images.build(
            tag=image_name,
            path=".",
            dockerfile=settings.dockerfile,
            buildargs={
                "PIP_REGISTRY_USERNAME": settings.pip_registry_username,
                "PIP_REGISTRY_PASSWORD": settings.pip_registry_password,
            },
        )
    except BuildError as e:
        logger.error(e)
        logs = e.build_log

    for log in logs:
        if "stream" in log:
            if (message := log["stream"]) != "\n":
                logger.info(message.strip())


def push():
    args = create_parser(
        "Helper script to push existing Process Docker image"
    ).parse_args()

    settings = PushSettings(_env_file=args.env_file, _env_file_encoding="utf-8")
    client = docker.from_env()

    repository_name = f"{settings.image_prefix}{settings.process_name}"

    image_name = f"{repository_name}:{settings.tag}"
    destination_repository = f"{settings.remote_docker_repo}/{repository_name}"
    destination_image_name = f"{destination_repository}:{settings.tag}"
    logger.info(f"Pushing {image_name} to {destination_image_name}")

    image: Image = client.images.get(image_name)
    image.tag(
        repository=f"{settings.remote_docker_repo}/{repository_name}",
        tag=settings.tag,
    )

    if settings.docker_username is not None:
        response = client.images.push(
            repository=destination_repository,
            tag=settings.tag,
            stream=True,
            decode=True,
            auth_config={
                "username": settings.docker_username,
                "password": settings.docker_password,
            },
        )
    else:
        response = client.images.push(
            repository=destination_repository,
            tag=settings.tag,
            stream=True,
            decode=True,
        )

    for log in response:
        logger.info(log)
