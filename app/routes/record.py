from fastapi import APIRouter, HTTPException, Depends
from ..services.database import SessionDep
from ..repositories import record_repo
from ..models.record import Record

record_router = APIRouter(
    prefix="/record",
    tags=["Records"],
)


tag_metadata = {
    "name": "Records",
    "description": "Operations with trash level records",
}


@record_router.post("/", response_model=Record)
async def create_sensor_record(record: Record, session: SessionDep):
    try:
        result = await record_repo.create(session, record)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=422, detail=f"Failed to create record: {str(e)}")
