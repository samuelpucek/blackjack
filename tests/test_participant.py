import unittest
from parameterized import parameterized
from src.participant import Participant
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


if __name__ == "__main__":
    unittest.main()
