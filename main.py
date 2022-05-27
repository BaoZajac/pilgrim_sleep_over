import json


def read_db(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def write_db(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f)


