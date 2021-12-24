from AOP_decorators.src.decorators import exception_catcher, method_call_decorator
from DataProcessing.Authority.src.logic.DatabaseHandler import DatabaseHandler


class CarRequestFulfillmentAuthority:

    def __init__(self, db_user, db_pass, db_host, db_schema):
        self.dataBaseHandler = DatabaseHandler(db_user, db_pass, db_host, db_schema)

    # TODO return data fom DB instead of dummy lists
    @exception_catcher
    @method_call_decorator
    def satisfyRequest(self, trafficCameraGeolocation):
        cars = self.dataBaseHandler.get_cars_by_geo_loc(trafficCameraGeolocation)
        obstacles = self.dataBaseHandler.get_obstacles_by_geo_loc(trafficCameraGeolocation)
        return cars, obstacles

    def insert_stuff(self):
        a = -2
        while a < 2:
            b = -2
            while b < 2:
                self.dataBaseHandler.insert_car(1,a,b)
                b += 0.1
            self.dataBaseHandler.insert_obstacle(1,a,b)
            a += 0.1
