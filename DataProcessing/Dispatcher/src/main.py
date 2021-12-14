import sys

from flask import Flask, request, jsonify
from configparser import ConfigParser
from subprocess import Popen, PIPE


PORT = 8080

VERBOSE = len(sys.argv) > 1


config_parser = ConfigParser()
config_parser.read('../configuration/db.config')
db_data = {
    'user': config_parser.get('database', 'user'),
    'pass': config_parser.get('database', 'pass'),
    'host': config_parser.get('database', 'host'),
    'schema': config_parser.get('database', 'schema')
}

app = Flask(__name__)


@app.post('/dispatch')
def dispatch():
    request_json = request.get_json()

    frame_size_x = request_json['frame_size_x']
    frame_size_y = request_json['frame_size_y']

    latitude = request_json['latitude']
    longitude = request_json['longitude']

    rotation_x = request_json['rotation_x']
    rotation_y = request_json['rotation_y']

    authority_process = Popen('python3 ../../Authority/src/main.py {} {} {} {} {} {} {} {} {} {}'.format(
        frame_size_x,
        frame_size_y,
        latitude,
        longitude,
        rotation_x,
        rotation_y,
        db_data['user'],
        db_data['pass'],
        db_data['host'],
        db_data['schema'],
        str(VERBOSE)
    ), stdout=PIPE)
    for stdout_line in iter(authority_process.stdout.readline, b''):
        if stdout_line != b'':
            try:
                authority_port = int(stdout_line)
                break
            except:
                continue

    return jsonify({
        'port': authority_port
    }), 200

@app.get('/ping')
def ping():
    return jsonify({
        'load': 'pong'
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)