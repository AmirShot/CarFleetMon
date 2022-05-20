from DataManager import DataManager
from ConnectionManager import ConnectionManager
from SQL_ORM import SQL_ORM
import GUI

class CarFleetMon:
    def __init__(self):
        self.sql_orm = SQL_ORM(".")
        self._connection_manager = ConnectionManager("127.0.0.1",self.sql_orm)
        self._data_manager = DataManager(self._connection_manager,self.sql_orm)
        self.GUI = GUI.GUI(self._data_manager)

if __name__ == "__main__":
    CFM = CarFleetMon()