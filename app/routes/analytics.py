from fastapi import APIRouter
from sqlmodel import select, func
from typing import List
from ..services.database import SessionDep
from ..repositories import record_repo
from ..models.record import Record
from ..models.sensor import Sensor
from ..models.response_models import SensorTrashLevel, SensorAverageLevel

analytics_router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)

tag_metadata = {
    "name": "Analytics",
    "description": "Analytical operations on trash data",
}


@analytics_router.get("/level/{region_id}", response_model=List[SensorTrashLevel])
async def get_latest_trash_levels_in_region(region_id: int, session: SessionDep):
    """Get the latest trash levels for all sensors in a specific region"""
    from app.models.region import City

    statement = select(Sensor.id).join(City).where(City.region_id == region_id)
    sensor_ids = [row[0] for row in session.exec(statement)]

    result = []
    for sensor_id in sensor_ids:
        latest = await record_repo.get_latest_record(session, sensor_id)
        if latest:
            result.append({
                "sensor_id": sensor_id,
                "trash_level": latest.trash_level,
                "timestamp": latest.time_stamp
            })

    return result


@analytics_router.get("/average/all", response_model=List[SensorAverageLevel])
async def get_average_trash_levels_all_sensors(session: SessionDep):
    """Get average trash levels across all sensors"""
    statement = select(
        Record.sensor_id,
        func.avg(Record.trash_level).label("average_level")
    ).group_by(Record.sensor_id)

    results = session.exec(statement)
    return [{"sensor_id": row[0], "average_level": row[1]} for row in results]


@analytics_router.get("/average/{region_id}", response_model=List[SensorAverageLevel])
async def get_average_trash_levels_of_all_sensors_in_region(region_id: int, session: SessionDep):
    """Get average trash levels for all sensors in a specific region"""
    from app.models.region import City

    subquery = select(Sensor.id).join(City).where(
        City.region_id == region_id).subquery()

    statement = select(
        Record.sensor_id,
        func.avg(Record.trash_level).label("average_level")
    ).where(
        Record.sensor_id.in_(select(subquery))
    ).group_by(Record.sensor_id)

    results = session.exec(statement)
    return [{"sensor_id": row[0], "average_level": row[1]} for row in results]
