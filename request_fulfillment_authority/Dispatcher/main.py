from flask import Flask, request, jsonify
from configparser import ConfigParser
from subprocess import Popen, PIPE
from time import sleep


PORT = 8081

app = Flask(__name__)


@app.route("/carRequest",  methods=['GET'])
def carRequest():
    request_json = request.get_json()

    # TODO use real geolocation values (there are temporary)
    geolocation = [12,34]
    authority_process = Popen('python ../Authority/src/main.py {}'.format(
        geolocation,
    ), stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True)
    
    obstacles = []
    cars = []
    for stdout_line in iter(authority_process.stdout.readline, ' '):
        output = str(stdout_line)
        print(output)
        print('END' in output)
        sleep(5)
        if "obstacles" in output:
            for obj in output[15:-6].split(', '):
                obstacles.append(obj)
        if "cars" in output:
            for obj in output[10:-6].split(', '):
                cars.append(obj)
        if "END" in output:
            break

    return jsonify({
        'cars': cars,
        'obstacles': obstacles,
    }), 200

if __name__ == '__main__':
    print("------------------------START")
    app.run(host='0.0.0.0', port=PORT)