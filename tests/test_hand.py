import unittest
from parameterized import parameterized

from src.card import Card
from src.hand import Hand


class TestHand(unittest.TestCase):
    @parameterized.expand(
        [
            ("one ace", [Card(0, 12)], 11),
            ("two aces", [Card(i, 12) for i in range(2)], 12),
            ("three aces", [Card(i, 12) for i in range(3)], 13),
            ("four aces", [Card(i, 12) for i in range(4)], 14),
        ]
    )
    def test_hand_value_aces(self, name, cards, expected_hand_value):
        hand = Hand(cards)
        self.assertEqual(hand.hand_value(), expected_hand_value)

    @parameterized.expand(
        # 2 A 3 A 9 K
        [
            ("2", [Card(0, 0)], 2),
            ("2 A", [Card(0, 0), Card(0, 12)], 13),
            ("2 A 3", [Card(0, 0), Card(0, 12), Card(0, 1)], 16),
            (
                "2 A 3 A",
                [Card(0, 0), Card(0, 12), Card(0, 1), Card(1, 12)],
                17,
            ),
            (
                "2 A 3 A 9",
                [Card(0, 0), Card(0, 12), Card(0, 1), Card(1, 12), Card(1, 7)],
                16,
            ),
            (
                "2 A 3 A 9 K",
                [
                    Card(0, 0),
                    Card(0, 12),
                    Card(0, 1),
                    Card(1, 12),
                    Card(1, 7),
                    Card(3, 11),
                ],
                26,
            ),
        ]
    )
    def test_hand_value_tricky_hand(self, name, cards, expected_hand_value):
        hand = Hand(cards)
        self.assertEqual(hand.hand_value(), expected_hand_value)

    @parameterized.expand(
        [
            ("2", [Card(0, 0)], False),
            ("2 A", [Card(0, 0), Card(0, 12)], False),
            ("2 A 3", [Card(0, 0), Card(0, 12), Card(0, 1)], False),
            (
                "2 A 3 A",
                [Card(0, 0), Card(0, 12), Card(0, 1), Card(1, 12)],
                False,
            ),
            (
                "2 A 3 A 9",
                [Card(0, 0), Card(0, 12), Card(0, 1), Card(1, 12), Card(1, 7)],
                False,
            ),
            (
                "2 A 3 A 9 K",
                [
                    Card(0, 0),
                    Card(0, 12),
                    Card(0, 1),
                    Card(1, 12),
                    Card(1, 7),
                    Card(3, 11),
                ],
                True,
            ),
            ("K A", [Card(0, 11), Card(0, 12)], False),
            ("9 K", [Card(0, 7), Card(0, 11)], False),
            ("2 Q J", [Card(0, 0), Card(0, 10), Card(0, 9)], True),
            ("6 Q K", [Card(0, 4), Card(0, 10), Card(0, 11)], True),
        ]
    )
    def test_busted_hand(self, name, cards, expected_busted):
        hand = Hand(cards)
        self.assertEqual(hand.busted(), expected_busted)


if __name__ == "__main__":
    unittest.main()
