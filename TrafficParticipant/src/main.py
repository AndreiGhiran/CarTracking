import requests

from configparser import ConfigParser


CARS_ENDPOINT = '/cars'
OBSTACLES_ENDPOINT = '/obstacles'


config_parser = ConfigParser()
config_parser.read('../configuration/traffic_fulfillment_authority.config')
traffic_fulfillment_authority_data = {
    'ip': config_parser.get('dispatcher', 'ip'),
    'port': config_parser.get('dispatcher', 'port')
}


def retrieve_data_from_server(ip, port, cars_endpoint, obstacles_endpoint):
    cars_url = '{}:{}{}'.format(ip, port, cars_endpoint)
    obstacles_url = '{}:{}{}'.format(ip, port, obstacles_endpoint)

    cars_positions = []
    obstacles_positions = []
    while True:
        cars_data = requests.get(cars_url, headers={'Content-Type': 'application/json'})
        updated_cars_positions = cars_data.json()['carsPositions']
        new_cars_positions = [car_position for car_position in updated_cars_positions if car_position not in cars_positions]
        if len(new_cars_positions) > 0:
            print('{} new cars positions retrieved'.format(len(new_cars_positions)))
        cars_positions = updated_cars_positions

        obstacles_data = requests.get(obstacles_url, headers={'Content-Type': 'application/json'})
        updated_obstacles_positions = obstacles_data.json()['obstaclesPositions']
        new_obstacles_positions = [obstacle_position for obstacle_position in updated_obstacles_positions if obstacle_position not in obstacles_positions]
        if len(new_obstacles_positions) > 0:
            print('{} new obstacles positions retrieved'.format(len(new_obstacles_positions)))
        obstacles_positions = updated_obstacles_positions


if __name__ == '__main__':
    retrieve_data_from_server(traffic_fulfillment_authority_data['ip'], traffic_fulfillment_authority_data['port'], CARS_ENDPOINT, OBSTACLES_ENDPOINT)