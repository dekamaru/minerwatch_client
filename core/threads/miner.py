import logging
import subprocess
import configparser
import time
import os
from threading import Thread
from core.notify_type import NotifyType

from core.miners.miner_factory import MinerFactory


class MinerThread(Thread):

    CRASH_LIMIT = 3
    CRASH_TIMEOUT = 60

    def __init__(self, application):
        Thread.__init__(self)
        self.app = application
        self.lifetime = time.time()
        self.crash_count = 0

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

            # check crash count
            elapsed = time.time() - self.lifetime
            if elapsed < MinerThread.CRASH_TIMEOUT:
                self.crash_count += 1
            else:
                self.lifetime = time.time()
                self.crash_count = 1

            if self.crash_count == MinerThread.CRASH_LIMIT:
                logging.error('Miner crash limit reached')
                self.app.protocol.notify(NotifyType.MINER_CRASH_REBOOT)
                os.system("shutdown -t 0 -r -f") # make reboot
                return False
            else:
                logging.warning('Miner was crashed. Restart...')


