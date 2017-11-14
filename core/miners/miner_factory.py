from core.miners.vendor import ewbf, noping, claymore
from core.miners.miner_type import MinerType


class NotImplementedMiner(Exception):
    pass


class MinerFactory:

    @staticmethod
    def create(m_type):
        if m_type == MinerType.EWBF:
            return ewbf.EWBF()
        elif m_type == MinerType.NO_PING:
            return noping.NoPing()
        elif m_type == MinerType.CLAYMORE:
            return claymore.Claymore()
        else:
            raise NotImplementedMiner
