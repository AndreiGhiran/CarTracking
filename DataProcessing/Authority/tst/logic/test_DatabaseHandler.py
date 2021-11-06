import pytest
import mysql.connector

from mockito import when, mock, spy, verify, unstub, forget_invocations

from ...src.logic.DatabaseHandler import DatabaseHandler


class TestUDPEndpoint:
    def setup_class(self):
        self.__sql_connection = mock()
        self.__cursor = mock()
        when(self.__sql_connection).cursor().thenReturn(self.__cursor)
        when(mysql.connector).connect(...).thenReturn(self.__sql_connection)

        self.__database_handler = DatabaseHandler('', '', '', '')

        spy(self.__cursor)

    def teardown_class(self):
        unstub(self.__cursor)
        unstub(self.__sql_connection)

    def test_when_InsertCamera_then_CursorExecutesCorrectStatement(self):
        forget_invocations(self.__cursor)

        self.__database_handler.insert_camera(0, 0, 0, 0)

        verify(self.__cursor).execute('INSERT INTO CAMERAS (Latitude, Longitude, XRotation, YRotation) VALUES (%f, %f, %f, %f)', (0, 0, 0, 0))

    def test_when_InsertCar_then_CursorExecutesCorrectStatement(self):
        forget_invocations(self.__cursor)

        self.__database_handler.insert_car(0, 0, 0)

        verify(self.__cursor).execute('INSERT INTO CARS (CameraID, Latitude, Longitude) VALUES (%d, %f, %f)', (0, 0, 0))

    def test_when_DeleteCars_then_CursorExecutesCorrectStatement(self):
        forget_invocations(self.__cursor)

        self.__database_handler.delete_cars(0)

        verify(self.__cursor).execute('DELETE FROM CARS WHERE CameraID = %d', (0))

    def test_when_InsertCars_then_CursorExecutesCorrectStatement(self):
        forget_invocations(self.__cursor)

        times = 10

        self.__database_handler.insert_cars(
            50,
            [(i, i) for i in range(times)]
        )

        for i in range(times):
            verify(self.__cursor).execute('INSERT INTO CARS (CameraID, Latitude, Longitude) VALUES (%d, %f, %f)', (50, i, i))
        verify(self.__cursor).execute('DELETE FROM CARS WHERE CameraID = %d', (50))

    def test_when_InsertObstacle_then_CursorExecutesCorrectStatement(self):
        forget_invocations(self.__cursor)

        self.__database_handler.insert_obstacle(0, 0, 0)

        verify(self.__cursor).execute('INSERT INTO OBSTACLES (CameraID, Latitude, Longitude) VALUES (%d, %f, %f)', (0, 0, 0))

    def test_when_DeleteObstacles_then_CursorExecutesCorrectStatement(self):
        forget_invocations(self.__cursor)

        self.__database_handler.delete_obstacles(0)

        verify(self.__cursor).execute('DELETE FROM OBSTACLES WHERE CameraID = %d', (0))

    def test_when_InsertObstacles_then_CursorExecutesCorrectStatement(self):
        forget_invocations(self.__cursor)

        times = 10

        self.__database_handler.insert_obstacles(
            50,
            [(i, i) for i in range(times)]
        )

        for i in range(times):
            verify(self.__cursor).execute('INSERT INTO OBSTACLES (CameraID, Latitude, Longitude) VALUES (%d, %f, %f)', (50, i, i))
        verify(self.__cursor).execute('DELETE FROM OBSTACLES WHERE CameraID = %d', (50))