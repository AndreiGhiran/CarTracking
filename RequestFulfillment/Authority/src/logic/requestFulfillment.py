# from ..AOP_decorators.decorators import method_call_decorator, exception_catcher
from AOP_decorators.src.decorators import exception_catcher,method_call_decorator


class CarRequestFulfillmentAuthority:

    # TODO return data fom DB instead of dummy lists
    @exception_catcher
    @method_call_decorator
    def satisfyRequest(self, trafficCameraGeolocation):
        return None
