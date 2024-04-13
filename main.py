import json


ACCOMMODATION_JSON_OBJECT_PATH = "accommodation/accommodation.json"
PILGRIM_JSON_OBJECT_PATH = "pilgrim/pilgrims.json"


def read_file(file_path):
    with open(file_path, "r") as f:
        data = json.load(f)
    return data


def write_file(data, file_path):
    with open(file_path, "w") as f:
        json.dump(data, f)


