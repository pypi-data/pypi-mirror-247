from pydantic import BaseSettings


class RunSettings(BaseSettings):
    process_package: str = "src"
