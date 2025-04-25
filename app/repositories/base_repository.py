from typing import Generic, TypeVar, Type, List, Optional
from sqlmodel import SQLModel, select, Session

T = TypeVar('T', bound=SQLModel)


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model

    async def get_all(self, session: Session) -> List[T]:
        return session.exec(select(self.model)).all()

    async def get_by_id(self, session: Session, id: int) -> Optional[T]:
        return session.get(self.model, id)

    async def create(self, session: Session, obj_in: T) -> T:
        session.add(obj_in)
        session.commit()
        session.refresh(obj_in)
        return obj_in
