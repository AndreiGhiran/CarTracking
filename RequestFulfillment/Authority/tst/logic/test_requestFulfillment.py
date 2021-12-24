from configparser import ConfigParser
from mockito import when
from datetime import datetime, timedelta

from ...src.logic.requestFulfillment import CarRequestFulfillmentAuthority

config_parser = ConfigParser()
config_parser.read(r'D:\Facultate\TAIP\project\CarTracking\RequestFulfillment\Authority\configuration\db.config')
db_data = {
    'user': config_parser.get('database', 'user'),
    'pass': config_parser.get('database', 'pass'),
    'host': config_parser.get('database', 'host'),
    'schema': config_parser.get('database', 'schema')
}

class TestRequestFulfillmentAuthority:

    def setup_class(self):
        self.__request_fulfillment = CarRequestFulfillmentAuthority(db_data['user'], db_data['pass'], db_data['host'], db_data['schema'])
        self.__trafficCameraGeolocation = [3,3]
        self.__stress_test_seconds = 3

    def test_satisfyRequest(self):
        when(self.__request_fulfillment).satisfyRequest(...).thenReturn([1,2,3,4], [4,5,6,3])

        assert self.__request_fulfillment.satisfyRequest(self.__trafficCameraGeolocation) == [1,2,3,4], [4,5,6,3]

    def test_stress_test(self):
        end = datetime.now() + timedelta(0,self.__stress_test_seconds)
        count = 0
        obj_count = 0
        start = datetime.now()
        while datetime.now().time() < end.time():
            cars, obstacles = self.__request_fulfillment.satisfyRequest(self.__trafficCameraGeolocation)
            obj_count += len(cars) + len(obstacles)
            count += 1
        end = datetime.now()
        interval = end - start
        print(f'{count} responses in {interval.seconds} seconds\naverage of {count/interval.seconds} responses/second \naverage of {obj_count/count} object locations/response')
        assert count >= self.__stress_test_seconds * 200 and count/interval.seconds >= 200 and obj_count/count >= 7 * count/interval.seconds
