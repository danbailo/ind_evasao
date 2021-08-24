import os

import pandas as pd
from mongoengine import connect
from mongoengine.connection import disconnect


def get_data_from_mongo():
    client = connect()
    database = client["ind_evasao"]
    answers = database["answer"]
    df = pd.DataFrame(list(answers.find()))
    disconnect()
    if os.path.isfile("../database.json"):
        os.remove("../database.json")
    df.to_json("database.json", indent=4)


if __name__ == "__main__":
    get_data_from_mongo()
