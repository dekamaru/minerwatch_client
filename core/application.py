import logging

from core import configuration, network, protocol, system
from core.threads import miner, observer
from core.miners.miner_type import MinerType
import configparser


class Application:

    VERSION = '1.1'

    def __init__(self, argv):

        self.need_stop = False

        self.argv = argv
        self.protocol = None
        self.configuration = None
        self.system_configuration = None
        self.SERVER_HOST = None
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s',
                            datefmt='%d.%m.%Y %I:%M:%S')

    def load_system_configuration(self):
        config = configparser.ConfigParser()
        if not system.file_exists('config.ini'):
            return False
        config.read('config.ini')
        try:
            self.SERVER_HOST = config.get('API', 'host')
        except configparser.NoOptionError:
            return False

        self.system_configuration = config

    def print_head(self):
        print(' =================================')
        print('|         Miner Watch ' + self.VERSION + '         |')
        print('|                                 |')
        print('|       Creator: dekamaru         |')
        print(' =================================')
        print()

    def check_connection(self):
        try:
            network.make_request(self.SERVER_HOST)
        except network.NoInternetConnection:
            return False
        return True

    def download_miner(self):
        logging.info('Downloading miner')
        miner_file = self.protocol.get_miner_file(self.configuration['type'])
        with open("miner.zip", "wb") as code:
            code.write(miner_file)
        system.extract_archive('miner.zip')

    def run_integrity_check(self):
        # first: check the configuration
        try:
            self.configuration = configuration.load()
        except configuration.NotFoundException:
            new_configuration = self.protocol.register_rig(self.VERSION, system.get_os_name(), system.get_mac_address())
            if new_configuration == -1:
                return False
            else:
                logging.info('New configuration saved')
                configuration.save(new_configuration)
                self.configuration = configuration.load()  # reload new configuration

        # second: check miner file
        # todo: make this platform-wide
        if not system.file_exists('miner.exe') and int(self.configuration['type']) != MinerType.NO_PING:
            self.download_miner()  # download miner
        return True

    def run(self):
        self.print_head()

        if len(self.argv) != 2:
            logging.error('USAGE: minerwatch.exe SECRET_KEY')
            return -1

        status = self.load_system_configuration()
        if status is False:
            logging.error('Config file "config.ini" not exists or broken')
            return -1

        # check internet connection
        if not self.check_connection():
            logging.error('No connection to Miner Watch server')
            return -1

        self.protocol = protocol.Protocol(self.SERVER_HOST, self.argv[1])  # init protocol

        integrity_status = self.run_integrity_check()
        if not integrity_status:
            return -1

        if int(self.configuration['type']) != MinerType.NO_PING:
            miner_thread = miner.MinerThread(self)
            observer_thread = observer.ObserverThread(self)
            miner_thread.start()
            observer_thread.start()
        else:
            logging.info('No ping miner selected. Miner thread don\'t start')
            observer_thread = observer.ObserverThread(self)
            observer_thread.start()

        while not self.need_stop:
            if not observer_thread.is_alive():
                logging.error('Observer thread is dead')
                self.need_stop = True

            if int(self.configuration['type']) != MinerType.NO_PING and not miner_thread.is_alive():
                logging.error('Miner thread is dead')
                self.need_stop = True

        return -1






