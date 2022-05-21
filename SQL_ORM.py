import sqlite3
import time
from datetime import datetime

from proto1_pb2 import *

dictDrivers = {'Driver Licence ID': "VARCHAR(255)",
                'Full Name': "VARCHAR(255)",
                'Exp Date Of Driver Licence': "VARCHAR(256)",
                'Vehicle ID': "VARCHAR(256)",
                'Phone Number': "VARCHAR(255)",
                'Email': "VARCHAR(255)"}

dictVehicles = {'Licence Plate': "VARCHAR(255)",
                 'Make': "VARCHAR(255)",
                 'Model': "VARCHAR(255)",
                 'Year': "INT",
                 'Kms': "INT",
                 'Driver': 'VARCHAR(255)',
                 'Issues': "VARCHAR(255)",
                 'Fuel Economy': "FLOAT",
                 'Join Date': "VARCHAR(255)",
                 'Fuel Type': "TEXT"}

dictStats = {"Licence Plate": "VARCHAR(255)",
              "Last Update Date": "VARCHAR(255)",
              "Trip Counter": "INT",
              "Update Counter": "INT",
              "Max Speed": "FLOAT",
              "Avg Speed": "FLOAT",
              "Max RPM": "FLOAT",
              "Avg RPM": "FLOAT",
              "Avg Fuel Economy": "FLOAT",
              "Curr Fuel Economy": "FLOAT",
              "Is Online": "BOOL"}

