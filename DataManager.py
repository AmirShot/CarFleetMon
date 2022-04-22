import threading
import time
from proto1_pb2 import *


class DataManager:
    def __init__(self, connection_manager):
        self._updatePeriod = 10
        self._connectionManager = connection_manager
        self._running = True
        self._thread = threading.Thread(target=self.update)
        self._thread.start()

    def update(self):
        lock = threading.Lock()
        while self._running:
            lock.acquire()
            for cw in self._connectionManager.conWrap:

                print(f"cw: {cw}")
                car_data = CurrData()
                #print(f"type: {self._connectionManager.conWrap[cw].update(5)}")

                if self._connectionManager.conWrap[cw].is_active():
                    data = self._connectionManager.conWrap[cw].update(5)
                    print(f"data: {data}")
                    car_data.ParseFromString(data)
                    print("Trying to print CarData")
                    print(car_data)
            lock.release()
            time.sleep(11)










