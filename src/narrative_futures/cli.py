from narrative_futures.utils import toml


def main():
    metadata = toml.load("pyproject.toml")
    print(metadata)
