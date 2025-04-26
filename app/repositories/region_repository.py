from sqlmodel import select, Session
from typing import List, Optional
from .base_repository import BaseRepository
from ..models.region import Region, City
from ..models.sensor import Sensor


class RegionRepository(BaseRepository[Region]):
    def __init__(self):
        super().__init__(Region)

    async def get_by_name(self, session: Session, name: str) -> Optional[Region]:
        statement = select(self.model).where(self.model.name == name)
        return session.exec(statement).first()

    async def get_regions_with_cities(self, session: Session) -> List[dict]:
        """Get all regions with their associated cities"""
        regions = await self.get_all(session)
        result = []

        for region in regions:
            cities = session.exec(select(City).where(
                City.region_id == region.id)).all()
            result.append({
                "id": region.id,
                "name": region.name,
                "cities": cities
            })

        return result

    async def get_regions_with_sensors(self, session: Session) -> List[dict]:
        """Get all regions with their sensors (via cities)"""
        regions = await self.get_all(session)
        result = []

        for region in regions:
            cities = session.exec(select(City).where(
                City.region_id == region.id)).all()

            region_sensors = []
            for city in cities:
                sensors = session.exec(select(Sensor).where(
                    Sensor.city_id == city.id)).all()
                region_sensors.extend(sensors)

            result.append({
                "id": region.id,
                "name": region.name,
                "sensors": region_sensors
            })

        return result

    async def get_region_sensors(self, region_id: int, session: Session) -> List[Sensor]:
        """Get region sensors (via cities)"""
        result = []

        cities = session.exec(select(City).where(
            City.region_id == region_id)).all()

        region_sensors = []
        for city in cities:
            sensors = session.exec(select(Sensor).where(
                Sensor.city_id == city.id)).all()
            region_sensors.extend(sensors)

        return region_sensors


class CityRepository(BaseRepository[City]):
    def __init__(self):
        super().__init__(City)

    async def get_cities_by_region(self, session: Session, region_id: int) -> List[City]:
        statement = select(self.model).where(self.model.region_id == region_id)
        return session.exec(statement).all()

    async def get_city_with_sensors(self, session: Session, city_id: int) -> dict:
        """Get a city with all of its sensors"""
        city = await self.get_by_id(session, city_id)
        if not city:
            return None

        sensors = session.exec(select(Sensor).where(
            Sensor.city_id == city_id)).all()

        return {
            "id": city.id,
            "name": city.name,
            "latitude": city.latitude,
            "longitude": city.longitude,
            "region_id": city.region_id,
            "sensors": sensors
        }
