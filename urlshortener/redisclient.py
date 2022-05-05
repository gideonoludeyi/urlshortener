from redis import Redis

from .client import Client


class RedisClient(Client):
    def __init__(self, host: str, port: int, password: str) -> None:
        self.redis = Redis(host=host, port=port, password=password)
        super().__init__()

    def get(self, code: str) -> str | None:
        url = self.redis.get(code)
        if url is not None:
            return url.decode('utf-8')

    def set(self, code: str, url: str) -> None:
        self.redis.set(code, url)

    def exists(self, code: str) -> bool:
        return self.redis.exists(code) == 1
