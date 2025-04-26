from pydantic import BaseModel


class DriverLocationInput(BaseModel):
    latitude: str
    longitude: str
    region_id: int
