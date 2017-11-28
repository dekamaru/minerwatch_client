import json
import logging
import socket
from core.miners.base_miner import BaseMiner
from core.miners.miner_type import MinerType


class DSTM(BaseMiner):

    def get_data(self):

        send_data = []
        sock = socket.socket()
        try:
            sock.connect(('127.0.0.1', 2222))
            sock.send(('{"id":1, "method":"getstat"}').encode('utf-8'))
            data = sock.recv(4096)
            sock.close()
        except ConnectionError:
            logging.warning('Can\'t get miner data from API')
            return send_data

        telemetry = json.loads(data.decode('utf-8'))
        if int(telemetry['uptime']) > 60:
            for gpu in telemetry['result']:
                send_data.append({
                    'name': 'GPU ' + str(gpu['gpu_id']),
                    'temp': gpu['temperature'],
                    'speed': gpu['sol_ps']
                })
        return send_data

    def get_command(self, configuration):
        password = ''

        if configuration['password'] != '':
            password = '--pass ' + configuration['password']
        # todo: platform-wide
        cmd = 'miner.exe --telemetry=0.0.0.0:2222 --server %s --port %s --user %s %s' % (
            configuration['host'],
            configuration['port'],
            configuration['username'],
            password
        )

        return cmd

    def get_type(self):
        return MinerType.DSTM

    def get_name(self):
        return 'DSTM'
