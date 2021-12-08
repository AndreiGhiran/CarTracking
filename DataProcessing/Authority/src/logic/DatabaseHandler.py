import mysql.connector

from threading import Lock
from typing import List, Tuple


class DatabaseHandler:
    def __init__(self, user: str, password: str, host: str, schema: str):
        self.__connection = mysql.connector.connect(user=user, password=password, host=host, database=schema)
        self.__cursor = self.__connection.cursor()
        self.__statement_lock = Lock() # Thread-safe

    def insert_camera(self, latitude: float, longitude: float, x_rotation: float, y_rotation: float) -> int:
        statement = 'INSERT INTO CAMERAS (Latitude, Longitude, XRotation, YRotation) VALUES (%s, %s, %s, %s)'
        values = (latitude, longitude, x_rotation, y_rotation)

        self.__statement_lock.acquire()
        self.__cursor.execute(statement, values)
        self.__connection.commit()
        inserted_row_id = self.__cursor.lastrowid
        self.__statement_lock.release()

        return inserted_row_id

    def insert_cars(self, camera_id: int, cars_positions: List[Tuple[float, float, float, float, float, float, float, float, float]]):
        self.delete_cars(camera_id)

        for car_position in cars_positions:
            self.insert_car(camera_id, car_position[0], car_position[1], car_position[2], car_position[3], car_position[4], car_position[5], car_position[6], car_position[7])

    def insert_car(self, camera_id: int, box_1_latitude: float, box_1_longitude: float, box_2_latitude: float, box_2_longitude: float, box_3_latitude: float, box_3_longitude: float, box_4_latitude: float, box_4_longitude: float):
        statement = 'INSERT INTO CARS (CameraID, Box_1_Latitude, Box_1_Longitude, Box_2_Latitude, Box_2_Longitude, Box_3_Latitude, Box_3_Longitude, Box_4_Latitude, Box_4_Longitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = (camera_id, box_1_latitude, box_1_longitude, box_2_latitude, box_2_longitude, box_3_latitude, box_3_longitude, box_4_latitude, box_4_longitude)

        self.__statement_lock.acquire()
        self.__cursor.execute(statement, values)
        self.__connection.commit()
        self.__statement_lock.release()
        
    def delete_cars(self, camera_id: int):
        statement = 'DELETE FROM CARS WHERE CameraID = %s'
        values = (camera_id,)

        self.__statement_lock.acquire()
        self.__cursor.execute(statement, values)
        self.__connection.commit()
        self.__statement_lock.release()

    def insert_obstacles(self, camera_id: int, obstacles_positions: List[Tuple[float, float, float, float, float, float, float, float, float]]):
        self.delete_obstacles(camera_id)

        for obstacle_position in obstacles_positions:
            self.insert_obstacle(camera_id, obstacle_position[0], obstacle_position[1], obstacle_position[2], obstacle_position[3], obstacle_position[4], obstacle_position[5], obstacle_position[6], obstacle_position[7])

    def insert_obstacle(self, camera_id: int, box_1_latitude: float, box_1_longitude: float, box_2_latitude: float, box_2_longitude: float, box_3_latitude: float, box_3_longitude: float, box_4_latitude: float, box_4_longitude: float):
        statement = 'INSERT INTO OBSTACLES (CameraID, Box_1_Latitude, Box_1_Longitude, Box_2_Latitude, Box_2_Longitude, Box_3_Latitude, Box_3_Longitude, Box_4_Latitude, Box_4_Longitude) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        values = (camera_id, box_1_latitude, box_1_longitude, box_2_latitude, box_2_longitude, box_3_latitude, box_3_longitude, box_4_latitude, box_4_longitude)

        self.__statement_lock.acquire()
        self.__cursor.execute(statement, values)
        self.__connection.commit()
        self.__statement_lock.release()

    def delete_obstacles(self, camera_id: int):
        statement = 'DELETE FROM OBSTACLES WHERE CameraID = %s'
        values = (camera_id,)

        self.__statement_lock.acquire()
        self.__cursor.execute(statement, values)
        self.__connection.commit()
        self.__statement_lock.release()

    def get_cars_by_geo_loc(self, geo_location):
        geo_loc_offset = 2
        statement = 'SELECT Latitude, Longitude FROM CARS WHERE Latitude <= %s AND Latitude >= %s AND Longitude <= %s AND Longitude >= %s'
        values = (geo_location[0] + geo_loc_offset, geo_location[0] - geo_loc_offset, geo_location[1] + geo_loc_offset, geo_location[1] - geo_loc_offset)
        self.__statement_lock.acquire()
        self.__cursor.execute(statement, values)
        result = self.__cursor.fetchall()
        self.__statement_lock.release()
        return result

    def get_obstacles_by_geo_loc(self, geo_location):
        geo_loc_offset = 2
        statement = 'SELECT Latitude, Longitude FROM OBSTACLES WHERE Latitude <= %s AND Latitude >= %s AND Longitude <= %s AND Longitude >= %s'
        values = (geo_location[0] + geo_loc_offset, geo_location[0] - geo_loc_offset, geo_location[1] + geo_loc_offset, geo_location[1] - geo_loc_offset)
        self.__statement_lock.acquire()
        self.__cursor.execute(statement, values)
        result = self.__cursor.fetchall()
        self.__statement_lock.release()
        return result
