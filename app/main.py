from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import *

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


# @app.get("/predict/{sensor_id}")
# async def predict(sensor_id: int):
#     predictor = smortPredictorImplementor(model_directory="./ML-model")
#     prediction = await predictor.predict_full_level(sensor_id)

#     return prediction
