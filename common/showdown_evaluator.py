from enum import Enum
from typing import Dict
from typing import List
from itertools import combinations

from common.cards import Card
from common.cards import Rank


class HandRank(Enum):
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIRS = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9


class HandRankWithScore:

    def __init__(self, rank: HandRank, cards: List[Card]):
        self.rank = rank
        self.cards = cards
        if self.rank == HandRank.HIGH_CARD:
            self.value = evaluate_HIGH_CARD(self.cards)
        elif self.rank == HandRank.ONE_PAIR:
            self.value = evaluate_ONE_PAIR(self.cards)
        elif self.rank == HandRank.TWO_PAIRS:
            self.value = evaluate_TWO_PAIRS(self.cards)
        elif self.rank == HandRank.THREE_OF_A_KIND:
            self.value = evaluate_THREE_OF_A_KIND(self.cards)
        elif self.rank == HandRank.STRAIGHT:
            self.value = evaluate_STRAIGHT(self.cards)
        elif self.rank == HandRank.FLUSH:
            self.value = evaluate_FLUSH(self.cards)
        elif self.rank == HandRank.FULL_HOUSE:
            self.value = evaluate_FULL_HOUSE(self.cards)
        elif self.rank == HandRank.FOUR_OF_A_KIND:
            self.value = evaluate_FOUR_OF_A_KIND(self.cards)
        elif self.rank == HandRank.STRAIGHT_FLUSH:
            self.value = evaluate_STRAIGHT_FLUSH(self.cards)
        else:
            self.value = 0

    def __str__(self):
        card_txt = ','.join([str(card) for card in self.cards])
        return f"{card_txt} - {self.rank} ({self.value})"

def rank_strength(rank: Rank) -> int:
    if rank == Rank.TWO:
        return 1
    elif rank == Rank.THREE:
        return 2
    elif rank == Rank.FOUR:
        return 3
    elif rank == Rank.FIVE:
        return 4
    elif rank == Rank.SIX:
        return 5
    elif rank == Rank.SEVEN:
        return 6
    elif rank == Rank.EIGHT:
        return 7
    elif rank == Rank.NINE:
        return 8
    elif rank == Rank.TEN:
        return 9
    elif rank == Rank.JACK:
        return 10
    elif rank == Rank.QUEEN:
        return 11
    elif rank == Rank.KING:
        return 12
    elif rank == Rank.ACE:
        return 13
    else:
        return 0

def remove_ranks(cards: List[Card], rank: Rank) -> List[Card]:
    new_cards = [c for c in cards if c.rank != rank]
    return new_cards

def calculate_rank_counts(cards: List[Card]) -> Dict[Rank, int]:
    sorted_cards = sorted(cards, key=lambda c: rank_strength(c.rank), reverse=True)
    rank_counts = {}
    for card in sorted_cards:
        if card.rank in rank_counts:
            rank_counts[card.rank] += 1
        else:
            rank_counts[card.rank] = 1
    return rank_counts

def evaluate_HIGH_CARD(cards: List[Card]) -> int:
    sorted_cards = sorted(cards, key=lambda c: rank_strength(c.rank))
    card_sum = 0
    for i, card in enumerate(sorted_cards):
        card_sum += rank_strength(card.rank) * (14 ** i)
    return card_sum

def evaluate_ONE_PAIR(cards: List[Card]) -> int:
    sorted_cards = sorted(cards, key=lambda c: rank_strength(c.rank), reverse=True)

    rank_counts = calculate_rank_counts(sorted_cards)
    pairs = find_elements_in_rank_counts(rank_counts, 2)  # 1db
    single_cards = remove_ranks(sorted_cards, pairs[0])
    sorted_single_cards = sorted(single_cards, key=lambda c: rank_strength(c.rank), reverse=True)

    card_sum = rank_strength(pairs[0]) * (14 ** 3)  # pair
    for i, card in enumerate(sorted_single_cards):  # every single
        card_sum += rank_strength(card.rank) * (14 ** i)
    return card_sum

def evaluate_TWO_PAIRS(cards: List[Card]) -> int:
    sorted_cards = sorted(cards, key=lambda c: rank_strength(c.rank), reverse=True)

    rank_counts = calculate_rank_counts(sorted_cards)
    pairs = find_elements_in_rank_counts(rank_counts, 2)  # 2db
    single_cards = remove_ranks(sorted_cards, pairs[0])
    single_cards = remove_ranks(single_cards, pairs[1])

    # erosebb pair van elorebb
    pairs = sorted(pairs, key=lambda p: rank_strength(p), reverse=True)
    card_sum = rank_strength(pairs[0]) * (14 ** 2)  # pair 1
    card_sum += rank_strength(pairs[1]) * (14 ** 1)  # pair 2
    card_sum += rank_strength(single_cards[0].rank)  # single 1
    return card_sum

