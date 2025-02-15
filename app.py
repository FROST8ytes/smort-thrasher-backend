from fastapi import FastAPI
import psycopg as pg 
from fastapi.responses import JSONResponse
app = FastAPI()

db = Database()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/sensor/{sensor_ID}")
async def get_sensor_record(sensor_ID: int):
    records = db.get_sensor_record(sensor_ID)
    return JSONResponse(content={"records": records})

    @app.post("/sensor")
    async def create_sensor_record(sensor_data: dict):
            #-----------------need to verify whether sensor data is coming from real sensor--------------
        db.save_sensor_record(sensor_data)
        return JSONResponse(content={"message": "Sensor data saved successfully"})