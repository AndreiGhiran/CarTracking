from AOP_decorators.decorators import method_call_decorator, exception_catcher

class CarRequestFullfilmentAuthority:


    # TODO return data fom DB instead of dummy lists
    @exception_catcher
    @method_call_decorator
    def satisfyRequest(self, trafficCameraGeolocation):
        return [1,2,3,4,5], [6,5,3,4,5]
