from random import shuffle

from common.cards import *
from common.showdown_evaluator import *
from common.texas_holdem_enums import PlayerGameStatus, Phase, Round
from server.data.player_game import PlayerGame


class Play:
    def __init__(self, players: List[PlayerGame], bind: int):
        self.players = players  # List of players in the play
        self.bind = bind  # Bind amount for the play
        self.deck = []  # Deck of cards for the play
        self.community_cards = []
        self.pot = 0
        self.phase = Phase.PRE_FLOP
        self.best_player_cards: dict[PlayerGame, HandRankWithScore] = {}

    # megkeverjuk a paklit es kiosztjuk a lapokat
    def start(self):
        self.create_shuffled_deck()
        self.deal_initial_cards()

    def create_shuffled_deck(self):
        temp_deck = [Card(rank, suit) for rank in Rank for suit in Suit]
        shuffle(temp_deck)
        self.deck = temp_deck

    # kiosztjuk a lapokat a jatekosoknak
    def deal_initial_cards(self):
        actual_players = self.get_actual_players()
        num_players = len(actual_players)
        for i, player in enumerate(self.players):
            player_cards = [self.deck[i], self.deck[i + num_players]]
            player.cards = player_cards

    def do_phase(self, phase: Phase):
        # normal round
        actual_players = self.get_actual_players()
        for player in actual_players:
            player.play(self.get_player_data(player), phase, Round.NORMAL, self.max_player_pot())

        # additional round
        # TODO: okosabb es akar tobb lepeses additional kor is lehet (benti reszben is at kell irni)
        actual_players = self.get_actual_players()
        for player in actual_players:
            player.play(self.get_player_data(player), phase, Round.ADDITIONAL, self.max_player_pot())

    # PreFlop fazis
    def pre_flop(self):
        self.do_phase(Phase.PRE_FLOP)

    # put 3 cards to the table
    def flop(self):
        self.community_cards.extend(self.get_next_cards(3))
        self.do_phase(Phase.FLOP)

    # put the 4th card on the table
    def turn(self):
        self.community_cards.extend(self.get_next_cards(1))
        self.do_phase(Phase.TURN)

    # put the 5th card on the table
    def river(self):
        self.community_cards.extend(self.get_next_cards(1))
        self.do_phase(Phase.RIVER)

    # ki a nyertes:
    # - mindenkinek a legjobb paklijat vesszuk
    # - megnezzuk kie eri a legtobet
    # TODO: egyezoseg most meg nincs (Pot osztas)
    def finish(self):
        actual_players = self.get_actual_players()
        for player in actual_players:
            self.best_player_cards[player] = evaluate_hand_strength(get_best_combination(player.cards))

        best_player: PlayerGame = None
        best_score: HandRankWithScore = None
        for player, score in self.best_player_cards:
            if best_player is None:
                best_player = player
                best_score = score
            elif best_score.rank.value < score.rank.value:
                best_player = player
                best_score = score.value
            elif best_score.rank.value == score.rank.value and best_score < score.value:
                best_player = player
                best_score = score.value
        print('winner: ' + str(best_player) + ' cards: ' + str(best_score))

        # POT handling: csak annyit kap amennyit betett a tobbet visszakapja mindenki (a NORMAL agra nincs is szukseg)
        # TODO: SIDE POT handling (nem kapjak vissza hanem ok is meg jatszanak a maradek POT-ert)
        if best_player.status == PlayerGameStatus.ALL_IN:
            winner_pot = best_player.player_pot
            for player in self.players:
                if player.player_pot <= winner_pot:
                    best_player.coins += winner_pot
                else:
                    best_player.coins += winner_pot
                    player.coins += (best_player.coins - winner_pot)
        elif best_player.status == PlayerGameStatus.NORMAL:
            best_player.coins += self.pot_sum()

    # a kiesett jatekosokat kivesszuk a jatekbol
    def get_actual_players(self):
        return [player for player in self.players if player.status != PlayerGameStatus.OUT]

    def max_player_pot(self):
        return max(player.player_pot for player in self.players)

    def pot_sum(self):
        return sum(player.player_pot for player in self.players)

    def get_next_cards(self, num_cards: int) -> List[Card]:
        if len(self.deck) < num_cards:
            raise ValueError("Not enough cards in the deck.")

        next_cards = [self.deck.pop(0) for _ in range(num_cards)]
        return next_cards

    # teljes jatek vegigjatszasa
    def play(self):
        self.start()
        self.pre_flop()
        self.flop()
        self.turn()
        self.river()
        self.finish()

    def get_player_data(self, player: PlayerGame) -> dict:
        player_data = {
            'player_card': convert_list_of_cards(player.cards),
            'cards_on_table': convert_list_of_cards(self.community_cards),
            'players': self.get_active_players(),
            'pot': self.pot,
            'phase': self.phase
        }
        return player_data

    def get_active_players(self):
        return [{'name': player.player.name, 'coin': player.coins} for player in self.players if
                player.status != PlayerGameStatus.OUT]
