from typing import Annotated
import re
from fastapi import Depends
from sqlmodel import Session, create_engine
from sqlalchemy.engine.url import URL
from .env import CONNECTION_STRING


def parse_pg_unix_connection_string(conn_string):
    """Parse a PostgreSQL connection string with unix_sock parameter."""
    pattern = r"(postgresql\+pg8000)://([^:]+):([^@]+)@/([^?]+)\?unix_sock=(.+)"
    match = re.match(pattern, conn_string)

    if match:
        drivername = match.group(1)
        username = match.group(2)
        password = match.group(3)
        database = match.group(4)
        socket_path = match.group(5)

        if "/.s.PGSQL.5432" in socket_path:
            unix_socket_path = socket_path.rsplit("/.s.PGSQL.5432", 1)[0]
        else:
            unix_socket_path = socket_path

        return {
            "drivername": drivername,
            "username": username,
            "password": password,
            "database": database,
            "unix_socket_path": unix_socket_path
        }
    return None


parsed = parse_pg_unix_connection_string(CONNECTION_STRING)
if parsed is None:
    engine = create_engine(CONNECTION_STRING)
else:
    engine = create_engine(
        URL.create(
            drivername=parsed["drivername"],
            username=parsed["username"],
            password=parsed["password"],
            database=parsed["database"],
            host=parsed['unix_socket_path'],
        )
    )


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
