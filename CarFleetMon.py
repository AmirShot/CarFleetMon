from DataManager import DataManager
from ConnectionManager import ConnectionManager

class CarFleetMon:
    def __init__(self):
        self._connection_manager = ConnectionManager("127.0.0.1")
        self._data_manager = DataManager(self._connection_manager)

if __name__ == "__main__":
    CFM = CarFleetMon()