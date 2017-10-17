import time
import logging
from miners.miner_factory import MinerFactory


def observer_thread(app):
    miner = MinerFactory.create(int(app.configuration['type']))
    while True:
        status = app.protocol.ping(miner)
        if status == -1:
            # todo: need re-register
            app.miner_thread_process.kill()
            pass
        elif status is False:
            return
        else:
            logging.info('Ping success')
            time.sleep(10)

