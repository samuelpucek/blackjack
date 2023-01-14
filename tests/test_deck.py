import unittest
from parameterized import parameterized

from src.utils import Card, Deck


class TestDeck(unittest.TestCase):
    ranks_count = len(Card.RANKS)
    suits_count = len(Card.SUITS)

    @parameterized.expand(
        [
            ("D1", Deck(1), ranks_count * suits_count),
            ("D2", Deck(2), ranks_count * suits_count * 2),
            ("D6", Deck(6), ranks_count * suits_count * 6),
        ]
    )
    def test_deck_size(self, name: str, deck: Deck, expected_deck_size: int):
        self.assertEqual(len(deck.cards), expected_deck_size)


if __name__ == "__main__":
    unittest.main()
