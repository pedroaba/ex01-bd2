import atexit

from pymongo import MongoClient

from src.thread import Thread


client = MongoClient('localhost', 64000)
database = client['bancoiot']
collection = database['sensores']

threads = [
    Thread(collection, "sensor-01"),
    Thread(collection, "sensor-02"),
    Thread(collection, "sensor-03")
]


def close_all_threads():
    for thread in threads:
        if not thread.stopped():
            thread.stop()


atexit.register(close_all_threads)
for _t in threads:
    _t.start()
