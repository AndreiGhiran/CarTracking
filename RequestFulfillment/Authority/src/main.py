from flask import Flask, request, jsonify
from logic.requestFulfillment import CarRequestFulfillmentAuthority
import sys

print(sys.argv)

PORT = 8081

app = Flask(__name__)

DB_USER = sys.argv[1]
DB_PASS = sys.argv[2]
DB_HOST = sys.argv[3]
DB_SCHEMA = sys.argv[4]


@app.route("/carRequest",  methods=['GET'])
def carRequest():
    request_json = request.get_json()

    geolocation = request_json['geolocation']
    
    request_handler = CarRequestFulfillmentAuthority(DB_USER, DB_PASS, DB_HOST, DB_SCHEMA)
    
    cars, obstacles = request_handler.satisfyRequest(geolocation)

    return jsonify({
        'cars': cars,
        'obstacles': obstacles,
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
