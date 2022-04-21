from datetime import datetime
from EngineStats import EngineStats


class Connection:
    def __init__(self, log):
        self.log = open(log, "r")
        self.log.readline()     # skip header line

    def sample(self, e: EngineStats):
        try:
            s = self.log.readline()
            e.unpack(s)
            return e
        except:
            return False
