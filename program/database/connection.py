import os
from contextlib import contextmanager
from typing import Optional
import pymysql
from pymysql.connections import Connection
from pymysql.cursors import DictCursor


class DatabaseConfig:
    def __init__(self, host="127.0.0.1", port=3306, user="root", password="", database="lab_inventory", charset="utf8mb4", autocommit=False):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.autocommit = autocommit

    @classmethod
    def from_env(cls):
        return cls(
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "lab_inventory"),
        )

    def to_dict(self):
        return {
            "host": self.host,
            "port": self.port,
            "user": self.user,
            "password": self.password,
            "database": self.database,
            "charset": self.charset,
            "autocommit": self.autocommit,
            "cursorclass": DictCursor,
        }


class DatabaseConnection:
    def __init__(self, config):
        self.config = config
        self._connection = None

    def connect(self):
        if self._connection is None or not self._connection.open:
            self._connection = pymysql.connect(**self.config.to_dict())
        return self._connection

    def close(self):
        if self._connection and self._connection.open:
            self._connection.close()
            self._connection = None

    @contextmanager
    def transaction(self):
        conn = self.connect()
        try:
            conn.begin()
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise

    @contextmanager
    def cursor(self):
        conn = self.connect()
        cursor = conn.cursor()
        try:
            yield cursor
        finally:
            cursor.close()

    def ping(self):
        try:
            if self._connection and self._connection.open:
                self._connection.ping(reconnect=True)
                return True
        except Exception:
            pass
        return False


_db_instance = None

def get_database(config=None):
    global _db_instance
    if _db_instance is None:
        _db_instance = DatabaseConnection(config or DatabaseConfig.from_env())
    return _db_instance

def init_database(config=None):
    global _db_instance
    if _db_instance:
        _db_instance.close()
    _db_instance = DatabaseConnection(config or DatabaseConfig.from_env())
    return _db_instance

def close_database():
    global _db_instance
    if _db_instance:
        _db_instance.close()
        _db_instance = None
