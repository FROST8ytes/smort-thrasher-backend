import joblib
import pandas as pd
import os
from typing import Dict, Optional
from database import Database

class SmortPredictor:
    def __init__(self, model_dir: str, sensor_ids: list):

        self.model_dir = model_dir
        self.sensors = sensor_ids
        self.models = self.load_models()

    def load_models(self) -> Dict[int, joblib]:
   
        models = {}
        for sensor_id in self.sensors:
            model_path = os.path.join(self.model_dir, f"sensor_{sensor_id}_model.joblib")
            if os.path.exists(model_path):
                models[sensor_id] = joblib.load(model_path)
            else:
                print(f"Warning: Model file not found for sensor {sensor_id}")
        return models

    def predict_full_level(self, sensor_id: int, latest_data: Dict) -> Optional[Dict]:
      
        if sensor_id not in self.models:
            raise ValueError(f"Model for sensor {sensor_id} is not loaded.")

        model = self.models[sensor_id]
        last_timestamp = latest_data['time_stamp']
        current_data = latest_data.copy()

        for step in range(672):  
            features = {
                'hour': (last_timestamp + pd.Timedelta(minutes=(step + 1) * 15)).hour,
                'day_of_week': (last_timestamp + pd.Timedelta(minutes=(step + 1) * 15)).dayofweek,
                'month': (last_timestamp + pd.Timedelta(minutes=(step + 1) * 15)).month,
                'is_weekend': int((last_timestamp + pd.Timedelta(minutes=(step + 1) * 15)).dayofweek in [5, 6]),
                'lag_1': current_data['trash_level'],
                'lag_2': current_data['lag_1'],
                'lag_3': current_data['lag_2']
            }

            pred = model.predict(pd.DataFrame([features]))[0]

            
            current_data['lag_3'] = current_data['lag_2']
            current_data['lag_2'] = current_data['lag_1']
            current_data['lag_1'] = pred
            current_data['trash_level'] = pred

            if pred >= 90:  
                predicted_time = last_timestamp + pd.Timedelta(minutes=(step + 1) * 15)
                return {
                    'sensor_id': sensor_id,
                    'predicted_timestamp': predicted_time,
                    'hours_until_full': (step + 1) * 0.25,
                    'predicted_level': pred
                }

        return None  

if __name__ == "__main__":
    model_directory = "ML-model"
    sensor_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9]  

    predictor = SmortPredictor(model_directory, sensor_ids)

    # Simulate new sensor data
    # latest_data = {
    #     'time_stamp': pd.Timestamp.now(),
    #     'trash_level': 70.0,  # Example current level
    #     'lag_1': 65.0,
    #     'lag_2': 60.0,
    #     'lag_3': 55.0
    # }

    # take from db 

    sensor_id = 9  # Example: Predict for sensor 9
    full_prediction = predictor.predict_full_level(sensor_id, latest_data)

    if full_prediction:
        print(f"Sensor {sensor_id} - Trash will be full at: {full_prediction['predicted_timestamp']}")
        print(f"Hours until full: {full_prediction['hours_until_full']}")
        print(f"Predicted level: {full_prediction['predicted_level']:.2f}%")
    else:
        print(f"Sensor {sensor_id} - No full-level prediction found within the next 7 days.")