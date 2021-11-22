from logic.trafficParticipant import TrafficParticipant
import requests
import json
from time import sleep


def dispatch(latitude, longitude):
    url = 'http://{}:{}/carRequest'.format('127.0.0.1', '8081')
    data = json.dumps({
        'geolocation': [latitude, longitude]
    })
    response = requests.get(url, data=data, headers={'Content-Type': 'application/json'})

    return response.json()


if __name__ == "__main__":
    response = dispatch(3, 2)
    print(response)
    car = TrafficParticipant([3, 2],response['cars'], [3, 2], response['obstacles'], None)
    car.connectToClosestCamera()
    while True:
        action = car.decideNextAction(car.geoLocation, response['cars'], response['obstacles'])
        print(action)
        response = dispatch(car.geoLocation[0],car.geoLocation[1])
        print(response)
        car.geoLocation[0] += 0.5
        car.geoLocation[1] += 0.5
        sleep(3)
        #TODO add a way to stop the loop when disconecting from the camera
