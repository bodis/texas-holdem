import requests
import json
import time
from flask import Flask, request, abort, jsonify
import random
import threading
from server.data.game import Game
import sys

app = Flask(__name__)


# global datas
SERVER_BASE_URL = 'http://127.0.0.1:5000'
NAME = sys.argv[1]
if NAME is None:
    NAME = 'texas-player'
MY_PORT = random.randint(10000, 11000)
MY_URL = 'http://127.0.0.1:' + str(MY_PORT)

game_actual: Game = None


@app.route('/register', methods=['GET'])
def register():
    # register data
    data = {
        'name': NAME,
        'url': MY_URL
    }

    response: requests.Response
    try:
        headers = {'Content-Type': 'application/json'}
        print(SERVER_BASE_URL + '/register  - ' + json.dumps(data))
        response = requests.post(SERVER_BASE_URL + '/register', data=json.dumps(data), headers=headers)
        print('reqistration response: ' + str(response.status_code))
    except requests.Timeout:
        print('ping timeout for REGISTRATION')
        abort(403)

    if response is None or response.status_code != 200:
        print('cannot register. http code ' + str(response))
        abort(403)

    print('Registration successful: ' + response.text)
    return 'OK', 200

@app.route('/phase', methods=['POST'])
def play_game():
    data = request.get_json()
    print(str(data))
    result = {
        'action': 'CALL'
        #'raised_coins': MY_URL
    }
    return 'OK', 200

@app.route('/ping', methods=['GET'])
def ping():
    return 'OK', 200

def init_application():
    time.sleep(2)
    with app.test_request_context():
        print('INIT CLIENT: call register')
        result = app.test_client().get('/register')

def init_rest_app():
    app.run(port=MY_PORT)

# kulon kell futtatni a szerert meg az init reszt
if __name__ == '__main__':
    print('port:' + str(MY_PORT))

    # Start a new thread to perform the actions
    t = threading.Thread(target=init_rest_app)
    t.start()

    t = threading.Thread(target=init_application)
    t.start()

