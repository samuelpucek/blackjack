import random
from .card import Card


class Deck:
    def __init__(self, decks: int) -> None:
        """
        Initialize a new deck of cards and shuffle.
        """
        self._suits = 4
        self._ranks = 13
        self._decks = decks
        self.cards = [
            Card(suit, rank)
            for suit in range(self._suits)
            for rank in range(self._ranks)
            for _ in range(self._decks)
        ]
        self._shuffle()

    def __len__(self) -> int:
        """
        Return the size of the deck.
        """
        return len(self.cards)

    def __str__(self) -> str:
        """
        Print the deck.
        """
        deck_written = ""
        for card in self.cards:
            deck_written += card.__str__() + " "
        return deck_written.strip()

    def _shuffle(self) -> None:
        """
        Shuffle the deck.
        """
        random.shuffle(self.cards)
