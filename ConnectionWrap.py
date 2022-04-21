import socket
from enum import Enum
import threading


class ConnectionWrap:
    def __init__(self, licence_plate, connection_manager, host, next_time):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._data = ""
        self._active = True
        self._idleCounter = 0
        self._licencePlate = licence_plate
        self._connectionManager = connection_manager
        self._port = 0
        self._running = True
        self._thread = threading.Thread(target=self.run_socket, args=host)
        self._nextTime = next_time
        self._thread.start()

    def __del__(self):
        self._running = False
        self._thread.join()
        self._socket.close()

    def run_socket(self, host):
        self._socket.bind((host, 0))
        self._port = self._socket.getsockname()[1]
        self._socket.listen()
        conn, addr = self._socket.accept()
        with conn:
            print(f"Connected by {addr}")
            while self._runnning:
                self._data = conn.recv(1024)
                #TODO: send time interval to wait before next sending
                conn.send(str(self._nextTime).encode())

    def get_socket(self):
        return self._socket

    def update(self, next_time):
        self._nextTime = next_time
        if self._active:
            result = self._data
            self._data = None
            self._active = False
            return result
        else:
            if self._idleCounter < 10:
                self._idleCounter += 1
            if self._idleCounter == 10:
                self._connectionManager.destroy(self)

    def get_licence_plate(self):
        return self._licencePlate




