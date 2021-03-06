import logging
import time
from threading import Thread

from core.miners.miner_factory import MinerFactory
from core.notify_type import NotifyType


class ObserverThread(Thread):

    COLLECTIONS_COUNT = 5
    COLLECT_TIME = 60

    def __init__(self, application):
        Thread.__init__(self)
        self.app = application
        self.collections_data = []

    def run(self):
        miner = MinerFactory.create(int(self.app.configuration['type']))
        while True:
            if len(self.collections_data) == ObserverThread.COLLECTIONS_COUNT:
                status = self.app.protocol.ping(self.collections_data)
                if status == -1:
                    logging.error('API returned -1 (need register)')
                    # configuration.delete()
                    return
                elif status is False:
                    logging.error('API error')
                    return
                else:
                    logging.info('Ping success')
                self.collections_data = []
            else:
                self.collections_data.append(miner.get_data())
                if self.app.start_notified is False and len(self.collections_data) == 2:
                    self.app.protocol.notify(NotifyType.MINER_STARTED_SUCCESSFULLY)
                    self.app.start_notified = True
                logging.info('Collected miner data ' + str(len(self.collections_data)) + '/' + str(int(ObserverThread.COLLECTIONS_COUNT)))
            time.sleep(ObserverThread.COLLECT_TIME)