import mysql.connector
from threading import Lock
from typing import List, Tuple


class DatabaseHandler:
    def __init__(self, user: str, password: str, host: str, schema: str):
        self.__connection = mysql.connector.connect(user=user, password=password, host=host, database=schema)
        self.__cursor = self.__connection.cursor()
        self.__statement_lock = Lock() # Thread-safe

    def insert_camera(self, latitude: float, longitude: float, x_rotation: float, y_rotation: float) -> int:
        statement = 'INSERT INTO CAMERAS (Latitude, Longitude, XRotation, YRotation) VALUES (%f, %f, %f, %f)'
        values = (latitude, longitude, x_rotation, y_rotation)

        self.__statement_lock.acquire()
        self.__cursor.execute(statement, values)
        self.__connection.commit()
        inserted_row_id = self.__cursor.lastrowid
        self.__statement_lock.release()

        return inserted_row_id

    def insert_cars(self, camera_id: int, cars_positions: List[Tuple[float, float]]):
        self.delete_cars(camera_id)

        for car_position in cars_positions:
            self.insert_car(camera_id, car_position[0], car_position[1])

    def insert_car(self, camera_id: int, latitude: float, longitude: float):
        statement = 'INSERT INTO CARS (CameraID, Latitude, Longitude) VALUES (%d, %f, %f)'
        values = (camera_id, latitude, longitude)

        self.__statement_lock.acquire()
        self.__cursor.execute(statement, values)
        self.__connection.commit()
        self.__statement_lock.release()
        
    def delete_cars(self, camera_id: int):
        statement = 'DELETE FROM CARS WHERE CameraID = %d'
        values = (camera_id)

        self.__statement_lock.acquire()
        self.__cursor.execute(statement, values)
        self.__connection.commit()
        self.__statement_lock.release()

    def insert_obstacles(self, camera_id: int, obstacles_positions: List[Tuple[float, float]]):
        self.delete_obstacles(camera_id)

        for obstacle_position in obstacles_positions:
            self.insert_obstacle(camera_id, obstacle_position[0], obstacle_position[1])

    def insert_obstacle(self, camera_id: int, latitude: float, longitude: float):
        statement = 'INSERT INTO OBSTACLES (CameraID, Latitude, Longitude) VALUES (%d, %f, %f)'
        values = (camera_id, latitude, longitude)

        self.__statement_lock.acquire()
        self.__cursor.execute(statement, values)
        self.__connection.commit()
        self.__statement_lock.release()

    def delete_obstacles(self, camera_id: int):
        statement = 'DELETE FROM OBSTACLES WHERE CameraID = %d'
        values = (camera_id)

        self.__statement_lock.acquire()
        self.__cursor.execute(statement, values)
        self.__connection.commit()
        self.__statement_lock.release()