from EngineStats import EngineStats
import obd
from datetime import datetime

class Connection:

    def __init__(self, log=""):
        self.conn = obd.OBD()
        print("-----------------------------\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        if log != "":
            print("-----------------------------\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            self.log = open(log, "w")
            self.log.write("Time Stemp,Engine On,Speed,MAF,RPM,RUN_TIME,CONTROL_MODULE_VOLTAGE,AMBIANT_AIR_TEMP,FUEL_TYPE,OIL_TEMP,\n")
        else:
            self.log = None

  #  def __del__(self):
   #     self.log.close()

    def sample(self, e: EngineStats):
        e.timeStamp = datetime.now()
        e.RPM = self.conn.query(obd.commands.RPM).value.magnitude
        e.engineOn = e.RPM > 1
        e.speed = self.conn.query(obd.commands.SPEED).value.magnitude
        e.MAF = self.conn.query(obd.commands.MAF).value.magnitude
        e.RUN_TIME = self.conn.query(obd.commands.RUN_TIME).value.magnitude
        e.CONTROL_MODULE_VOLTAGE = self.conn.query(obd.commands.CONTROL_MODULE_VOLTAGE).value.magnitude
        e.AMBIANT_AIR_TEMP = self.conn.query(obd.commands.AMBIANT_AIR_TEMP).value.magnitude
        e.FUEL_TYPE = self.conn.query(obd.commands.FUEL_TYPE).value
        e.OIL_TEMP = self.conn.query(obd.commands.OIL_TEMP).value.magnitude
        dtc = self.conn.query(obd.commands.OIL_TEMP).value
        e.DTC = ""
        for each in dtc:
            e.DTC += f'::{each[0]}'

        if self.log:
            self.log.write(f"{e}\n")
        return e
