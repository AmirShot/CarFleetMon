from datetime import datetime
import time
from threading import Thread

from EngineStats import EngineStats
#from EngineConnection import Connection
from LogConnection import Connection


class FuelGetter():
    def __init__(self):
        self.secondsToWait = 0
        self.kmWithEngineOn = 0
        self.CurrentRideTotalDistance = 0
        self.timeDiffMeasured = 0
        self.connection = Connection("log.csv")
        self.sumOfFuelCons = 0
        self.beforeKms = 0



    def ThreadOfFuel(self):
        file = open("logKm.txt", "r+")
        content = file.read()
        print(f"read: {content}")
        try:
            print(content)
            self.beforeKms = float(content)
        except:
            file.write("0")
            print("no kms were written")
        file.close()
        sample = EngineStats()
        self.connection.sample(sample)
        #print(sample)
        time.sleep(self.secondsToWait)
        currentTimeStamp = sample.timeStamp

        #
        #print(self.connection.sample(sample))
        #
        while self.connection.sample(sample):
            #print(f"---------------------------\n\n{sample}\n\n---------------------------")
            timeDiffMeasured = (sample.timeStamp - currentTimeStamp).microseconds / 1000000
            self.CurrentRideTotalDistance += sample.speed * timeDiffMeasured / 3600
            self.updateKms(file)
            #print(f"Current Distance is: {self.CurrentRideTotalDistance}")

            #print(f"Current Fuel Consumption: {self.sumOfFuelCons}")
            if sample.engineOn:
                self.kmWithEngineOn += sample.speed * timeDiffMeasured / 3600
                #print(f"kmWithEngineOn: {self.kmWithEngineOn}")
                self.sumOfFuelCons += sample.getCurrFuelConsumption() * timeDiffMeasured / 0.752 / 1000
                #print(
                    #"\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\nOn----------------------------------------------------------------------------")
            try:
                print(f"total fuel used: {self.sumOfFuelCons} Liter")
                print(
                    f"---------------------------- FUEL: {self.CurrentRideTotalDistance / self.sumOfFuelCons} [km/l]----------------------------")
                #kinda return
            except:
                print("Distance is 0")
            currentTimeStamp = sample.timeStamp
            time.sleep(self.secondsToWait)

    def updateKms(self,file):
        file = open("logKm.txt", "w+")
        totalKms = self.beforeKms + self.CurrentRideTotalDistance
        print(f"totalKms = {totalKms}--------------------")
        file.write(f"{totalKms}")
        file.close()
    def startFuelThread(self):
        thread = Thread(target=self.ThreadOfFuel)
        thread.start()
        thread.join()
        print("finished measuring fuel")

fueler = FuelGetter()
fueler.startFuelThread()





