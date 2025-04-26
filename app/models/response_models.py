from sqlmodel import SQLModel
from typing import List, Optional
from datetime import datetime
from .region import Region, City
from .sensor import Sensor
from .record import Record


class CityWithSensors(SQLModel):
    id: int
    name: str
    latitude: float
    longitude: float
    region_id: int
    sensors: List[Sensor]


class RegionWithCities(SQLModel):
    id: int
    name: str
    cities: List[City]


class RegionWithSensors(SQLModel):
    id: int
    name: str
    sensors: List[Sensor]


class LatestRecord(SQLModel):
    id: int
    sensor_id: int
    time_stamp: datetime
    trash_level: int
    image: Optional[str] = None


class SensorWithLatestRecord(SQLModel):
    id: int
    name: str
    latitude: float
    longitude: float
    city_id: int
    latest_record: Optional[LatestRecord] = None


class SensorTrashLevel(SQLModel):
    sensor_id: int
    trash_level: int
    timestamp: datetime


class SensorAverageLevel(SQLModel):
    sensor_id: int
    average_level: float


class SensorPredictTrashLevel(SQLModel):
    sensor_id: int
    predicted_timestamp: datetime
    hours_until_full: int
    predicted_level: float
