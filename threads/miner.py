from miners.miner_factory import MinerFactory
import logging
import subprocess


def miner_thread(configuration, proto):
    miner = MinerFactory.create(int(configuration['type']))
    cmd = miner.get_command(configuration)

    logging.info('Starting miner: ' + cmd)
    while True:
        p = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        p.wait()
        # todo: make api call and add timeout (maybe check return code?)
        logging.warning('Miner was crashed. Restart...')