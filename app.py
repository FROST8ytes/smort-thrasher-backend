from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from components.database import Database
from os import getenv
from dotenv import load_dotenv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()

db = Database(getenv("DB_HOST"), getenv("DB_PORT"), getenv(
    "DB_USER"), getenv("DB_PASSWORD"), getenv("DB_NAME"))


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/region")
async def get_regions():
    regions = await db.get_regions()
    return regions


@app.get("/region/{region_ID}/sensors")
async def get_region_sensors(region_ID: int):
    sensors = await db.get_region_sensors(region_ID)
    return sensors


@app.post("/sensor")
async def add_sensor(data: dict):
    status = await db.add_sensor(**data)
    if not status:
        return HTTPException(status_code=422, detail="Maybe the JSON data is wrong...")
    return status


@app.get("/sensor/{sensor_ID}")
async def get_sensor(sensor_ID: int):
    sensor = await db.get_sensor(sensor_ID)
    return sensor


@app.get("/sensor/{sensor_ID}/records")
async def get_sensor_records(sensor_ID: int):
    records = await db.get_sensor_records(sensor_ID)
    return records


@app.post("/record")
async def create_sensor_record(sensor_data: dict):
    status = await db.add_sensor_record(**sensor_data)
    if not status:
        return HTTPException(status_code=422, detail="Maybe the JSON data is wrong...")
    return status
