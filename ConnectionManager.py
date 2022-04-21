import socket
import threading
from ConnectionWrap import ConnectionWrap

class ConnectionManager:
    def __init__(self, host):
        self._mainPort = 65432
        self._mainSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conWrap = dict()
        self._running = True
        self.nextTime = 10
        print(host)
        self._thread = threading.Thread(target=self.run_main_socket, args=(host,))
        self._thread.start()

    def run_main_socket(self, host):
        self._mainSocket.bind((host, self._mainPort))
        self._mainSocket.listen()
        conn, addr = self._mainSocket.accept()
        with conn:
            print(f"Connected by {addr}")
            while self._running:
                data = conn.recv(1024).decode()
                plate = data #maybe split
                print(f"plate: {plate}")

                if plate not in self.conWrap:
                    print("not exist")
                    self.conWrap[plate] = ConnectionWrap(plate, self, host, self.nextTime)
                    print(f"connWrap: {self.conWrap[plate]}")
                print(self.conWrap[plate].get_socket().getsockname()[1])
                conn.send(str(self.conWrap[plate].get_socket().getsockname()[1]).encode())

                print("sent new socket")

    def stop_server(self):
        self._running = False
        self._thread.join()



if __name__ == "__main__":
    server = ConnectionManager("127.0.0.1")


