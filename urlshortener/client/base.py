import abc
from contextlib import AbstractContextManager


class Client(AbstractContextManager, abc.ABC):
    @abc.abstractmethod
    def get(self, code: str) -> str | None:
        raise NotImplementedError

    @abc.abstractmethod
    def set(self, code: str, url: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def exists(self, code: str) -> bool:
        raise NotImplementedError

    def __enter__(self) -> 'Client':
        return self
