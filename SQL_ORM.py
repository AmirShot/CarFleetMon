import sqlite3
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
                 'Fuel Type': "TEXT",
                 'Is Online': "BOOL"}

dictStats = {"Licence Plate": "VARCHAR(255)",
              "Last Update Date": "VARCHAR(255)",
              "Trip Counter": "INT",
              "Update Counter": "INT",
              "Max Speed": "FLOAT",
              "Avg Speed": "FLOAT",
              "Max RPM": "FLOAT",
              "Avg RPM": "FLOAT",
              "Avg Fuel Economy": "FLOAT"}

class SQL_ORM:
    def __init__(self, home_dir):
        self.homeDir = home_dir
        self.sqliteConnection = sqlite3.connect(f'{self.homeDir}/CFM.db')
        self.cursor = self.sqliteConnection.cursor()
        print(f"Connected to database - {self.homeDir}/CFM.db")
        self.table("Vehicles", dictVehicles)
        self.table("Drivers", dictDrivers)
        self.table("Stats", dictStats)

    def table(self, name, values : dict):
        self.cursor.execute(f''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{name}' ''')
        ret = self.cursor.fetchall()
        if ret[0][0] == 0:
            print(f"Creating table {name}")
            command = f'''CREATE TABLE {name} ('''
            for each in values:
                command += f"'{each}' {values[each]}, "
            command += f"PRIMARY KEY ('{list(values.keys())[0]}'));"
            self.cursor.execute(command)

    def __del__(self):
        self.sqliteConnection.close()

    def message(self, data):
        car_data = CurrData()
        car_data.ParseFromString(data)


if __name__ == "__main__":
    sql = SQL_ORM(".")
