from miners.miner_factory import MinerFactory
import logging
import subprocess


def miner_thread(app):
    miner = MinerFactory.create(int(app.configuration['type']))

    while True:
        cmd = miner.get_command(app.configuration)
        logging.info('Starting miner: ' + cmd)

        p = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        app.miner_thread_process = p
        p.wait()

        # todo: make api call and add timeout (maybe check return code?)
        logging.warning('Miner was crashed. Restart...')