from AOP_decorators.src.decorators import exception_catcher, method_call_decorator


class TrafficParticipant:
    geoLocation = None
    otherCarsGeolocations = []
    trafficCameraGeolocation = None
    obstaclesGeolocations = []
    cameraConnection = None

    def __init__(self, geoLoc, otherGeoLoc, cameraGeolocation, obstaclesGeoloc, cameraConn):
        self.geoLocation = geoLoc
        self.otherCarsGeolocations = otherGeoLoc
        self.traffiCameraGeolocation = cameraGeolocation
        self.obstaclesGeolocations = obstaclesGeoloc
        self.cameraConnection = cameraConn

    @exception_catcher
    @method_call_decorator
    def decideNextAction(self, geolocation, otherCarsGeolocations, obstaclesGeolocations):
        return None


    @exception_catcher
    @method_call_decorator
    def connectToClosestCamera(self):
        return None

    @exception_catcher
    @method_call_decorator
    def dissconectFromCamera(self):
        return None