def evaluate_THREE_OF_A_KIND(cards: List[Card]) -> int:
    sorted_cards = sorted(cards, key=lambda c: rank_strength(c.rank), reverse=True)

    rank_counts = calculate_rank_counts(sorted_cards)
    three = find_elements_in_rank_counts(rank_counts, 3)  # 1db
    single_cards = remove_ranks(sorted_cards, three[0])  # 2db
    sorted_single_cards = sorted(single_cards, key=lambda c: rank_strength(c.rank), reverse=True)

    # erosebb pair van elorebb
    card_sum = rank_strength(three[0]) * (14 ** 2)  # threes 1
    card_sum += rank_strength(sorted_single_cards[0].rank) * (14 ** 1)  # single 1
    card_sum += rank_strength(sorted_single_cards[1].rank)  # single 2
    return card_sum

def evaluate_STRAIGHT(cards: List[Card]) -> int:
    sorted_cards = sorted(cards, key=lambda c: rank_strength(c.rank), reverse=True)
    if sorted_cards[0].rank == Rank.ACE and sorted_cards[1].rank == Rank.FIVE:
        # A,2,3,4,5 -> weakest
        return 1
    else:
        return evaluate_HIGH_CARD(cards)

def evaluate_FLUSH(cards: List[Card]) -> int:
    card_sum = 0
    for card in cards:
        card_sum += rank_strength(card.rank)
    return card_sum

def evaluate_FULL_HOUSE(cards: List[Card]) -> int:
    sorted_cards = sorted(cards, key=lambda c: rank_strength(c.rank), reverse=True)
    rank_counts = calculate_rank_counts(sorted_cards)
    three = find_elements_in_rank_counts(rank_counts, 3)  # 1db
    twos = find_elements_in_rank_counts(rank_counts, 2)   # 1db
    return rank_strength(three[0]) * (14 ** 1) + rank_strength(three[0])

def evaluate_FOUR_OF_A_KIND(cards: List[Card]) -> int:
    sorted_cards = sorted(cards, key=lambda c: rank_strength(c.rank), reverse=True)
    rank_counts = calculate_rank_counts(sorted_cards)
    four = find_elements_in_rank_counts(rank_counts, 4)  # 1db
    return rank_strength(four[0])

def evaluate_STRAIGHT_FLUSH(cards: List[Card]) -> int:
    sorted_cards = sorted(cards, key=lambda c: rank_strength(c.rank), reverse=True)
    return rank_strength(sorted_cards[0].rank)

def find_elements_in_rank_counts(rank_counts: Dict[Rank, int], value: int) -> List[Rank]:
    result = []
    for key, val in rank_counts.items():
        if val == value:
            result.append(key)
    return result

def calculate_is_straight(cards: List[Card]) -> bool:
    sorted_cards = sorted(cards, key=lambda c: rank_strength(c.rank), reverse=True)
    return (
            len(sorted_cards) == 5
            and len(set([card.rank for card in sorted_cards])) == 5
            and (
                    rank_strength(sorted_cards[0].rank) - rank_strength(sorted_cards[4].rank) == 4
                    or (
                            sorted_cards[0].rank == Rank.ACE
                            and sorted_cards[1].rank == Rank.FIVE
                            and sorted_cards[2].rank == Rank.FOUR
                            and sorted_cards[3].rank == Rank.THREE
                            and sorted_cards[4].rank == Rank.TWO
                    )
            )
    )


def evaluate_hand_strength(cards: List[Card]) -> HandRankWithScore:
    sorted_cards = sorted(cards, key=lambda c: rank_strength(c.rank), reverse=True)

    # Check for flush
    suits = {card.suit for card in sorted_cards}
    is_flush = len(suits) == 1

    # Check for straight
    is_straight = calculate_is_straight(cards)

    # Check for duplicates
    rank_counts = calculate_rank_counts(sorted_cards)

    # Evaluate hand strength based on the rules of Texas Hold'em
    if is_straight and is_flush:
        hand_rank = HandRank.STRAIGHT_FLUSH
    elif any(count == 4 for count in rank_counts.values()):
        hand_rank = HandRank.FOUR_OF_A_KIND
    elif any(count == 3 for count in rank_counts.values()) and any(count == 2 for count in rank_counts.values()):
        hand_rank = HandRank.FULL_HOUSE
    elif is_flush:
        hand_rank = HandRank.FLUSH
    elif is_straight:
        hand_rank = HandRank.STRAIGHT
    elif any(count == 3 for count in rank_counts.values()):
        hand_rank = HandRank.THREE_OF_A_KIND
    elif list(rank_counts.values()).count(2) == 2:
        hand_rank = HandRank.TWO_PAIRS
    elif any(count == 2 for count in rank_counts.values()):
        hand_rank = HandRank.ONE_PAIR
    else:
        hand_rank = HandRank.HIGH_CARD

    return HandRankWithScore(hand_rank, cards)

def get_best_combination(cards: List[Card]) -> List[Card]:
    possible_combinations = list(combinations(cards, 5))
    best_combination = None
    best_rank = None

    for combination in possible_combinations:
        hand_rank = evaluate_hand_strength(combination)
        if best_rank is None:
            best_rank = hand_rank
            best_combination = combination
        elif rank_strength(hand_rank.rank) > rank_strength(best_rank.rank):
            best_rank = hand_rank
            best_combination = combination
        elif rank_strength(hand_rank.rank) == rank_strength(best_rank.rank) and hand_rank.value > best_rank.value:
            best_rank = hand_rank
            best_combination = combination

    return list(best_combination)

