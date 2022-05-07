from types import TracebackType
from typing import Type

from .base import Client

db: dict[str, dict] = dict()


class InMemoryClient(Client):
    def __init__(self) -> None:
        super().__init__()

    def get(self, key: str) -> dict | None:
        return db.get(key)

    def set(self, key: str, data: dict) -> None:
        db[key] = data

    def exists(self, key: str) -> bool:
        return db.get(key) is not None

    def __exit__(self, __exc_type: Type[BaseException] | None, __exc_value: BaseException | None, __traceback: TracebackType | None) -> bool | None:
        return None
