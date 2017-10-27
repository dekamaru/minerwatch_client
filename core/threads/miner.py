import logging
import subprocess
from threading import Thread

from core.miners.miner_factory import MinerFactory
from core.message.thread_network import ThreadNetwork


class MinerThread(Thread):
    def __init__(self, application):
        Thread.__init__(self)
        self.app = application

    def run(self):
        miner = MinerFactory.create(int(self.app.configuration['type']))

        while True:
            cmd = miner.get_command(self.app.configuration)
            logging.info('Starting miner: ' + cmd)

            p = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
            p.wait()

            # todo: make api call and add timeout (maybe check return code?)
            logging.warning('Miner was crashed. Restart...')
