import json


def load(fp: str):
    data = None
    with open(fp, "r") as f:
        data = json.load(f)
    return data


def dump(fp, data):
    with open(fp, "w") as f:
        json.dump(data, f, indent=2)
