from sqlmodel import select
from .base_repository import BaseRepository
from ..models.sensor import Sensor


class SensorRepository(BaseRepository[Sensor]):
    def __init__(self):
        super().__init__(Sensor)

    async def get_sensors_by_city(self, session, city_id: int):
        statement = select(self.model).where(self.model.city_id == city_id)
        return session.exec(statement).all()

    async def get_sensor_with_location(self, session, sensor_id: int):
        from sqlmodel import select
        from app.models.region import City

        statement = select(self.model, City).join(
            City).where(self.model.id == sensor_id)
        results = session.exec(statement).first()
        return results
