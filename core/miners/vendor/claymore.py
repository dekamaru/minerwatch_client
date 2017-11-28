import time
import requests
import logging
import re
import json
from core.miners.base_miner import BaseMiner
from core.miners.miner_type import MinerType


class Claymore(BaseMiner):

    def get_data(self):
        try:
            miner_data = requests.get('http://127.0.0.1:3333').text
        except Exception:
            logging.warning('Can\'t get miner data from API')
            return []


        json_data = re.search('({.*?})', miner_data)
        if json_data is not None:
            miner_data = json.loads(json_data.group(0))
        else:
            logging.warning('Can\'t get miner data json from api page')
            return []

        send_data = []

        speeds = miner_data['result'][3].split(';')
        temps = miner_data['result'][6].split(';')
        temps_iterator = 0
        gpu_id = 0
        for i in range(0, len(speeds)):
            send_data.append({
                'name': 'GPU ' + str(gpu_id),
                'temp': int(temps[temps_iterator]),
                'speed': int(speeds[i]) / 1000
            })

            temps_iterator += 2  # every second item is temp
            gpu_id += 1  # increase gpu id
        return send_data

    def get_command(self, configuration):
        password = '-epsw x'

        if configuration['password'] != '':
            password = '-epsw ' + configuration['password']
        # todo: platform-wide
        cmd = 'miner.exe -r -1 -epool %s:%s -ewal %s %s' % (
            configuration['host'],
            configuration['port'],
            configuration['username'],
            password
        )

        return cmd

    def get_type(self):
        return MinerType.CLAYMORE

    def get_name(self):
        return 'CLAYMORE'