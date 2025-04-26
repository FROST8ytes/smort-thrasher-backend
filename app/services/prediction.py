import os
import joblib
import pandas as pd
from sklearn.exceptions import NotFittedError
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

    def predict_full_level(
        self,
        sensor_id: int,
        latest_data: dict,
        threshold=95,
        step_minutes=30
    ) -> dict | None:
        if sensor_id not in self.models:
            raise ValueError(f"Model for sensor {sensor_id} is not loaded.")

        model = self.models.get(sensor_id)

        if model is None:
            raise NotFittedError(
                "Model not fitted. Call train_random_forest() first.")

        try:
            last_timestamp = latest_data['time_stamp']
            current_data = latest_data.copy()
            step = 0

            while True:
                future_time = last_timestamp + \
                    pd.Timedelta(minutes=(step + 1) * step_minutes)
                features = {
                    'hour': future_time.hour,
                    'day_of_week': future_time.dayofweek,
                    'month': future_time.month,
                    'is_weekend': int(future_time.dayofweek in [5, 6]),
                    'lag_1': current_data['trash_level'],
                    'lag_2': current_data['lag_1'],
                    'lag_3': current_data['lag_2']
                }

                pred = model.predict(pd.DataFrame([features]))[0]

                current_data['lag_3'] = current_data['lag_2']
                current_data['lag_2'] = current_data['lag_1']
                current_data['lag_1'] = pred
                current_data['trash_level'] = pred

                step += 1

                if pred >= threshold:
                    return {
                        'sensor_id': sensor_id,
                        'predicted_timestamp': future_time,
                        'hours_until_full': step * (step_minutes / 60),
                        'predicted_level': pred
                    }

        except Exception as e:
            raise ValueError(f"Error predicting full level: {str(e)}")


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
