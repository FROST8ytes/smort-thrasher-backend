from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine
from .env import CONNECTION_STRING

engine = create_engine(CONNECTION_STRING)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
