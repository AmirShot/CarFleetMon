from datetime import datetime

a = 7.718
b = 0.425143707


class EngineStats:

    def __init__(self):
        self.timeStamp = -1
        self.engineOn = False
        self.speed = -1
        self.MAF = -1          # MAF = mass air flow in g/s
        self.RPM = -1
        self.RUN_TIME = -1
        self.CONTROL_MODULE_VOLTAGE = -1
        self.AMBIANT_AIR_TEMP = -1
        self.FUEL_TYPE = ""
        self.OIL_TEMP = -1
        self.DTC = ""

    def __str__(self):
        return f"{self.timeStamp},{self.engineOn},{self.speed},{self.MAF},{self.RPM},{self.RUN_TIME},{self.CONTROL_MODULE_VOLTAGE},{self.AMBIANT_AIR_TEMP},{self.FUEL_TYPE},{self.OIL_TEMP}, {self.DTC}"

    def unpack(self, s):
        lst = s.split(",")
        print(lst)
        self.timeStamp = datetime.strptime(lst[0], '%Y-%m-%d %H:%M:%S.%f')
        self.speed = float(lst[2])
        self.MAF = float(lst[3])
        self.RPM = float(lst[4])
        self.RUN_TIME = float(lst[5])
        self.CONTROL_MODULE_VOLTAGE = float(lst[6])
        self.AMBIANT_AIR_TEMP = float(lst[7])
        self.FUEL_TYPE = str(lst[8])
        self.OIL_TEMP = float(lst[9])
        self.DTC = str(lst[10])
        if self.RPM > 0:
            self.engineOn = True
        else:
            self.engineOn = False
        print(self)

    def getCurrFuelConsumption(self):
        if not self.MAF:
            return 0
        #ret = self.speed*1/3600*1/self.MAF*14.7*710
        ret = self.MAF / 14.7
        print(f"curr fuel {ret}")
        return ret











