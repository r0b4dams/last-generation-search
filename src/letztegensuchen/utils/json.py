import json


def load_json(fp):
    data = None
    with open(fp, "r") as f:
        data = json.load(f)
    return data


def save_json(fp, data):
    with open(fp, "w") as f:
        json.dump(data, f, indent=2)
