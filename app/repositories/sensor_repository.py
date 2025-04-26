from sqlmodel import select
from .base_repository import BaseRepository
from ..models.sensor import Sensor
from sqlmodel import Session


class SensorRepository(BaseRepository[Sensor]):
    def __init__(self):
        super().__init__(Sensor)

    async def get_sensors_by_city(
        self,
        session: Session,
        city_id: int
    ):
        statement = select(self.model).where(self.model.city_id == city_id)
        return session.exec(statement).all()

    async def get_sensor_with_location(self, session, sensor_id: int):
        from sqlmodel import select
        from app.models.region import City

        statement = select(self.model, City).join(
            City).where(self.model.id == sensor_id)
        results = session.exec(statement).first()
        return results

    async def get_latest_sensor_records(
        self,
        session,
        sensor_id: int,
        limit: int = 4
    ) -> list[dict]:
        """
        Get the latest N records for a specific sensor.

        Args:
            session: Database session
            sensor_id: ID of the sensor to get records for
            limit: Maximum number of records to return (default: 10)

        Returns:
            List of sensor records ordered by timestamp (newest first)
        """
        from ..models.record import Record
        from sqlmodel import select, desc

        statement = select(Record).where(
            Record.sensor_id == sensor_id
        ).order_by(
            desc(Record.time_stamp)
        ).limit(limit)

        records = session.exec(statement).all()

        return [
            {
                "id": record.id,
                "sensor_id": record.sensor_id,
                "timestamp": record.time_stamp,
                "trash_level": record.trash_level
            }
            for record in records
        ]
