import json
from typing import List

import requests

from common.cards import Card
from common.texas_holdem_enums import *
from server.data.player import Player


class PlayerGame:

    def __init__(self, player: Player, coins: int):
        self.player = player
        self.cards = []
        self.bid = 1
        self.coins = coins
        self.status = PlayerGameStatus.NORMAL
        self.player_pot = 0

    def set_player_cards(self, cards: List[Card]):
        self.cards = cards

    def update_coin_number(self, amount):
        self.coins += amount

    def restart(self):
        self.coins = 10000

    def play(self, player_data: dict, phase: Phase, r: Round, pot_per_player_max: int):
        if self.status == PlayerGameStatus.OUT:
            return
        elif self.status == PlayerGameStatus.ALL_IN:
            return

        player_data['phase'] = phase.name
        player_data['round'] = r.name

        print(player_data)
        print(json.dumps(player_data))

        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(self.player.registration_url + '/phase', json=json.dumps(player_data),
                                     headers=headers, timeout=1)
        except requests.Timeout:
            # request timeout => OUT and LOSE
            self.player_out()
            return

        response_data = response.get_json()
        action = response_data['action']
        raised_coin = response_data['raised_coins']

        try:
            if not action or action not in PlayerAction.__members__:
                raise ValueError('Invalid action received from player')

            if player_data['round'] == Round.ADDITIONAL and action == PlayerAction.RAISE:
                raise ValueError('Invalid action in FOLD round')

        except ValueError:
            # every serious error => OUT abd LOSE
            self.player_out()
            return

        # ALL_IN -> minden bemegy
        if action == PlayerAction.ALLIN:
            self.all_in()
        # emelest ker -> amennyit ker emel vagy ha sokat akkor ALL_IN
        elif action == PlayerAction.RAISE:
            if raised_coin >= self.coins:
                self.all_in()
            else:
                self.player_pot += raised_coin
                self.coins -= raised_coin
        # tart -> amennyivel kell tart vagy ha nem marad tobb penze ALL_IN
        elif action == PlayerAction.CALL:
            additional_coins = pot_per_player_max - self.player_pot
            if additional_coins >= self.coins:
                self.all_in()
            else:
                self.player_pot += additional_coins
                self.coins -= additional_coins
        # kiszall a jatekbol
        else:
            self.status = PlayerGameStatus.OUT

    def best_cards(self, community_cards: List[Card]) -> List[Card]:
        best = list(community_cards)
        best.append(self.cards)
        return best

    def player_out(self):
        self.status = PlayerGameStatus.OUT
        self.coins = 0

    def all_in(self):
        self.player_pot += self.coins
        self.coins = 0
        self.status = PlayerGameStatus.ALL_IN

    def __str__(self):
        return f"Player: {self.player.name}, Cards: {self.cards}, Bid: {self.bid}, Coins: {self.coins}"
