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


def save(configuration):
    with open('miner.settings', 'w') as f:
        f.write(json.dumps(configuration))
