from fastapi import FastAPI
import psycopg as pg 
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
