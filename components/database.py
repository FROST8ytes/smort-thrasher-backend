import psycopg2 as pg 
from datetime import datetime



class Database:
    def __init__(self):
        self.connection = pg.connect(
            dbname="smort",
            user="postgres",
            password="",
            host="localhost",
            port="5432"

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

    def add_sensor_record(self, sensor_ID: int, trash_level: str, image_64bit_encoded: str) -> bool:
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query = """
            INSERT INTO sensor_record (smort_ID, trash_level, time_stamp, image)
            VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (sensor_ID, trash_level, timestamp, pg.Binary(image_64bit_encoded)))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
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
    
    def update_sensor_info(self, ID: int, latitude: str = None, longitude: str = None, name: str = None) -> bool:
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
