from miners.miner_factory import MinerFactory
import logging

def miner_thread(configuration, proto):

    miner = MinerFactory.create(int(configuration['type']))

    logging.info('Starting miner: ' + miner.get_command(configuration))
    while True:
        p = subprocess.Popen(cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)
        p.wait()
        log('MINER', 'Miner was crashed. Restart...')