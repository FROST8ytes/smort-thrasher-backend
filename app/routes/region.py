from fastapi import APIRouter, HTTPException
from typing import List
from ..services.database import SessionDep
from ..repositories import region_repo, city_repo
from ..models import Region, City
from ..models.response_models import RegionWithCities, RegionWithSensors, CityWithSensors

region_router = APIRouter(
    prefix="/region",
    tags=["Regions"],
)

tag_metadata = {
    "name": "Regions",
    "description": "Operations with regions and cities",
}


@region_router.get("/", response_model=List[Region])
async def get_regions(session: SessionDep):
    """Get all regions"""
    regions = await region_repo.get_all(session)
    return regions


@region_router.get("/with-cities", response_model=List[RegionWithCities])
async def get_regions_with_cities(session: SessionDep):
    """Get all regions with their associated cities"""
    regions = await region_repo.get_regions_with_cities(session)
    return regions


@region_router.get("/with-sensors", response_model=List[RegionWithSensors])
async def get_regions_with_sensors(session: SessionDep):
    """Get all regions with their sensors"""
    regions = await region_repo.get_regions_with_sensors(session)
    return regions


@region_router.get("/search", response_model=Region)
async def search_region_by_name(name: str, session: SessionDep):
    """Search for a region by name"""
    region = await region_repo.get_by_name(session, name)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    return region


@region_router.get("/{region_id}", response_model=Region)
async def get_region(region_id: int, session: SessionDep):
    """Get a region by ID"""
    region = await region_repo.get_by_id(session, region_id)
    if not region:
        raise HTTPException(status_code=404, detail="Region not found")
    return region


@region_router.get("/{region_id}/cities", response_model=list[City])
async def get_cities_by_region(region_id: int, session: SessionDep):
    """Get all cities in a region"""
    cities = await city_repo.get_cities_by_region(session, region_id)
    return cities


@region_router.get("/city/{city_id}", response_model=City)
async def get_city(city_id: int, session: SessionDep):
    """Get a city by ID"""
    city = await city_repo.get_by_id(session, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city


@region_router.get("/city/{city_id}/with-sensors", response_model=CityWithSensors)
async def get_city_with_sensors(city_id: int, session: SessionDep):
    """Get a city with all its sensors"""
    city = await city_repo.get_city_with_sensors(session, city_id)
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city
