import json
from types import TracebackType
from typing import Type

from redis import Redis  # type: ignore

from .base import Client


class RedisClient(Client):
    def __init__(self, host: str, port: int, password: str, *, prefix: str = 'urls:') -> None:
        super().__init__()

        self.redis = Redis(host=host, port=port, password=password)
        self.prefix = prefix

    def _to_key(self, key: str) -> str:
        return self.prefix + key

    def get(self, key: str) -> dict | None:
        key = self._to_key(key)
        data = self.redis.get(key)
        if data is not None:
            return json.loads(data)
        else:
            return None

    def set(self, key: str, data: dict) -> None:
        key = self._to_key(key)
        value = json.dumps(data)
        self.redis.set(key, value)

    def exists(self, key: str) -> bool:
        key = self._to_key(key)
        return self.redis.exists(key) == 1

    def __exit__(self, __exc_type: Type[BaseException] | None, __exc_value: BaseException | None, __traceback: TracebackType | None) -> bool | None:
        self.redis.close()
        return None
