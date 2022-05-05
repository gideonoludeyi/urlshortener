from .base import Client
from .clouddsclient import CloudDatastoreClient
from .redisclient import RedisClient


def get_cloud_datastore_client(kind='urls', service_account_filepath: str | None = None):
    with CloudDatastoreClient(
            kind=kind,
            service_account_filename=service_account_filepath) as client:
        yield client


def get_redis_client(host: str, port: int, password: str):
    with RedisClient(host, port, password) as client:
        yield client
