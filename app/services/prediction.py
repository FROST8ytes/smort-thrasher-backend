import os
import joblib
import pandas as pd
from ..repositories import sensor_repo
from ..services.database import SessionDep


class SmortPredictor:
    def __init__(self, model_dir: str, sensor_ids: list[int]) -> None:
        self.model_dir: str = model_dir
        self.sensors: list[int] = sensor_ids
        self.models: dict[int, any] = self.load_models()

    def load_models(self) -> dict[int, any]:
        models = {}
        for sensor_id in self.sensors:
            model_path = os.path.join(
                self.model_dir, f"sensor_{sensor_id}_model.joblib")
            if os.path.exists(model_path):
                models[sensor_id] = joblib.load(model_path)
            else:
                print(f"Warning: Model file not found for sensor {sensor_id}")
        return models

    def predict_full_level(self, sensor_id: int, latest_data: dict) -> dict | None:
        if sensor_id not in self.models:
            raise ValueError(f"Model for sensor {sensor_id} is not loaded.")

        model = self.models[sensor_id]

        last_timestamp: pd.Timestamp = latest_data['time_stamp']
        current_data: dict = latest_data.copy()

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

            pred: float = model.predict(pd.DataFrame([features]))[0]

            current_data['lag_3'] = current_data['lag_2']
            current_data['lag_2'] = current_data['lag_1']
            current_data['lag_1'] = pred
            current_data['trash_level'] = pred

            if pred >= 90:
                predicted_time: pd.Timestamp = last_timestamp + \
                    pd.Timedelta(minutes=(step + 1) * 15)
                return {
                    'sensor_id': sensor_id,
                    'predicted_timestamp': predicted_time,
                    'hours_until_full': (step + 1) * 0.25,
                    'predicted_level': pred
                }

        return None


class SmortPredictorImplementor:
    def __init__(self, model_directory: str = "../ml_model", sensor_ids: list[int] = [1, 2, 3, 4, 5, 6, 7, 8, 9]) -> None:
        self.model_directory: str = model_directory
        self.sensor_ids: list[int] = sensor_ids
        self.predictor: SmortPredictor = SmortPredictor(
            self.model_directory, self.sensor_ids)

    async def predict_full_level(self, sensor_id: int, session: SessionDep) -> dict | None:
        latest_data = await sensor_repo.get_latest_sensor_records(
            session=session, sensor_id=sensor_id, limit=4)

        data: dict = {
            'time_stamp': pd.Timestamp(latest_data[0]['timestamp']),
            'trash_level': float(latest_data[0]['trash_level']),
            'lag_1': float(latest_data[1]['trash_level']),
            'lag_2': float(latest_data[2]['trash_level']),
            'lag_3': float(latest_data[3]['trash_level'])
        }

        return self.predictor.predict_full_level(sensor_id, data)


if __name__ == "__main__":
    obj = SmortPredictorImplementor()
    sensor_id = 9

    full_prediction = obj.predict_full_level(sensor_id)

    if full_prediction:
        print(
            f"Sensor {sensor_id} - Trash will be full at: {full_prediction['predicted_timestamp']}")
        print(f"Hours until full: {full_prediction['hours_until_full']}")
        print(f"Predicted level: {full_prediction['predicted_level']:.2f}%")
    else:
        print(
            f"Sensor {sensor_id} - No full-level prediction found within the next 7 days.")
