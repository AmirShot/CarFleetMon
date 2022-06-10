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
        self.secondsToWait = 5
        self.kmWithEngineOn = 0
        self.CurrentRideTotalDistance = 0
        self.timeDiffMeasured = 0
        self.connection = Connection("log.csv")
        self.sumOfFuelCons = 0
        self.initialDistance = 0
        self.initialFuelUsed = 0
        self.fuelEconomy = 0
        self.totalKms = 0
        self.totalFuel = 0
        self.timeToWait = 0
        self.running = True
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
        self.directSocket = socket.socket()
        self.directSocket.connect(("127.0.0.1", int(newPort)))
        #####################################################

        # read first sample
        self.sample = EngineStats()
        self.connection.sample(self.sample)
        # print(sample)
        time.sleep(self.timeToWait)
        self.current_time_stamp = self.sample.timeStamp
        ########################################

        # start thread of send updates
        self.t = threading.Thread(target=self.update)
        self.t.start()
        self.t2 = threading.Thread(target=self.send_data())
        #####################################################


    def update(self):
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
        # read initial fuel from file
        file2 = open("logFuel.txt", "r+")
        content = file2.read()
        print(f"read: {content}")
        try:
            print(content)
            self.initialFuelUsed = float(content)
        except:
            file2.write("0")
            print("no kms were written")
        file2.close()
        ####################################

        # main loop
        print(f"Sample: {self.connection.sample(self.sample)}")
        while self.connection.sample(self.sample):
            time_diff_measured = (self.sample.timeStamp - self.current_time_stamp).microseconds / 1000000
            self.CurrentRideTotalDistance += self.sample.speed * time_diff_measured / 3600
            self.update_kms_and_fuel(file)
            if self.sample.engineOn:
                self.kmWithEngineOn += self.sample.speed * time_diff_measured / 3600
                self.sumOfFuelCons += self.sample.getCurrFuelConsumption() * time_diff_measured / 0.752 / 1000
            try:
                print(f"total fuel used: {self.sumOfFuelCons} Liter")
                self.fuelEconomy = self.CurrentRideTotalDistance / self.sumOfFuelCons
            except:
                print("Distance is 0")
            current_time_stamp = self.sample.timeStamp
            time.sleep(self.timeToWait)
        self.running = False

    def send_data(self):
        while self.running:
            # build message
            message = CurrData()
            message.CAR_ID = self.ID
            message.RPM = self.sample.RPM
            message.SPEED = self.sample.speed
            message.RUN_TIME = self.sample.RUN_TIME
            message.CONTROL_MODULE_VOLTAGE = self.sample.CONTROL_MODULE_VOLTAGE
            message.AMBIANT_AIR_TEMP = self.sample.AMBIANT_AIR_TEMP
            message.FUEL_TYPE = self.sample.FUEL_TYPE
            message.OIL_TEMP = self.sample.OIL_TEMP
            message.FUEL_CONSUMPTION = self.fuelEconomy
            message.TOTAL_DISTANCE_SINCE_JOIN = self.totalKms
            message.DTC = self.sample.DTC
            try:
                message.AVG_FUEL_CONSUMPTION = self.totalKms / self.totalFuel
            except:
                message.AVG_FUEL_CONSUMPTION = 0
            ##############################

            # send message
            bits = message.SerializeToString()  # string of bits
            print(bits)
            self.directSocket.send(bits)
            self.timeToWait = int(self.directSocket.recv(1024).decode())
            print(f"-----------------------\n\n\n\nupdated time to wait: {self.timeToWait}\n\n\n\n-----------------------")
            ##############################
            time.sleep(self.timeToWait)

    def update_kms_and_fuel(self, file):
        print(f"""
        ------------------------------------
        
        total kms of all times: {self.totalKms}
        total fuel used: {self.totalFuel}
        total fuel used for this ride: {self.sumOfFuelCons}
        
        ------------------------------------
        """)
        file = open("logKm.txt", "w+")
        self.totalKms = self.initialDistance + self.CurrentRideTotalDistance
        print(f"totalKms = {self.totalKms}--------------------")
        file.write(f"{self.totalKms}")
        file.close()
        file2 = open("logFuel.txt", "w+")
        self.totalFuel = self.initialFuelUsed + self.sumOfFuelCons
        print(f"totalFuel = {self.totalFuel}--------------------")
        file2.write(f"{self.totalFuel}")
        file2.close()



if __name__ == "__main__":
    client = ObdClient()
