from core.miners.base_miner import BaseMiner
from core.miners.miner_type import MinerType


class NoPing(BaseMiner):

    def get_data(self):
        pass

    def get_command(self, configuration):
        pass

    def get_type(self):
        return MinerType.NO_PING

    def get_name(self):
        return 'NOPING'