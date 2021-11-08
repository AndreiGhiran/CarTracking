import pytest
import mysql.connector

from mockito import when, mock, spy, verify, unstub, forget_invocations, any

from ...src.logic.requestFulfillment import CarRequestFulfillmentAuthority


class TestRequestFulfillmentAuthority:

    def setup_class(self):
        self.__request_fulfillment = CarRequestFulfillmentAuthority()
        self.__trafficCameraGeolocation = [0,0]

    def test_satisfyRequest(self):
        when(self.__request_fulfillment).satisfyRequest(...).thenReturn([1,2,3,4], [4,5,6,3])

        assert self.__request_fulfillment.satisfyRequest(self.__trafficCameraGeolocation) == [1,2,3,4], [4,5,6,3]


