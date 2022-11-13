import random
from card import Card


class Deck:
    def __init__(self, decks: int = 6) -> None:
        """
        Initialize a new deck of cards and shuffle.
        """
        self.cards = [
            Card(i, j) for i in range(4) for j in range(13) for k in range(decks)
        ]
        self._shuffle()

    def __len__(self) -> int:
        """Return size of the deck."""
        return len(self.cards)

    def _shuffle(self) -> None:
        """Shuffle the deck."""
        random.shuffle(self.cards)

    def __str__(self) -> str:
        """Print the deck."""
        deck_written = ""
        for card in self.cards:
            deck_written += card.__str__() + " "
        return deck_written.strip()
