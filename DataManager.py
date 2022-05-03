import threading
import time
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
        print(f"--------------creating a new connection {id}------------------")
        self._active_connections[id] = True
        self._sql_orm.create_connection(id)

    def close_connection(self, id: str):
        print(f"--------------closing a connection {id}------------------")
        self._active_connections.pop(id)
        self._sql_orm.close_connection(id)

    def update(self):
        lock = threading.Lock()
        while self._running:
            # clean active connection statuses
            for cw in self._active_connections:
                self._active_connections[cw] = False

            #
            active_connections = self._connectionManager.conWrap.copy()
            for cw in active_connections:
                if active_connections[cw].is_active():
                    if cw not in self._active_connections:
                        self.new_connection(cw)
                    data = self._connectionManager.conWrap[cw].update(5)
                    self._active_connections[cw] = True
                    self._sql_orm.message(data)

            active_connections = self._active_connections.copy()
            for cw in active_connections:
                if not self._active_connections[cw]:
                    self.close_connection(cw)
            time.sleep(5)

    def activateLiveConnection(self, LicencePlate:str):
        try:
            print(f"Licence Plate = {LicencePlate}")
            print("Checking if the connection is Alive")
            print(f"Active Connections = {self._active_connections}")
            print(f"Trying to find the connction: {self._connectionManager.conWrap[LicencePlate]}")
            self._connectionManager.conWrap[LicencePlate].update(1)
            return True
        except:
            print("")
            return False
















