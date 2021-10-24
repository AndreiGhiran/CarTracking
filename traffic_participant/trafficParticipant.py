from AOP_decorators.decorators import method_call_decorator, exception_catcher

class TafficParticipant:
    geoLocation = None
    otherCarsGeolocations = []
    traffiCameraGeolocation = None
    obstaclesGeolocations = []
    cameraConnection = None

    @exception_catcher
    @method_call_decorator
    def __init__(self, geoLoc, otherGeoLoc, cameraGeolocation, obstaclesGeoloc, cameraConn):
        self.geoLocation = geoLoc
        self.otherCarsGeolocations = otherGeoLoc
        self.traffiCameraGeolocation = cameraGeolocation
        self.obstaclesGeolocations = obstaclesGeoloc
        self.cameraConnection = cameraConn
    
    @exception_catcher
    @method_call_decorator
    def decideNexrAction(self, geolocation, otherCarsGeolocations, obstaclesGeolocations):
        action = None
        return action
    
    @exception_catcher
    @method_call_decorator
    def connectToClosestCamera():
        return 

    @exception_catcher
    @method_call_decorator
    def dissconectFromCamera():
        return None