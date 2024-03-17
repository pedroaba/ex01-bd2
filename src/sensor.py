from uuid import uuid4
from datetime import datetime

from pymongo.collection import Collection


class Sensor:
    def __init__(self, sensor_value: float, sensor_name: str = None, collection: Collection = None):
        if sensor_name is None:
            self.sensor_name = f"sensor-{uuid4()}"
        else:
            self.sensor_name = sensor_name

        value = {"value": sensor_value, "readAt": datetime.now().timestamp()}
        self.sensor_value = collection.find_one({"nomeSensor": self.sensor_name}, {"valorSensor": 1})
        if self.sensor_value is None:
            self.sensor_value = [value]
        else:
            self.sensor_value = self.sensor_value["valorSensor"]
            self.sensor_value.append(value)
        self.is_alarmed = False if sensor_value < 38 else True
        self.unit = "C°"
        self.created_at = datetime.now().timestamp()

    def to_dict(self):
        return {
            "nomeSensor": self.sensor_name,
            "valorSensor": self.sensor_value,
            "unidadeMedida": self.unit,
            "sensorAlarmado": self.is_alarmed,
            "createdAt": self.created_at
        }
