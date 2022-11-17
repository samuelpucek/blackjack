import unittest
from parameterized import parameterized
from src.participant import Participant, Player, Dealer
from src.card import Card


class TestParticipant(unittest.TestCase):
    @parameterized.expand(
        [
            ("one ace", [Card(0, 12)], 11),
            ("two aces", [Card(i, 12) for i in range(2)], 12),
            ("three aces", [Card(i, 12) for i in range(3)], 13),
            ("four aces", [Card(i, 12) for i in range(4)], 14),
        ]
    )
    def test_hand_value_aces(self, name, hand_example, expected_hand_value):
        participant = Participant()
        participant.hand = hand_example
        self.assertEqual(participant.hand_value(), expected_hand_value)

    @parameterized.expand(
        # 2 A 3 A 9 K
        [
            ("2", [Card(0, 0)], 2),
            ("2 A", [Card(0, 0), Card(0, 12)], 13),
            ("2 A 3", [Card(0, 0), Card(0, 12), Card(0, 1)], 16),
            ("2 A 3 A", [Card(0, 0), Card(0, 12), Card(0, 1), Card(1, 12)], 17),
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
    def test_tricky_hand(self, name, hand_example, expected_hand_value):
        participant = Participant()
        participant.hand = hand_example
        self.assertEqual(participant.hand_value(), expected_hand_value)

    test_busted_hand_examples = [
        ("2", [Card(0, 0)], False),
        ("2 A", [Card(0, 0), Card(0, 12)], False),
        ("2 A 3", [Card(0, 0), Card(0, 12), Card(0, 1)], False),
        ("2 A 3 A", [Card(0, 0), Card(0, 12), Card(0, 1), Card(1, 12)], False),
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

    @parameterized.expand(test_busted_hand_examples)
    def test_dealer_busted(self, name, hand_example, expected_busted):
        dealer = Dealer()
        dealer.hand = hand_example
        self.assertEqual(dealer.busted(), expected_busted)

    @parameterized.expand(test_busted_hand_examples)
    def test_player_busted(self, name, hand_example, expected_busted):
        player = Player()
        player.hand = hand_example
        self.assertEqual(player.busted(), expected_busted)


if __name__ == "__main__":
    unittest.main()
