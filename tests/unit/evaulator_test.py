import unittest

from common.cards import convert_to_cards
from common.showdown_evaluator import *

class TestHandEvaluator(unittest.TestCase):
    def test_evaluate_hand_strength(self):
        # Test case 1: HIGH_CARD
        cards1 = convert_to_cards(['2S', '3C', '4H', 'AD', '9S'])
        result = evaluate_hand_strength(cards1)
        self.assertEqual(HandRank.HIGH_CARD, result.rank)
        self.assertEqual(44617, result.value)
        print(result)

        # Test case 2: ONE_PAIR
        cards2 = convert_to_cards(['2S', '2C', '4S', 'KS', '6S'])
        result2 = evaluate_hand_strength(cards2)
        self.assertEqual(HandRank.ONE_PAIR, result2.rank)
        self.assertEqual(3414, result2.value)
        print(result2)

        # Test case 3: TWO_PAIRS
        cards3 = convert_to_cards(['2S', '2C', '4S', '4C', '6S'])
        result3 = evaluate_hand_strength(cards3)
        self.assertEqual(HandRank.TWO_PAIRS, result3.rank)
        self.assertEqual(result3.value, 607)
        print(result3)

        # Test case 4: THREE_OF_A_KIND
        cards4 = convert_to_cards(['3S', '3C', '3D', 'AS', 'KS'])
        result4 = evaluate_hand_strength(cards4)
        self.assertEqual(HandRank.THREE_OF_A_KIND, result4.rank)
        self.assertEqual(586, result4.value)
        print(result4)

        # Test case 5: STRAIGHT
        cards5 = convert_to_cards(['2S', '3C', '4S', '5D', '6S'])
        result5 = evaluate_hand_strength(cards5)
        self.assertEqual(HandRank.STRAIGHT, result5.rank)
        self.assertEqual(44553, result5.value)
        print(result5)
        cards5 = convert_to_cards(['AS', '2S', '3C', '4S', '5D'])
        result5 = evaluate_hand_strength(cards5)
        self.assertEqual(HandRank.STRAIGHT, result5.rank)
        self.assertEqual(1, result5.value)
        print(result5)

        # Test case 6: FLUSH
        cards6 = convert_to_cards(['2S', '4S', '6S', '9S', 'AS'])
        result6 = evaluate_hand_strength(cards6)
        self.assertEqual(HandRank.FLUSH, result6.rank)
        self.assertEqual(30, result6.value)
        print(result6)

        # Test case 7: FULL_HOUSE
        cards7 = convert_to_cards(['2S', '2C', '2D', '5D', '5S'])
        result7 = evaluate_hand_strength(cards7)
        self.assertEqual(HandRank.FULL_HOUSE, result7.rank)
        self.assertEqual(15, result7.value)
        print(result7)

        # Test case 8: FOUR_OF_A_KIND
        cards8 = convert_to_cards(['4S', '4C', '4D', '4H', '6S'])
        result8 = evaluate_hand_strength(cards8)
        self.assertEqual(HandRank.FOUR_OF_A_KIND, result8.rank)
        self.assertEqual(3, result8.value)
        print(result8)

        # Test case 9: Straight Flush
        cards9 = convert_to_cards(['2S', '3S', '4S', '5S', '6S'])
        result9 = evaluate_hand_strength(cards9)
        self.assertEqual(HandRank.STRAIGHT_FLUSH, result9.rank)
        self.assertEqual(5, result9.value)
        print(result9)

    def test_get_best_combination(self):
        # Test case 1: Straight Flush vs Four of a Kind
        cards = convert_to_cards(['2S', '3S', '4S', '5S', '6S', '7S', '8S'])
        cards_best = convert_to_cards(['4S', '5S', '6S', '7S', '8S'])

        best_combination = get_best_combination(cards)
        result = evaluate_hand_strength(best_combination)
        print(result)


if __name__ == '__main__':
    unittest.main()
