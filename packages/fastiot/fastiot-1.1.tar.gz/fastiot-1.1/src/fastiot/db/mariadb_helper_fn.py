import sys
import time
from typing import Optional

import pymysql.err

from fastiot import logging
from fastiot.env.env import env_mariadb
from fastiot.exceptions.exceptions import ServiceError


def get_mariadb_client_from_env(schema: Optional[str] = None):
    """
    Establishes a connection to a MariaDB instance and returns a Connection object.

    An optional schema name can be specified. The connection should be closed before termination.

    For connecting Mariadb, the environment variables can be set,
    if you want to use your own settings instead of default:
    :envvar:`FASTIOT_MARIA_DB_HOST`, :envvar:`FASTIOT_MARIA_DB_PORT`, :envvar:`FASTIOT_MARIA_DB_USER`,
    :envvar:`FASTIOT_MARIA_DB_PASSWORD`, :envvar:`FASTIOT_MARIA_DB_SCHEMA_FASTIOTLIB`

    >>> mariadb_client = get_mariadb_client_from_env(schema=None)
    You should create a schema using `init_schema()` after opening the connection.
    """
    db_client = get_mariadb_client(
        host=env_mariadb.host,
        port=env_mariadb.port,
        schema=schema,
        user=env_mariadb.user,
        password=env_mariadb.password
    )
    return db_client


def get_mariadb_client(host: str, port: int, schema: Optional[str],
                       user: str, password: str):
    # We found that mariadb initial start time takes very long in some environments. Therefore we need a timeout much
    # greater then two minutes.
    try:
        # pylint: disable=import-outside-toplevel
        import pymysql.cursors
    except (ImportError, ModuleNotFoundError):
        logging.error("You have to manually install `fastiot[mariadb]` or `PyMySQL>=1.0,<2` using your "
                      "`pyproject.toml` to make use of this helper.")
        sys.exit(5)

    for _ in range(10):
        try:
            db_client = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=schema,
                cursorclass=pymysql.cursors.DictCursor
            )
            return db_client
        except pymysql.err.OperationalError as exception:
            logging.error("Error connecting to MariaDB: %s", str(exception))
            time.sleep(1)
    raise ServiceError("Giving up trials to connect to MariaDB")


def init_schema(connection, schema: str):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                query=f'CREATE SCHEMA {schema}'
            )
        connection.commit()
    except pymysql.err.ProgrammingError as e:
        logging.info('%s', str(e))