class SQL_ORM:
    def __init__(self, home_dir):
        self.homeDir = home_dir
        self.sqliteConnection = sqlite3.connect(f'{self.homeDir}/CFM.db')
        #print(f"Connected to database - {self.homeDir}/CFM.db")
        self.table("Vehicles", dictVehicles)
        self.table("Drivers", dictDrivers)
        self.table("Stats", dictStats)
        #print("CREATED SQL CONNECTION _____________________________________________")

    def get_cursor(self):
        sqliteConnection = sqlite3.connect(f'{self.homeDir}/CFM.db')
        return sqliteConnection, sqliteConnection.cursor()

    def table(self, name, values : dict):
        sql, cursor = self.get_cursor()
        cursor.execute(f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{name}' ''')
        ret = cursor.fetchall()
        if ret[0][0] == 0:
            #print(f"Creating table {name}")
            command = f'''CREATE TABLE {name} ('''
            for each in values:
                command += f"'{each}' {values[each]}, "
            command += f"PRIMARY KEY ('{list(values.keys())[0]}'));"
            cursor.execute(command)
        sql.commit()
        sql.close()

    def deleteDriver(self, DriverLicenceID : str):
        sql, cursor = self.get_cursor()
        command = f"""DELETE FROM Drivers WHERE "Driver Licence ID" = "{DriverLicenceID}";"""
        cursor.execute(command)
        sql.commit()
        sql.close()

    def deleteVehicle(self, LicencePlate : str):
        sql, cursor = self.get_cursor()
        command = f"""DELETE FROM Vehicles WHERE "Licence Plate" = "{LicencePlate}";"""
        cursor.execute(command)
        command = f"""DELETE FROM Stats WHERE "Licence Plate" = "{LicencePlate}";"""
        cursor.execute(command)
        sql.commit()
        sql.close()

    def __del__(self):
        self.sqliteConnection.close()

    def message(self, data):
        sql, cursor = self.get_cursor()
        car_data = CurrData()
        car_data.ParseFromString(data)
        stats = {"Licence Plate": "",
              "Last Update Date": "",
              "Trip Counter": -1,
              "Update Counter": -1,
              "Max Speed": -1.0,
              "Avg Speed": -1.0,
              "Max RPM": -1.0,
              "Avg RPM": -1.0,
              "Avg Fuel Economy": -1.0,
              "Curr Fuel Economy" :-1.0}
        command = (f"""SELECT * FROM Stats WHERE "Licence Plate" = "{car_data.CAR_ID}";""")
        #print(command)
        cursor.execute(command)
        ret = cursor.fetchall()
        #print(ret)
        values = ret[0]
        for index, key in enumerate(stats):
            stats[key] = values[index]
        stats["Last Update Date"] = str(datetime.now())
        if stats["Max Speed"] < car_data.SPEED:
            stats["Max Speed"] = car_data.SPEED
        if stats["Max RPM"] < car_data.RPM:
            stats["Max RPM"] = car_data.RPM
        stats["Curr Fuel Economy"] = car_data.FUEL_CONSUMPTION
        stats["Avg Speed"] = stats["Avg Speed"] * stats["Update Counter"] + car_data.SPEED
        stats["Avg RPM"] = stats["Avg RPM"] * stats["Update Counter"] + car_data.RPM
        stats["Update Counter"] = stats["Update Counter"] + 1
        stats["Avg Speed"] /= stats["Update Counter"]
        stats["Avg RPM"] /= stats["Update Counter"]
        if stats["Trip Counter"] == 1:
            stats["Avg Fuel Economy"] = car_data.FUEL_CONSUMPTION
        command = """UPDATE Stats SET """
        for each in stats:
            try:
                float(stats[each])
                command+= f""""{each}" = {stats[each]}, """
            except:
                command += f""""{each}" = "{stats[each]}", """
        command = f"""{command[:-2]} WHERE "Licence Plate" = "{car_data.CAR_ID}";"""
        #print(command)
        cursor.execute(command)
        print(f"stats: {stats}")
        sql.commit()
        sql.close()

    def create_connection(self, id: str):
        sql, cursor = self.get_cursor()
        command = f"""SELECT * FROM Stats WHERE "Licence Plate" = "{id}";"""
        cursor.execute(command)
        ret = cursor.fetchall()
        if not ret:
            #print(f"------------------------Creating a new line {id}-------------------------")
            command = f"""INSERT INTO Stats VALUES ("{id}","0",1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,TRUE);"""
            cursor.execute(command)
        else:
            command = f"""UPDATE Stats SET "Is Online" = TRUE WHERE "Licence Plate" = "{id}";"""
            cursor.execute(command)
            command = f"""UPDATE Stats SET "Trip Counter" = "Trip Counter" + 1 WHERE "Licence Plate" = "{id}";"""
            cursor.execute(command)
        sql.commit()
        sql.close()


    def close_connection(self, id: str):
        sql, cursor = self.get_cursor()
        command = f"""UPDATE Stats SET "Is Online" = FALSE WHERE "Licence Plate" = "{id}";"""
        cursor.execute(command)
        command = f"""SELECT * FROM Stats WHERE "Licence Plate" = "{id}";"""
        cursor.execute(command)
        values = cursor.fetchall()[0]
        stats = {"Licence Plate": "",
                 "Last Update Date": "",
                 "Trip Counter": -1,
                 "Update Counter": -1,
                 "Max Speed": -1.0,
                 "Avg Speed": -1.0,
                 "Max RPM": -1.0,
                 "Avg RPM": -1.0,
                 "Avg Fuel Economy": -1.0,
                 "Curr Fuel Economy": -1.0}
        for index, key in enumerate(stats):
            stats[key] = values[index]
        avg_fuel_economy = (stats["Trip Counter"]-1)*stats["Avg Fuel Economy"]+stats["Curr Fuel Economy"]
        avg_fuel_economy /= stats["Trip Counter"]
        command = f"""UPDATE Stats SET "Avg Fuel Economy" = {avg_fuel_economy} WHERE "Licence Plate" = "{id}";"""
        cursor.execute(command)
        sql.commit()
        sql.close()

    def getStats(self):
        sql, cursor = self.get_cursor()
        command = f"""SELECT * FROM Stats;"""
        cursor.execute(command)
        ret = cursor.fetchall()
        sql.close()
        return ret

    def updateDrivers(self, driverLicenceID, fullName, expDate, vehicleID, phoneNumber, email):
        sql, cursor = self.get_cursor()
        command = f"""INSERT INTO Drivers VALUES ("{driverLicenceID}","{fullName}","{expDate}","{vehicleID}","{phoneNumber}","{email}");"""
        sql.execute(command)
        sql.commit()
        sql.close()


if __name__ == "__main__":
    sql = SQL_ORM(".")
