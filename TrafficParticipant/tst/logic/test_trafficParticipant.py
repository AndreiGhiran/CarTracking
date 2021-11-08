import pytest
from mockito import when, mock, spy, verify, unstub, forget_invocations

from ...src.logic.trafficParticipant import TrafficParticipant


class TestTrafficParticipant:
    def setup_class(self):
        self.__action = mock()
        self.__geolocation = [0,0]
        self.__otherCarsGeolocations = [[0,0], [0,0]]
        self.__obstaclesGeolocations = [[0,0], [0,0]]
        self.__cameraGeolocation = [0,0]
        self.__cameraConnection = mock()
        self.__traffic_participant = TrafficParticipant([0, 0], self.__otherCarsGeolocations, self.__cameraGeolocation,
                                                        self.__obstaclesGeolocations, self.__cameraConnection)
        spy(self.__cameraConnection)

    def teardown_class(self):
        unstub(self.__cameraConnection)

    def test_decideNextAction(self):
        when(self.__traffic_participant).decideNextAction(...).thenReturn(self.__action)

        assert self.__traffic_participant.decideNextAction(self.__geolocation, self.__otherCarsGeolocations,
                                                           self.__obstaclesGeolocations) == self.__action

    def test_connectToClosestCamera(self):
        self.__traffic_participant.connectToClosestCamera()

        verify(self.__cameraConnection)

    def test_dissconectFromCamera(self):
        self.__traffic_participant.dissconectFromCamera()

        verify(self.__cameraConnection)
