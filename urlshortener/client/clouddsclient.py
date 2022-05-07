import types
from typing import Type

from google.cloud import datastore
from google.oauth2 import service_account  # type: ignore

from .base import Client


class CloudDatastoreClient(Client):
    def __init__(self, kind: str = 'urls', service_account_filepath: str | None = None) -> None:
        super().__init__()

        self.kind = kind
        if service_account_filepath is not None:
            credentials = service_account.Credentials.from_service_account_file(
                service_account_filepath)
            self.client = datastore.Client(credentials=credentials)
        else:
            # imply credentials from the environment (eg: if deployed in a Google App Engine of same GCP project as Cloud Datastore)
            self.client = datastore.Client()

    def _to_key(self, key: str) -> datastore.Key:
        return self.client.key(self.kind, key)

    def get(self, key: str) -> dict | None:
        datastore_key = self._to_key(key)
        entity = self.client.get(key=datastore_key)
        if entity is not None:
            return dict(entity)
        else:
            return None

    def set(self, key: str, data: dict) -> None:
        datastore_key = self._to_key(key)
        entity = self.client.entity(key=datastore_key)
        entity.update({**entity, **data})
        self.client.put(entity=entity)

    def exists(self, key: str) -> bool:
        return self.get(key) is not None

    def __exit__(self, __exc_type: Type[BaseException] | None, __exc_value: BaseException | None, __traceback: types.TracebackType | None) -> bool | None:
        self.client.close()
        return None
