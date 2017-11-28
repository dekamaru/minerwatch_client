import logging
import subprocess
import configparser
from threading import Thread

from core.miners.miner_factory import MinerFactory
from core.miners.miner_type import MinerType


class MinerThread(Thread):
    def __init__(self, application):
        Thread.__init__(self)
        self.app = application

    def run(self):
        miner = MinerFactory.create(int(self.app.configuration['type']))

        while True:
            cmd = miner.get_command(self.app.configuration)

            try:
                additional_params = self.app.system_configuration.get(miner.get_name(), 'additional_params')
            except configparser.Error:
                additional_params = ''

            cmd += ' ' + additional_params

            logging.info('Starting miner: ' + cmd)

            p = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
            p.wait()

            # todo: make api call and add timeout (maybe check return code?)
            logging.warning('Miner was crashed. Restart...')
