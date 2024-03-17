import random
import threading
import time
import datetime

from pymongo.collection import Collection

from src.graphic import Graphic
from src.sensor import Sensor


DEBUG = False


class Thread(threading.Thread):
    def __init__(self, collection: Collection, sensor_name: str):
        super(Thread, self).__init__()
        self.kill = threading.Event()
        self.collection = collection

        self._thread_sensor_name = sensor_name
        self._show_warning = False
        self._control_date = datetime.datetime.now()
        self._graphic_generator = Graphic(collection)

    def run(self):
        while not self.kill.is_set():
            time.sleep(self._get_interval())
            self._generate_graph()

            if self._show_warning:
                print(f"Atenção! Temperatura muito alta! Verificar Sensor {self._thread_sensor_name}!")
                continue

            sensor_value = self._get_sensor_value()

            sensor = Sensor(sensor_value, self._thread_sensor_name, self.collection)
            self._thread_sensor_name = sensor.sensor_name
            print(f"Sensor '{self._thread_sensor_name}' value: {sensor_value:.2f}")

            if sensor.sensor_value[-1]["value"] >= 38:
                self._show_warning = True

            result = self.collection.update_one(
                {
                    "nomeSensor": sensor.sensor_name
                },
                {
                    "$set": {
                        "valorSensor": sensor.sensor_value,
                        "sensorAlarmado": sensor.is_alarmed,
                        "unidadeMedida": sensor.unit
                    }
                },
                upsert=True
            )
            if not result.acknowledged:
                print(f"Sensor {sensor.sensor_name} with value {sensor_value} did not inserted")

    def stop(self):
        self.kill.set()

    def stopped(self):
        return self.kill.is_set()

    @staticmethod
    def _get_interval():
        return random.uniform(0.1, 3)

    @staticmethod
    def _get_sensor_value():
        return random.uniform(30, 40)

    def _generate_graph(self):
        now = datetime.datetime.now()
        difference = now - self._control_date
        difference_in_minutes = difference.total_seconds() / 60

        minutes_to_compare = 60 if DEBUG else 0.01
        if difference_in_minutes > minutes_to_compare:
            self._graphic_generator.generate_graph(self._thread_sensor_name)
            self._control_date = datetime.datetime.now()
