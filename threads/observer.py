import time
import logging
from miners.miner_factory import MinerFactory
from threading import Thread


class ObserverThread(Thread):
    def __init__(self, application):
        Thread.__init__(self)
        self.app = application

    def run(self):
        miner = MinerFactory.create(int(self.app.configuration['type']))
        while True:
            status = self.app.protocol.ping(miner)
            if status == -1:
                # configuration.delete()
                return
            elif status is False:
                return
            else:
                logging.info('Ping success')
                time.sleep(10)
