from typing import Optional

import psycopg2
from psycopg2._psycopg import connection
from psycopg2.extras import RealDictCursor

db_conn: Optional[connection] = None


def init_connection():
    global db_conn
    db_conn = psycopg2.connect(
        user="postgres",
        password="mysecretpassword",
        host="localhost",
        port="5432",
        database="postgres",
        cursor_factory=RealDictCursor,
    )


def close_connection():
    global db_conn
    try:
        db_conn.close()
    except:  # noqa
        pass


def get_connection() -> connection:
    if db_conn is None:
        raise ValueError("La connexion à la bdd n'est pas établie")
    return db_conn
