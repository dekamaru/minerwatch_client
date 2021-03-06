import time
import requests
import logging
from core.miners.base_miner import BaseMiner
from core.miners.miner_type import MinerType


class EWBF(BaseMiner):

    def get_data(self):
        try:
            miner_data = requests.get('http://127.0.0.1:25000/getstat').json()
        except Exception:
            logging.warning('Can\'t get miner data from API')
            return []
        passed_secs = int(time.time()) - int(miner_data['start_time'])
        send_data = []
        # prevent send zero values on miner start
        if passed_secs > 60:
            for gpu in miner_data['result']:
                send_data.append({
                    'name': gpu['name'],
                    'temp': gpu['temperature'],
                    'speed': gpu['speed_sps']
                })
        return send_data

    def get_command(self, configuration):
        password = ''

        if configuration['password'] != '':
            password = '--pass ' + configuration['password']
        # todo: platform-wide
        cmd = 'miner.exe --server %s --port %s --user %s --api 0.0.0.0:25000 %s' % (
            configuration['host'],
            configuration['port'],
            configuration['username'],
            password
        )

        return cmd

    def get_type(self):
        return MinerType.EWBF

    def get_name(self):
        return 'EWBF'