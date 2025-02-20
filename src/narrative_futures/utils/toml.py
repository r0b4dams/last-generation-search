import tomllib


def load(fp: str):
    data = None
    with open(fp, "rb") as f:
        data = tomllib.load(f)
    return data
