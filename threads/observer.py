import time
import logging


def observer_thread(proto):
    while True:
        status = proto.ping()
        if status == -1:
            # todo: need re-register
            pass
        elif status is False:
            return
        else:
            logging.info('Ping success')
            time.sleep(300)
