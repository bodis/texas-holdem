from enum import Enum

# 13 fele rank van
class Rank(Enum):
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = '10'
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'
    ACE = 'A'

    def to_string(self):
        return self.value


class Suit(Enum):
    HEARTS = 'H'
    DIAMONDS = 'D'
    CLUBS = 'C'
    SPADES = 'S'

    def to_string(self):
        return self.value


class Phase(Enum):
    PRE_FLOP = 1
    FLOP = 2
    TURN = 3
    RIVER = 4


class Round(Enum):
    NORMAL = 1
    ADDITIONAL = 2


class PlayerAction(Enum):
    RAISE = 1
    ALLIN = 2
    CALL = 3
    FOLD = 4


class PlayerGameStatus(Enum):
    NORMAL = '1'
    ALL_IN = '2'
    OUT = '3'

