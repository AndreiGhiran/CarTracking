import mysql.connector

from threading import Lock


class DatabaseHandler:
    def __init__(self, user: str, password: str, host: str, schema: str):
        self.__connection = mysql.connector.connect(user=user, password=password, host=host, database=schema)
        self.__cursor = self.__connection.cursor(buffered=True)
        self.__statement_lock = Lock() # Thread-safe

    def get_cars(self):
        statement = 'SELECT Box_1_Latitude, Box_1_Longitude, Box_2_Latitude, Box_2_Longitude, Box_3_Latitude, Box_3_Longitude, Box_4_Latitude, Box_4_Longitude FROM CARS'
        values = ()
        self.__statement_lock.acquire()
        self.__cursor.execute(statement, values)
        self.__connection.commit()
        result = self.__cursor.fetchall()
        self.__statement_lock.release()
        return result

    def get_obstacles(self):
        statement = 'SELECT Box_1_Latitude, Box_1_Longitude, Box_2_Latitude, Box_2_Longitude, Box_3_Latitude, Box_3_Longitude, Box_4_Latitude, Box_4_Longitude FROM OBSTACLES'
        values = ()
        self.__statement_lock.acquire()
        self.__cursor.execute(statement, values)
        self.__connection.commit()
        result = self.__cursor.fetchall()
        self.__statement_lock.release()
        return result