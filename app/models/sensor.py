from sqlmodel import SQLModel, Field
from typing import Optional


class Sensor(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    latitude: float
    longitude: float
    name: str
    city_id: int = Field(foreign_key="city.id")
