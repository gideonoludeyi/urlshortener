import abc
from contextlib import AbstractContextManager


class Client(AbstractContextManager, abc.ABC):
    @abc.abstractmethod
    def get(self, key: str) -> dict | None:
        raise NotImplementedError

    @abc.abstractmethod
    def set(self, key: str, data: dict) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def exists(self, key: str) -> bool:
        raise NotImplementedError

    def __enter__(self) -> 'Client':
        return self
