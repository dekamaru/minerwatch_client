from core import configuration, network, protocol, system
import logging


class Application:

    VERSION = '0.2'
    SERVER_HOST = 'http://163.172.189.169'

    def __init__(self, argv):
        self.argv = argv
        self.protocol = None
        self.configuration = None
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

        # save configuration or load
        try:
            self.configuration = configuration.load()
        except configuration.NotFoundException:
            logging.info('Started registration process')
            new_configuration = self.protocol.register_rig(self.VERSION, system.get_os_name(), system.get_mac_address())
            if new_configuration == -1:
                return -1
            else:
                logging.info('New configuration saved')
                configuration.save(new_configuration)
                self.configuration = configuration.load()  # reload new configuration

        print(self.configuration)





