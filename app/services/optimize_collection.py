import json
from datetime import datetime, timedelta
from typing import Optional

from .prediction import SmortPredictorImplementor
from .env import GOOGLE_MAPS_API_KEY
from .maps_router import MapsRouter
from ..repositories import region_repo

CONFIDENCE_THRESHOLD = 0.75
BUFFER_HOURS = 0.2


async def get_sensors_for_collection(
    session,
    frequency_hours: int,
    start_time: datetime,
    region_id: int,
    refered_date: datetime = datetime.now()
) -> list[dict]:
    """
    Returns bins that will be full before next scheduled collection.
    """
    sensors_for_collection = []
    predictor = SmortPredictorImplementor()

    sensors = await region_repo.get_region_sensors(session=session, region_id=region_id)
    print(f"sensors: {sensors}")

    for sensor in sensors:
        sensor_id = sensor.id
        latitude = sensor.latitude
        longitude = sensor.longitude

    next_collection_time = start_time

    if next_collection_time < refered_date:
        diff_hours = (
            refered_date - next_collection_time).total_seconds() / 3600
        skips = (diff_hours // frequency_hours) + 1
        next_collection_time += timedelta(
            hours=skips * frequency_hours)

    print(next_collection_time)
    prediction = await predictor.predict_full_level(session=session, sensor_id=sensor_id)
    if prediction:
        hours_until_full = prediction["hours_until_full"]
        time_full = refered_date + timedelta(hours=hours_until_full)
        print(f"Sensor {sensor_id} will be full at {time_full} ",
              f"which is {hours_until_full:.2f} hours away.")

        adjusted_time_full = time_full - timedelta(hours=BUFFER_HOURS)

        print(
            "adjusted_time_full: {adjusted_time_full} , next_collection : {next_collection_time}")
        if adjusted_time_full <= next_collection_time:
            sensors_for_collection.append({
                "id": sensor_id,
                "latitude": latitude,
                "longitude": longitude
            })
    else:
        print(
            f"Warning: No prediction for sensor {sensor_id}. Skipping.")

    return sensors_for_collection


async def generate_optimized_route(sensors: list[dict], origin: str) -> Optional[str]:
    """
    Generate an optimized multi-stop Google Maps URL from selected sensors.
    """
    if not sensors:
        return None

    route_optimizer = MapsRouter(GOOGLE_MAPS_API_KEY)

    coordinates_json = json.dumps([
        {"latitude": float(s["latitude"]), "longitude": float(s["longitude"])}
        for s in sensors
    ])

    optimized_json = route_optimizer.sorting_waypoints(
        coordinates_json, origin,
        EmissionRatePerKM=0.1, FuelConsumptionRatePerKM=0.1
    )

    final_url = route_optimizer.generate_multi_stop_url(optimized_json, origin)
    return final_url


async def run(session, frequency_hours: int, start_time_str: str, origin: str, region_id: int, refered_date_str: str):
    """
    wrapper for all process to get the final linke 
    """
    try:
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        refered_date = datetime.strptime(refered_date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        print(
            f"Error: Invalid date format: {e}. Use YYYY-MM-DD HH:MM:SS format.")
        return

    sensors_to_collect = await get_sensors_for_collection(
        session, frequency_hours, start_time, region_id, refered_date
    )

    if sensors_to_collect:
        print(f"Sensors needing collection in region {region_id}:")
        for s in sensors_to_collect:
            print(f" - ID {s['id']}: ({s['latitude']}, {s['longitude']})")

        route_url = await generate_optimized_route(sensors_to_collect, origin)

        if route_url:
            print("\nOptimized Google Maps Route URL:")
            print(route_url)

            return route_url
        else:
            print("\nError: Could not generate route.")
    else:
        print("\nNo bins require urgent collection at this time.")

    return None
