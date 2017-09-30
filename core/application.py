from core import configuration, network
import logging


class Application:

    VERSION = '0.2'
    SERVER_HOST = 'http://163.172.189.169'

    def __init__(self, argv):
        self.argv = argv
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

        try:
            self.configuration = configuration.load()
        except configuration.NotFoundException:
            # need register
            pass



