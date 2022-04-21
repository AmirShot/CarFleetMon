import threading

from EngineStats import EngineStats
#from EngineConnection import Connection
from LogConnection import Connection
import socket
from proto1_pb2 import *
import time


class ObdClient:
    def __init__(self):
        self.connection = Connection("log.csv")
        self.secondsToWait = 0
        self.kmWithEngineOn = 0
        self.CurrentRideTotalDistance = 0
        self.timeDiffMeasured = 0
        self.connection = Connection("log.csv")
        self.sumOfFuelCons = 0
        self.initialDistance = 0
        self.fuelEconomy = 0
        self.totalKms = 0
        with open("CarData.txt", "r") as file:
            self.ID = file.readline()
            if not self.ID:
                print("ENTER LICENCE PLATE NOW! (file: CarData.txt)")

        # create client server connection - initial socket  -> new socket
        port = 65432
        s = socket.socket()
        s.connect(("127.0.0.1", port))
        s.send(self.ID.encode())
        newPort = s.recv(1024).decode()
        print(newPort)
        s.close()
        self.directSocket = socket.socket()
        self.directSocket.connect(("127.0.0.1", int(newPort)))
        #####################################################

        # start thread of send updates
        self.t = threading.Thread(target=self.send_update)
        #####################################################

    def send_update(self):
        # read initial distance from file
        file = open("logKm.txt", "r+")
        content = file.read()
        print(f"read: {content}")
        try:
            print(content)
            self.initialDistance = float(content)
        except:
            file.write("0")
            print("no kms were written")
        file.close()
        ####################################

        # read first sample
        sample = EngineStats()
        self.connection.sample(sample)
        # print(sample)
        time.sleep(self.secondsToWait)
        current_time_stamp = sample.timeStamp
        ########################################

        # main loop
        while self.connection.sample(sample):
            time_diff_measured = (sample.timeStamp - current_time_stamp).microseconds / 1000000
            self.CurrentRideTotalDistance += sample.speed * time_diff_measured / 3600
            self.update_kms(file)
            if sample.engineOn:
                self.kmWithEngineOn += sample.speed * time_diff_measured / 3600
                self.sumOfFuelCons += sample.getCurrFuelConsumption() * time_diff_measured / 0.752 / 1000
            try:
                print(f"total fuel used: {self.sumOfFuelCons} Liter")
                self.fuelEconomy = self.CurrentRideTotalDistance / self.sumOfFuelCons
            except:
                print("Distance is 0")
            current_time_stamp = sample.timeStamp

            # build message
            message = CurrData()
            message.CAR_ID = self.ID
            message.RPM = sample.RPM
            message.SPEED = sample.speed
            message.RUN_TIME = sample.RUN_TIME
            message.CONTROL_MODULE_VOLTAGE = sample.CONTROL_MODULE_VOLTAGE
            message.AMBIANT_AIR_TEMP = sample.AMBIANT_AIR_TEMP
            message.FUEL_TYPE = sample.FUEL_TYPE
            message.OIL_TEMP = sample.OIL_TEMP
            message.FUEL_CONSUMPTION = self.fuelEconomy
            message.TOTAL_DISTANCE_SINCE_JOIN = self.totalKms
            message.DTC = sample.DTC
            ##############################

            # send message
            bits = message.SerializeToString() # string of bits
            self.directSocket.send(bits)
            ##############################

            time.sleep(self.secondsToWait)

    def update_kms(self, file):
        file = open("logKm.txt", "w+")
        self.totalKms = self.initialDistance + self.CurrentRideTotalDistance
        print(f"totalKms = {self.totalKms}--------------------")
        file.write(f"{self.totalKms}")
        file.close()



if __name__ == "__main__":
    client = ObdClient()
