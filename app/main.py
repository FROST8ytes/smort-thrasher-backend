import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from .routes import *
from .models.response_models import SensorPredictTrashLevel
from .services.database import SessionDep
from .services.prediction import SmortPredictorImplementor
from .services import optimize_collection
from .models.request_models import DriverLocationInput
from .models.response_models import OptimizationResponse

tags_metadata = [
    region_tag_metadata,
    sensor_tag_metadata,
    record_tag_metadata,
    analytics_tag_metadata
]

app = FastAPI(
    title="SMORT REST API",
    description="SMORT REST API for Web and Mobile.",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in (region_router, sensor_router, record_router, analytics_router):
    app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/predict/{sensor_id}", response_model=SensorPredictTrashLevel)
async def predict(sensor_id: int, session: SessionDep):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_DIR = os.path.join(BASE_DIR, "app/ml_model")
    print(f"[+] Model Directory: {MODEL_DIR}")
    predictor = SmortPredictorImplementor(model_directory=MODEL_DIR)
    prediction = await predictor.predict_full_level(sensor_id, session)

    return prediction


@app.post("/driverLocation", response_model=OptimizationResponse)
async def add_driver_location(data: DriverLocationInput, session: SessionDep):
    """
    Input JSON should be like:
    {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "region_id": 1
    }

    Response example:
    {
        "status": "400",
        "message": "https://maps/link/api ............"
    }
    """
    frequency = 24  # hours
    start_time_string = "2024-01-01 08:00:00"

    # Corrected to use the fields properly
    collection_origin = f"{data.latitude},{data.longitude}"

    refered_date_string = "2025-04-26 22:00:00"

    target_region_id = data.region_id

    try:
        link = await optimize_collection.run(session, frequency, start_time_string, collection_origin, target_region_id, refered_date_string)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return {
        "status": "200",
        "message": link
    }
