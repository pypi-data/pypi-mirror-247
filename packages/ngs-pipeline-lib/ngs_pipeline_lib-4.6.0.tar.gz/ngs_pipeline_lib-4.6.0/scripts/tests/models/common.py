from pathlib import Path
from urllib.parse import urlparse

from pydantic import BaseModel


class ScenarioMetadata(BaseModel):
    name: str
    description: str
    path: Path


class S3Url:
    def __init__(self, url: str):
        self._parsed = urlparse(url, allow_fragments=False)

    @property
    def bucket(self) -> str:
        return self._parsed.netloc

    @property
    def key(self) -> str:
        if self._parsed.query:
            return self._parsed.path.lstrip("/") + "?" + self._parsed.query
        else:
            return self._parsed.path.lstrip("/")

    @property
    def url(self) -> str:
        return self._parsed.geturl()
