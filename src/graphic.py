import uuid
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
from pymongo.collection import Collection


class Graphic:
    def __init__(self, collection: Collection):
        self.collection = collection

    def generate_graph(self, sensor_name: str):
        print("Gerando gráfico")

        sensors = self.collection.find({}, {"nomeSensor": 1})
        dataframe = pd.DataFrame(data=sensors)

        labels = dataframe["nomeSensor"].drop_duplicates().to_list()

        plt.figure(str(uuid.uuid4()))
        plt.ylabel("Temperatura [Celcius]")
        plt.xlabel("Tempo [Timestamp]")

        now = datetime.now()
        timestamp_now = now.timestamp()
        timestamp_one_hour_past = (now - timedelta(minutes=1)).timestamp()

        for label in labels:
            data = self.collection.find_one({
                "nomeSensor": label,
                # "valorSensor.readAt": {
                #     "$gte": timestamp_one_hour_past,
                #     "$lt": timestamp_now
                # }
            }, {"valorSensor": 1})

            dataframe = pd.DataFrame(data=data["valorSensor"])
            dataframe = dataframe.loc[
                (dataframe["readAt"] >= timestamp_one_hour_past) &
                (dataframe["readAt"] < timestamp_now)
            ]

            max_temp = dataframe["value"].max()
            min_temp = dataframe["value"].min()

            values = dataframe["value"]

            print(values.shape)

            plt.plot(values.to_list(),  label=label)
            plt.yticks(range(int(min_temp), int(max_temp)))
        plt.legend()
        plt.savefig(f"Gráfico-{uuid.uuid4()}.png")
