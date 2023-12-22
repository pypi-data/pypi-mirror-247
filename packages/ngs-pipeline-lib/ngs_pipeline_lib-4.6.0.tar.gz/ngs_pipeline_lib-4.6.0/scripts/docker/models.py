from pydantic import BaseSettings, root_validator

IMAGE_DEFAULT_PREFIX = "ngs-pipeline-process-"


class BuildSettings(BaseSettings):
    image_prefix: str = IMAGE_DEFAULT_PREFIX
    process_name: str
    tag: str = "latest"
    dockerfile: str = "Dockerfile"
    pip_registry_username: str | None
    pip_registry_password: str | None

    @root_validator(pre=True)
    def check_login_consistency(cls, values):
        username, password = values.get("pip_registry_username"), values.get(
            "pip_registry_password"
        )
        if username is not None and password is None:
            raise ValueError("PIP password is missing")
        if password is not None and username is None:
            raise ValueError("PIP username is missing")
        return values


class PushSettings(BaseSettings):
    image_prefix: str = IMAGE_DEFAULT_PREFIX
    process_name: str
    remote_docker_repo: str
    tag: str = "latest"
    docker_username: str | None
    docker_password: str | None

    @root_validator(pre=True)
    def check_login_consistency(cls, values):
        username, password = values.get("docker_username"), values.get(
            "docker_password"
        )
        if username is not None and password is None:
            raise ValueError("Docker password is missing")
        if password is not None and username is None:
            raise ValueError("Docker username is missing")
        return values
