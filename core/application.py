from core import configuration, logger, network


class Application:

    VERSION = '0.2'
    SERVER_HOST = 'http://163.172.189.169'

    def __init__(self, argv):
        self.argv = argv
        self.configuration = None
        self.logger = logger.Logger()

    def print_head(self):
        print(' =================================')
        print('|         Miner Watch ' + self.VERSION + '         |')
        print('|                                 |')
        print('|       Creator: dekamaru         |')
        print(' =================================')
        print()

    def run(self):
        self.print_head()

        if len(self.argv) != 2:
            print('USAGE: minerwatch.exe SECRET_KEY')
            return -1

        # check internet connection
        if network.make_request(self.SERVER_HOST) is False:


        try:
            self.configuration = configuration.load()
        except configuration.NotFoundException:
            # need register
            pass



