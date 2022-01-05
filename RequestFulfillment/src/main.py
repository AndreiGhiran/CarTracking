from database.DatabaseHandler import DatabaseHandler

from flask import Flask, jsonify
from configparser import ConfigParser


PORT = 8081


app = Flask(__name__)

config_parser = ConfigParser()
config_parser.read('../configuration/db.config')
db_data = {
    'user': config_parser.get('database', 'user'),
    'pass': config_parser.get('database', 'pass'),
    'host': config_parser.get('database', 'host'),
    'schema': config_parser.get('database', 'schema')
}
database_handler = DatabaseHandler(db_data['user'], db_data['pass'], db_data['host'], db_data['schema'])


@app.get('/cars')
def cars():
    cars_positions = database_handler.get_cars()

    response = {
        'carsPositions': [
            {
                'Box_1_Latitude': car_position[0],
                'Box_1_Longitude': car_position[1],
                'Box_2_Latitude': car_position[2],
                'Box_2_Longitude': car_position[3],
                'Box_3_Latitude': car_position[4],
                'Box_3_Longitude': car_position[5],
                'Box_4_Latitude': car_position[6],
                'Box_4_Longitude': car_position[7],
            }
            for car_position in cars_positions
        ]
    }

    return jsonify(response), 200

@app.get('/obstacles')
def obstacles():
    obstacles_positions = database_handler.get_obstacles()

    response = {
        'obstaclesPositions': [
            {
                'Box_1_Latitude': obstacle_position[0],
                'Box_1_Longitude': obstacle_position[1],
                'Box_2_Latitude': obstacle_position[2],
                'Box_2_Longitude': obstacle_position[3],
                'Box_3_Latitude': obstacle_position[4],
                'Box_3_Longitude': obstacle_position[5],
                'Box_4_Latitude': obstacle_position[6],
                'Box_4_Longitude': obstacle_position[7],
            }
            for obstacle_position in obstacles_positions
        ]
    }

    return jsonify(response), 200

@app.get('/ping')
def ping():
    return jsonify({
        'load': 'pong'
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)