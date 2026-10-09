import logging
import os
from contextlib import contextmanager

import psycopg2
import psycopg2.extras
from psycopg2 import pool

psycopg2.extras.register_uuid()

logger = logging.getLogger(__name__)


class DAO:
    DB_HOST = "DB_HOST"
    DB_PORT = "DB_PORT"
    DB_USER = "DB_USER"
    DB_PASSWORD = "DB_PASSWORD"
    DB_DATABASE = "DB_DATABASE"
    DB_POOL_MIN = "DB_POOL_MIN"
    DB_POOL_MAX = "DB_POOL_MAX"

    # Pool compartilhado por todas as instâncias
    _pool: pool.ThreadedConnectionPool | None = None

    @classmethod
    def init_pool(cls) -> None:
        """Cria o pool uma única vez. Chame na inicialização da aplicação."""
        if cls._pool is not None:
            return
        try:
            cls._pool = pool.ThreadedConnectionPool(
                minconn=int(os.getenv(cls.DB_POOL_MIN, "1")),
                maxconn=int(os.getenv(cls.DB_POOL_MAX, "10")),
                user=os.getenv(cls.DB_USER, "postgres"),
                password=os.getenv(cls.DB_PASSWORD, "example"),
                host=os.getenv(cls.DB_HOST, "db"),
                port=os.getenv(cls.DB_PORT, "5432"),
                database=os.getenv(cls.DB_DATABASE, "todo"),
            )
        except Exception as ex:
            logger.error(f"error creating the connection pool: {ex}")
            raise

    @classmethod
    def close_pool(cls) -> None:
        """ Cloase all the connections."""
        if cls._pool is not None:
            cls._pool.closeall()
            cls._pool = None

    def __init__(self):
        DAO.init_pool()

    @contextmanager
    def _get_connection(self):
        """Get connection from the pool and always return it."""
        conn = DAO._pool.getconn()
        try:
            yield conn
        except Exception:
            conn.rollback()
            raise
        finally:
            DAO._pool.putconn(conn)

    def execute(self, sql: str, parameters: tuple = ()) -> int:
        with self._get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(sql, parameters)
            conn.commit()
            return cursor.rowcount

    def fetch_all(self, sql: str, parameters: tuple = ()) -> list:
        with self._get_connection() as conn, conn.cursor() as cursor:
            cursor.execute(sql, parameters)
            return cursor.fetchall()
