import abc


class Client(abc.ABC):
    @abc.abstractmethod
    def get(self, code: str) -> str | None:
        raise NotImplementedError

    @abc.abstractmethod
    def set(self, code: str, url: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def exists(self, code: str) -> bool:
        raise NotImplementedError
