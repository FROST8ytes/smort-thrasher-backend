from sqlmodel import select, desc
from typing import List, Optional
from datetime import datetime
from .base_repository import BaseRepository
from ..models.record import Record


class RecordRepository(BaseRepository[Record]):
    def __init__(self):
        super().__init__(Record)

    async def get_records_by_sensor(self, session, sensor_id: int) -> List[Record]:
        statement = select(self.model).where(self.model.sensor_id == sensor_id)
        return session.exec(statement).all()

    async def get_latest_record(self, session, sensor_id: int) -> Optional[Record]:
        statement = select(self.model).where(
            self.model.sensor_id == sensor_id
        ).order_by(desc(self.model.time_stamp)).limit(1)

        return session.exec(statement).first()

    async def get_records_in_timeframe(
            self,
            session,
            sensor_id: int,
            start_time: datetime,
            end_time: datetime) -> List[Record]:
        statement = select(self.model).where(
            self.model.sensor_id == sensor_id,
            self.model.time_stamp >= start_time,
            self.model.time_stamp <= end_time
        ).order_by(self.model.time_stamp)

        return session.exec(statement).all()
