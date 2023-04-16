import unittest
from parameterized import parameterized

from src.utils import Card, Hand


class TestHand(unittest.TestCase):
    @parameterized.expand(
        [
            ("one ace", [Card(0, 12)], 11),
            ("two aces", [Card(i, 12) for i in range(2)], 12),
            ("three aces", [Card(i, 12) for i in range(3)], 13),
            ("four aces", [Card(i, 12) for i in range(4)], 14),
        ]
    )
    def test_hand_value_aces(
        self, name: str, cards: list, expected_hand_value: int
    ):
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
    def test_hand_value_tricky_hand(
        self, name: str, cards: list, expected_hand_value: int
    ):
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
    def test_busted_hand(self, name: str, cards: list, expected_busted: bool):
        hand = Hand(cards)
        self.assertEqual(hand.busted(), expected_busted)

    @parameterized.expand(
        [
            ("2", [Card(0, 0)], False),
            ("2 A", [Card(0, 0), Card(0, 12)], False),
            ("2 A 3", [Card(0, 0), Card(0, 12), Card(0, 1)], False),
            ("K A A", [Card(0, 11), Card(0, 12), Card(0, 12)], False),
            ("A Q", [Card(3, 12), Card(2, 10)], True),
            ("K A", [Card(1, 11), Card(3, 12)], True),
            ("10 A", [Card(0, 8), Card(0, 12)], True),
            (
                "K K A A",
                [Card(0, 11), Card(0, 11), Card(0, 12), Card(0, 12)],
                False,
            ),
        ]
    )
    def test_black_jack_hand(
        self, name: str, cards: list, expected_black_jack: bool
    ):
        hand = Hand(cards)
        self.assertEqual(hand.black_jack(), expected_black_jack)

    @parameterized.expand(
        [
            ("2", [Card(0, 0)], False),
            ("2 A", [Card(0, 0), Card(0, 12)], False),
            ("2 2 2", [Card(0, 0), Card(0, 0), Card(0, 0)], False),
            ("2 A 3", [Card(0, 0), Card(0, 12), Card(0, 1)], False),
            ("K A A", [Card(0, 11), Card(0, 12), Card(0, 12)], False),
            ("A Q", [Card(3, 12), Card(2, 10)], False),
            ("K A", [Card(1, 11), Card(3, 12)], False),
            ("2 2", [Card(1, 0), Card(3, 0)], True),
            ("3 3", [Card(1, 1), Card(3, 1)], True),
            ("4 4", [Card(1, 2), Card(3, 2)], True),
            ("5 5", [Card(1, 3), Card(3, 3)], True),
            ("6 6", [Card(1, 4), Card(3, 4)], True),
            ("7 7", [Card(1, 5), Card(3, 5)], True),
            ("8 8", [Card(1, 6), Card(3, 6)], True),
            ("9 9", [Card(1, 7), Card(3, 7)], True),
            ("10 10", [Card(1, 8), Card(3, 8)], True),
            ("J J", [Card(1, 9), Card(3, 9)], True),
            ("Q Q", [Card(1, 10), Card(3, 10)], True),
            ("K K", [Card(1, 11), Card(3, 11)], True),
            ("A A", [Card(1, 12), Card(3, 12)], True),
        ]
    )
    def test_hand_of_pairs(self, name: str, cards: list, expected_pairs: bool):
        hand = Hand(cards)
        self.assertEqual(hand.hand_of_pairs(), expected_pairs)

    @parameterized.expand(
        [
            ("2", [Card(0, 0)], False),
            ("2 A", [Card(0, 0), Card(0, 12)], False),
            ("2 A 3", [Card(0, 0), Card(0, 12), Card(0, 1)], False),
            ("K A A", [Card(0, 11), Card(0, 12), Card(0, 12)], False),
            ("A Q", [Card(3, 12), Card(2, 10)], False),
            ("K A", [Card(1, 11), Card(3, 12)], False),
            ("2 2", [Card(1, 0), Card(3, 0)], False),
            ("3 3", [Card(1, 1), Card(3, 1)], False),
            ("4 4", [Card(1, 2), Card(3, 2)], False),
            ("5 5", [Card(1, 3), Card(3, 3)], False),
            ("6 6", [Card(1, 4), Card(3, 4)], False),
            ("7 7", [Card(1, 5), Card(3, 5)], False),
            ("8 8", [Card(1, 6), Card(3, 6)], False),
            ("9 9", [Card(1, 7), Card(3, 7)], False),
            ("10 10", [Card(1, 8), Card(3, 8)], False),
            ("J J", [Card(1, 9), Card(3, 9)], False),
            ("Q Q", [Card(1, 10), Card(3, 10)], False),
            ("K K", [Card(1, 11), Card(3, 11)], False),
            ("A A", [Card(1, 12), Card(3, 12)], True),
            ("A A", [Card(0, 12), Card(0, 12)], True),
            ("A A", [Card(3, 12), Card(3, 12)], True),
        ]
    )
    def test_hand_of_double_aces(
        self, name: str, cards: list, expected_pairs: bool
    ):
        hand = Hand(cards)
        self.assertEqual(hand.hand_of_double_aces(), expected_pairs)


if __name__ == "__main__":
    unittest.main()
