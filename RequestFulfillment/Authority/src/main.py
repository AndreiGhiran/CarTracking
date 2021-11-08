from flask import Flask, request, jsonify
from logic.requestFulfillment import CarRequestFulfillmentAuthority


PORT = 8081

app = Flask(__name__)


@app.route("/carRequest",  methods=['GET'])
def carRequest():
    request_json = request.get_json()

    # TODO use real geolocation values (there are temporary)
    geolocation = [12,34]
    
    request_handler = CarRequestFulfillmentAuthority()
    
    cars, obstacles = request_handler.satisfyRequest(geolocation)

    return jsonify({
        'cars': cars,
        'obstacles': obstacles,
    }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
