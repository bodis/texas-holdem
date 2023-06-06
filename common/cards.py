from typing import List

from common.texas_holdem_enums import Rank, Suit

class Card:
    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit

    @classmethod
    def from_text(cls, text: str):
        rank_text = text[:-1]
        suit_text = text[-1]
        return Card(Rank(rank_text), Suit(suit_text))

    def __str__(self):
        return f"{self.rank.to_string()}{self.suit.to_string()}"

def convert_list_of_cards(cards: List[Card]) -> List[str]:
    return [str(card) for card in cards]

def convert_to_cards(card_values):
    cards = []
    for card_value in card_values:
        card = Card.from_text(card_value)
        cards.append(card)
    return cards
