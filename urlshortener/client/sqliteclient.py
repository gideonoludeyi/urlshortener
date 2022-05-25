import calendar
from datetime import datetime
import os
import sqlite3
from types import TracebackType
from typing import Type

from urlshortener.client.base import Client

SQLITE3_DB = os.getenv('SQLITE3_DB', 'sqlite_dev.db')


if not os.path.isfile(SQLITE3_DB):
    connection = sqlite3.connect(SQLITE3_DB)
    with connection:
        connection.execute(
            '''CREATE TABLE urls (code TEXT UNIQUE, url TEXT);''')
        connection.execute(
            '''CREATE TABLE users (email TEXT UNIQUE, hashed_password TEXT, ignore_access_tokens_before TIMESTAMP);''')
    connection.close()


class SQLiteClient(Client):
    def __init__(self, table_name: str, key_name: str) -> None:
        super().__init__()
        self.table_name = table_name
        self.key_name = key_name
        self.connection: sqlite3.Connection | None = None

    def _join_names(self, names: list[str]) -> str:
        return ','.join(names)

    def get(self, key: str) -> dict | None:
        if not self.connection:
            raise Exception(
                "cannot call .get outside of context. Consider using `with SQLiteClient(...) as client:`")

        values = self.connection.execute(f'''\
            SELECT {self._join_names(self.column_names)} FROM {self.table_name}
            WHERE {self.key_name} = ?;
            ''', (key,)).fetchone()

        if values is None:
            return None

        return dict(zip(self.column_names, values))

    def set(self, key: str, data: dict) -> None:
        data.update({self.key_name: key})
        items = data.items()

        values = [value for _, value in
                  sorted(items, key=lambda item: self.column_names.index(item[0]))]

        placeholder = self._join_names(['?'] * len(self.column_names))

        if not self.connection:
            raise Exception(
                "cannot call .set outside of context. Consider using `with SQLiteClient(...) as client:`")

        with self.connection:
            if self.exists(key):
                data.pop(self.key_name)
                self.connection.execute(f'''\
                    UPDATE {self.table_name}
                    SET
                       {','.join([f'{k} = ?' for k in data.keys()])}
                    WHERE {self.key_name} = ?
                    ''', (list(data.values()) + [key]))
            else:
                self.connection.execute(f'''\
                    INSERT INTO {self.table_name} ({self._join_names(self.column_names)})
                    VALUES ({placeholder});
                    ''', values)

    def exists(self, key: str) -> bool:
        if not self.connection:
            raise Exception(
                "cannot call .exists outside of context. Consider using `with SQLiteClient(...) as client:`")

        count, = self.connection.execute(f'''\
            SELECT COUNT(*) FROM {self.table_name}
            WHERE {self.key_name} = ?;
            ''', (key,)).fetchone()
        return count != 0

    def __enter__(self) -> Client:
        self.connection = sqlite3.connect(SQLITE3_DB)
        cursor = self.connection.execute(
            f'SELECT name FROM PRAGMA_TABLE_INFO("{self.table_name}");')
        self.column_names = [row[0] for row in cursor]
        return self

    def __exit__(self, __exc_type: Type[BaseException] | None, __exc_value: BaseException | None, __traceback: TracebackType | None) -> bool | None:
        if self.connection is not None:
            self.connection.close()
        return None


if __name__ == '__main__':
    with SQLiteClient('users', 'email') as client:
        print(client.get('pihwwir'))
        print(client.exists('pihwwir'))
        client.set('pihwwir', {'hashed_password': 'myprecious', 'ignore_access_tokens_before': calendar.timegm(
            datetime.utcnow().timetuple())})
        print(client.get('pihwwir'))
        print(client.exists('pihwwir'))
