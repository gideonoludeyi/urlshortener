import types
from typing import Type

from google.cloud import datastore
from google.oauth2 import service_account

from .base import Client


class CloudDatastoreClient(Client):
    def __init__(self, kind: str = 'urls', service_account_filename: str | None = None) -> None:
        self.kind = kind
        if service_account_filename is not None:
            credentials = service_account.Credentials.from_service_account_file(
                service_account_filename)
            self.client = datastore.Client(credentials=credentials)
        else:
            # imply credentials from the environment (eg: if deployed in a Google App Engine of same GCP project as Cloud Datastore)
            self.client = datastore.Client()

    def _to_key(self, code: str) -> datastore.Key:
        return self.client.key(self.kind, code)

    def get(self, code: str) -> str | None:
        key = self._to_key(code)
        entity = self.client.get(key=key)
        if entity is not None:
            return entity.get('url')

    def set(self, code: str, url: str) -> None:
        key = self._to_key(code)
        entity = self.client.entity(key=key)
        entity.update({'url': url})
        self.client.put(entity=entity)

    def exists(self, code: str) -> bool:
        return self.get(code) is not None

    def __exit__(self, __exc_type: Type[BaseException] | None, __exc_value: BaseException | None, __traceback: types.TracebackType | None) -> bool | None:
        self.client.close()
