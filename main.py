import json


def read_db():
    with open("noclegi.json", "r") as f:
        data = json.load(f)
    return data


def write_db(data):
    with open("noclegi.json", "w") as f:
        json.dump(data, f)

