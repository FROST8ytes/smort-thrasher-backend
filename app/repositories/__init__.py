from .region_repository import RegionRepository, CityRepository
from .sensor_repository import SensorRepository
from .record_repository import RecordRepository

# Export instances for direct use
region_repo = RegionRepository()
city_repo = CityRepository()
sensor_repo = SensorRepository()
record_repo = RecordRepository()
