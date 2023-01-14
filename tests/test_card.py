import unittest
from parameterized import parameterized

from src.utils import Card


class TestCard(unittest.TestCase):
    @parameterized.expand(
        [
            ("2", Card(0, 0), False),
            ("8", Card(0, 6), False),
            ("Q", Card(0, 10), False),
            ("A", Card(0, 12), True),
            ("A", Card(3, 12), True),
        ]
    )
    def test_is_ace_card(self, name: str, card: Card, expected_ace: bool):
        self.assertEqual(card.is_ace_card, expected_ace)

    @parameterized.expand(
        [
            ("2", Card(0, 0), False, 2),
            ("8", Card(0, 6), False, 8),
            ("Q", Card(0, 10), False, 10),
            ("A", Card(0, 12), False, 11),
            ("A", Card(3, 12), True, 1),
        ]
    )
    def test_card_value(
        self, name: str, card: Card, ace_as_one, expected_value: int
    ):
        self.assertEqual(card.card_value(ace_as_one), expected_value)


if __name__ == "__main__":
    unittest.main()
