from pathlib import Path
import json


class NotFoundException(Exception):
    pass


def load():
    configuration = Path("miner.settings")
    if not configuration.is_file():
        raise NotFoundException

    with open("miner.settings") as f:
        configuration = json.loads(f.read())
    return configuration
