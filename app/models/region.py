from sqlmodel import SQLModel, Field
from typing import Optional


class Region(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    name: str = Field(unique=True)
    state: str
    emblem_url: str | None = None


class City(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True, index=True)
    name: str
    latitude: float
    longitude: float
    region_id: int = Field(foreign_key="region.id")
