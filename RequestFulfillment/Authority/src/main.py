from flask import Flask, request, jsonify
from configparser import ConfigParser
from logic.requestFulfillment import CarRequestFulfillmentAuthority
import sys

print(sys.argv)

PORT = 8081

app = Flask(__name__)

config_parser = ConfigParser()
config_parser.read(r'D:\Facultate\TAIP\project\CarTracking\RequestFulfillment\Authority\configuration\db.config')
db_data = {
    'user': config_parser.get('database', 'user'),
    'pass': config_parser.get('database', 'pass'),
    'host': config_parser.get('database', 'host'),
    'schema': config_parser.get('database', 'schema')
}

@app.route("/carRequest",  methods=['GET'])
def carRequest():
    request_json = request.get_json()

    geolocation = request_json['geolocation']
    
    request_handler = CarRequestFulfillmentAuthority(db_data['user'], db_data['pass'], db_data['host'], db_data['schema'])
    
    cars, obstacles = request_handler.satisfyRequest(geolocation)

    return jsonify({
        'cars': cars,
        'obstacles': obstacles,
    }), 200


if __name__ == '__main__':
    request_handler = CarRequestFulfillmentAuthority(db_data['user'], db_data['pass'], db_data['host'], db_data['schema'])
    request_handler.insert_stuff()

    app.run(host='0.0.0.0', port=PORT)
