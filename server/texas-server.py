import requests
from typing import List
from flask import Flask, request, abort, jsonify
from data.player import Player
from typing import Dict
from server.data.game import Game

app = Flask(__name__)

# Global variable

class TexasGameDate:
    def __init__(self):
        self.players: Dict[str, Player] = {}
        self.game_actual: Game
        self.old_games: List[Game] = []
        self.is_game_running = False

game_data = TexasGameDate()

def is_player_valid(player: Player) -> bool:
    try:
        print('ping player on URL: ' + player.registration_url + '/ping' )
        response = requests.get(player.registration_url + '/ping', timeout=1)
    except requests.Timeout:
        print('ping timeout for url ' + player.registration_url)
        return False
    except requests.ConnectionError:
        print('connection refused for url ' + player.registration_url)
        return False
    if response.status_code != 200:
        print('Not Http200 for ping request for url:' + player.registration_url + ' - instead: ' + response.status_code)
        return False
    return True

# add nem player to the list
def add_player_to_global(player: Player):
    if is_player_valid(player):
        print('player is valid: ' + str(player))
        game_data.players[player.name] = player
        return True
    return False

# check all players and remove everybody who is not accessible
def check_players():
    print('players: ' + str(game_data.players))
    for name, player in game_data.players.items():
        print(player)
        if not is_player_valid(player):
            game_data.players.pop(name)

def continous_games():
    while game_data.is_game_running:
        check_players()
        if len(game_data.players) < 2:
            print('Not enough active users['+str(len(game_data.players))+'] so cannot run GAME')
            is_game_running = False
            return
        game_actual = Game(list(game_data.players.values()))
        game_actual.play_game()
        game_data.old_games.append(game_actual)
        game_actual = None

@app.route('/register', methods=['POST'])
def register():
    registration_data = request.get_json()
    name = registration_data['name']
    url = registration_data['url']
    if name is None or url is None:
        print('no name or url')
        abort(403)
    print('new registration - name:' + name + '; url:' + url)
    add_player_to_global(Player(name, url))
    return 'OK', 200

@app.route('/start_games', methods=['GET'])
def start_games():
    print(game_data.is_game_running)
    if game_data.is_game_running:
        print('game is already running')
    else:
        print('Starting games')
        game_data.is_game_running = True
        continous_games()
    return 'OK', 200

@app.route('/stop_games', methods=['GET'])
def stop_games():
    if not game_data.is_game_running:
        print('game is not running - cannot be stopped')
    else:
        print('Stopping games')
        game_data.is_game_running = False
    return 'OK', 200

@app.route('/list/players', methods=['GET'])
def list_players():
    return game_data.players

@app.route('/list/game/actual', methods=['GET'])
def list_game_actual():
    return game_data.game_actual

@app.route('/list/game/old', methods=['GET'])
def list_game_old():
    return game_data.old_games

if __name__ == '__main__':
    app.run()
