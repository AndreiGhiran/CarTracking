import sys

from logic.requestFulfillment import CarRequestFullfilmentAuthority

GEO_LOCATION = sys.argv[1]

if __name__ == "__main__":
    request_fulfillment = CarRequestFullfilmentAuthority()

    other_cars, obstacles = request_fulfillment.satisfyRequest(GEO_LOCATION)
    print("cars: ", other_cars)
    print("obstacles: ", obstacles)
    print("END")
    