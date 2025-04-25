from fastapi import APIRouter, HTTPException
from typing import List
from ..services.database import SessionDep
from ..repositories import sensor_repo, record_repo
from ..models.sensor import Sensor
from ..models.record import Record
from ..models.response_models import SensorWithLatestRecord

sensor_router = APIRouter(
    prefix="/sensor",
    tags=["Sensors"],
)

tag_metadata = {
    "name": "Sensors",
    "description": "Operations with trash sensors",
}


@sensor_router.post("/", response_model=Sensor)
async def add_sensor(sensor: Sensor, session: SessionDep):
    """Create a new sensor"""
    try:
        result = await sensor_repo.create(session, sensor)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=422, detail=f"Failed to create sensor: {str(e)}")


@sensor_router.get("/{sensor_id}", response_model=Sensor)
async def get_sensor(sensor_id: int, session: SessionDep):
    """Get a sensor by ID"""
    sensor = await sensor_repo.get_by_id(session, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    return sensor


@sensor_router.get("/{sensor_id}/record", response_model=Record)
async def get_latest_sensor_trash_level(sensor_id: int, session: SessionDep):
    """Get the latest record for a sensor"""
    record = await record_repo.get_latest_record(session, sensor_id)
    if not record:
        raise HTTPException(
            status_code=404, detail="No records found for this sensor")
    return record


@sensor_router.get("/{sensor_id}/records", response_model=List[Record])
async def get_sensor_records(sensor_id: int, session: SessionDep):
    """Get all records for a sensor"""
    records = await record_repo.get_records_by_sensor(session, sensor_id)
    return records


@sensor_router.get("/{sensor_id}/with-latest", response_model=SensorWithLatestRecord)
async def get_sensor_with_latest_record(sensor_id: int, session: SessionDep):
    """Get a sensor with its latest record"""
    sensor = await sensor_repo.get_by_id(session, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")

    latest = await record_repo.get_latest_record(session, sensor_id)

    return {
        "id": sensor.id,
        "name": sensor.name,
        "latitude": sensor.latitude,
        "longitude": sensor.longitude,
        "city_id": sensor.city_id,
        "latest_record": latest
    }
