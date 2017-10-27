from miners.vendor import ewbf

from core.miners.miner_type import MinerType


class NotImplementedMiner(Exception):
    pass


class MinerFactory:

    @staticmethod
    def create(m_type):
        if m_type == MinerType.EWBF:
            return ewbf.EWBF()
        else:
            raise NotImplementedMiner
