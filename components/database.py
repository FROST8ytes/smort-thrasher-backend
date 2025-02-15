import psycopg2 as pg
from datetime import datetime
from decimal import Decimal
from os import getenv


class Database:
    def __init__(self, host: str, port: str, user: str, password: str, dbname: str):
        self.connection = pg.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port

        )
        self.cursor = self.connection.cursor()

    def check_connection(self) -> bool:
        try:
            self.cursor.execute("SELECT version();")
            record = self.cursor.fetchone()
            print("You are connected to - ", record, "\n")
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

    def close_connection(self):
        if self.connection:
            self.cursor.close()
            print("PostgreSQL connection is closed")
            self.connection.close()

    async def get_regions(self) -> list:
        try:
            query = "SELECT * FROM region"
            self.cursor.execute(query)
            regions = self.cursor.fetchall()
            return regions
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    async def get_region_sensors(self, region_ID: int) -> list:
        try:
            query = "SELECT id, latitude, longitude, name FROM region_sensor INNER JOIN sensor s on s.id = region_sensor.sensor_id WHERE region_id = %s"
            self.cursor.execute(query, (region_ID,))
            sensors = self.cursor.fetchall()
            return sensors
        except Exception as e:
            print(f"An error occured: {e}")
            return []

    async def add_sensor(self, latitude: float, longitude: float, name: str, region_ID: int) -> bool:
        try:
            query = "INSERT INTO sensor (latitude, longitude, name) VALUES (%s, %s, %s) RETURNING ID"
            self.cursor.execute(query, (latitude, longitude, name))
            sensor_id = self.cursor.fetchone()[0]
            print(f"[+] Inserted new sensor with ID: {sensor_id}")

            query = "INSERT INTO region_sensor (region_ID, sensor_ID) VALUES (%s, %s)"
            self.cursor.execute(query, (region_ID, sensor_id))

            self.connection.commit()
            return True
        except Exception as e:
            print(f"An error occured: {e}")
            self.connection.rollback()
            return False

    def get_sensor_record(self, sensor_ID: int) -> list:
        try:
            query = """
            SELECT * FROM sensor_record WHERE smort_ID = %s
            """
            self.cursor.execute(query, (sensor_ID,))
            records = self.cursor.fetchall()
            return records
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    # only for ML section
    def get_partial_sensor_record(self, sensor_ID: int) -> list:
        try:
            query = """
            SELECT smort_ID, time_stamp, trash_level FROM sensor_record WHERE smort_ID = %s
            """
            self.cursor.execute(query, (sensor_ID,))
            records = self.cursor.fetchall()
            return records
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def get_latest_sensor_record(self, sensor_ID: int) -> list:
        try:
            query = """
            SELECT smort_ID, time_stamp, trash_level 
            FROM sensor_record 
            WHERE smort_ID = %s 
            ORDER BY time_stamp DESC 
            LIMIT 1
            """
            self.cursor.execute(query, (sensor_ID,))
            record = self.cursor.fetchone()  
            return [record] if record else [] 
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def get_sensor(self, ID:int) -> dict:
        try:
            query = """
            SELECT * FROM sensor WHERE ID = %s
            """
            self.cursor.execute(query, (ID,))
            sensor = self.cursor.fetchone()
            return sensor
        except Exception as e:
            print(f"An error occurred: {e}")
            return {}

    async def update_sensor(self, ID: int, latitude: float = None, longitude: float = None, name: str = None) -> bool:
        try:
            updates = []
            params = []
            if latitude is not None:
                updates.append("latitude = %s")
                params.append(latitude)
            if longitude is not None:
                updates.append("longitude = %s")
                params.append(longitude)
            if name is not None:
                updates.append("name = %s")
                params.append(name)

            if not updates:
                print("No values provided to update.")
                return False

            query = f"UPDATE sensor SET {', '.join(updates)} WHERE ID = %s"
            params.append(ID)
            self.cursor.execute(query, tuple(params))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()
            return False

    async def add_sensor_record(self, sensor_ID: int, trash_level: float, image_base64: str) -> bool:
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = """
            INSERT INTO sensor_record (smort_ID, trash_level, time_stamp, image)
            VALUES (%s, %s, %s, %s)
            """
            print(f"[*] Executing add_sensor_record")
            self.cursor.execute(
                query, (sensor_ID, trash_level, timestamp, image_base64))
            print(f"[*] Executed add_sensor_record")
            self.connection.commit()
            print(f"[+] Committed changes.")
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            self.connection.rollback()
            return False

    async def get_sensor_records(self, sensor_ID: int) -> list:
        try:
            query = """
            SELECT * FROM sensor_record WHERE smort_ID = %s
            """
            self.cursor.execute(query, (sensor_ID,))
            records = self.cursor.fetchall()
            return records
        except Exception as e:
            print(f"An error occurred: {e}")
            return []


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()

    db = Database(getenv("DB_HOST"), getenv("DB_PORT"), getenv(
        "DB_USER"), getenv("DB_PASSWORD"), getenv("DB_NAME"))
    db.check_connection()

    dataRow = db.get_sensor_record(1)
    print(dataRow)

    db.close_connection()
