import threading
import time
from proto1_pb2 import *
from SQL_ORM import *


class DataManager:
    def __init__(self, connection_manager):
        self._active_connections = dict()
        self._updatePeriod = 10
        self._connectionManager = connection_manager
        self._running = True
        self._thread = threading.Thread(target=self.update)
        self._thread.start()
        self._sql_orm = SQL_ORM(".")

    def new_connection(self, id: str):
        self._active_connections[id] = True

    def init_connections(self):
        for cw in self._active_connections:
            self._active_connections[cw] = False

    def close_connection(self, id: str):
        self._active_connections.pop(id)


    def update(self):
        lock = threading.Lock()
        while self._running:
            lock.acquire()
            self.init_connections()
            for cw in self._connectionManager.conWrap:
                car_data = CurrData()
                if not cw in self._active_connections:
                    self.new_connection(cw)
                if self._connectionManager.conWrap[cw].is_active():
                    data = self._connectionManager.conWrap[cw].update(5)
                    car_data.ParseFromString(data)
                    self._sql_orm.message(car_data)
            for cw in self._active_connections:
                if not self._active_connections[cw]:
                    self.close_connection(cw)

            lock.release()
            time.sleep(1)











