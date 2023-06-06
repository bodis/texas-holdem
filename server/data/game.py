from typing import List
from server.data.player import Player
from server.data.play import Play
from server.data.player_game import PlayerGame


class Game:
    def __init__(self, initial_players: List[Player]):
        self.players: List[Player] = initial_players  # List of registered players
        self.plays: List[Play] = []  # List of previous plays in the game
        self.current_play: Play = None  # Current play in progress
        self.player_games = []
        for player in self.players:
            self.player_games.append(PlayerGame(player, 10000))

    def add_play(self, play: Play):
        if self.current_play:
            self.plays.append(self.current_play)
        self.current_play = play

    def add_player(self, player: Player):
        self.players.append(player)

    def get_players_with_coins(self) -> List[Player]:
        return [player for player in self.players if player.coin_number > 0]

    # running if more than 1 player has >0 coins
    def is_game_running(self) -> bool:
        return sum(1 for p in self.player_games if p.coins > 0) > 1

    def play_game(self):
        # play till the end
        while self.is_game_running():
            play = Play(self.player_games, 1)
            self.add_play(play)
            play.play()


    def __str__(self):
        player_names = [player.name for player in self.players]
        num_plays = len(self.plays)

        game_info = f"Players: {', '.join(player_names)}"
        game_info += f"\nNumber of plays: {num_plays}"

        if self.current_play:
            game_info += "\n\nCurrent Play:\n" + str(self.current_play)

        return game_info
