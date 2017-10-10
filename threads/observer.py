import time


def observer_thread(proto):
    while True:
        proto.ping()
        time.sleep(300)
