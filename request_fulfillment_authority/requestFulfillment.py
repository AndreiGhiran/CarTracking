from AOP_decorators.decorators import method_call_decorator, exception_catcher

class CarRequestFullfilmentAuthority:

    @exception_catcher
    @method_call_decorator
    def satisfyRequest(self, client, trafficCameraGeolocation):
        return [], []
