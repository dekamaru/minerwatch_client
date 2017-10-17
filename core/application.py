from core import configuration, network, protocol, system
from threads import miner, observer
import logging
import threading
import time


class Application:

    VERSION = '0.2'
    SERVER_HOST = 'http://163.172.189.169'

    def __init__(self, argv):
        self.argv = argv
        self.protocol = None
        self.configuration = None
        self.miner_thread_process = None
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] %(message)s',
                            datefmt='%d.%m.%Y %I:%M:%S')

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
        if not system.file_exists('miner.exe'):
            self.download_miner()  # download miner
        return True

    def run(self):
        self.print_head()

        if len(self.argv) != 2:
            logging.error('USAGE: minerwatch.exe SECRET_KEY')
            return -1

        # check internet connection
        if not self.check_connection():
            logging.error('No connection to Miner Watch server')
            return -1

        self.protocol = protocol.Protocol(self.SERVER_HOST, self.argv[1])  # init protocol

        integrity_status = self.run_integrity_check()
        if not integrity_status:
            return -1

        # RUN MINER THREAD
        miner_thread = threading.Thread(target=miner.miner_thread, args=(self,))
        miner_thread.start()

        time.sleep(10)
        # RUN OBSERVER THREAD
        observer_thread = threading.Thread(target=observer.observer_thread, args=(self,))
        observer_thread.start()

        observer_thread.join()
        logging.error('Observer thread are dead because error was occurred')
        return -1






