import socket
from enum import Enum
import threading


class ConnectionWrap:
    def __init__(self, licence_plate, connection_manager, host, next_time):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._data = ""
        self._active = False
        self._idleCounter = 0
        self._licencePlate = licence_plate
        self._connectionManager = connection_manager
        self._port = 0
        self._running = True
        self._thread = threading.Thread(target=self.run_socket, args=(host,))
        self._nextTime = next_time
        self._thread.start()

    def __del__(self):
        self._running = False
        try:
            self._thread.join()
        except:
            pass
        self._socket.close()

    def run_socket(self, host):
        self._socket.bind((host, 0))
        self._port = self._socket.getsockname()[1]
        self._socket.listen()
        conn, addr = self._socket.accept()
        with conn:
            #print(f"Connected by {addr}")
            while self._running:
                try:
                    self._data = conn.recv(1024)
                    self._active = True
                    print(self._data)
                    #send time interval to wait before next sending
                    conn.send(str(self._nextTime).encode())
                except:
                    #print("Conenction was closed")
                    self._socket.close()
                    self._connectionManager.disconnect_a_client(self._licencePlate)
                    break

    def get_socket(self):
        return self._socket

    def update(self, next_time):
        self._nextTime = next_time
        if self._active:
            result = self._data
            self._active = False
            return result
        else:
            if self._idleCounter < 10:
                self._idleCounter += 1
            if self._idleCounter == 10:
                self._connectionManager.destroy(self)

    def updateWithOutTime(self):
        if self._active:
            result = self._data
            self._active = False
            return result
        else:
            if self._idleCounter < 10:
                self._idleCounter += 1
            if self._idleCounter == 10:
                self._connectionManager.destroy(self)

    def get_licence_plate(self):
        return self._licencePlate

    def is_active(self):
        return self._active

    def get_data(self):
        return self._data



