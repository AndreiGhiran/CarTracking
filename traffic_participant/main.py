from logic.trafficParticipant import TrafficParticipant
from flask import jsonify
import requests

def dispatch(latitude, longitude):
    url = 'http://{}:{}/carRequest'.format('127.0.0.1', '8081')
    data = {
        'geolocation': [latitude,longitude]
    }
    response = requests.get(url, data=data)

    return response.json()

if __name__ == "__main__":
    response = dispatch(10,12)
    car = TrafficParticipant([10,12],response['cars'], [9,10], response['obstacles'], None)
    car.connectToClosestCamera()
    while True:
        action = car.decideNextAction(car.geoLocation, response['cars'], response['obstacles'])
        print(action)
        response = dispatch(car.geoLocation[0],car.geoLocation[1])
        #TODO add a way to stop the loop when disconecting from the camera
