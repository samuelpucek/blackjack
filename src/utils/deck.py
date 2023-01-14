import random
from .card import Card


class Deck:
    def __init__(self, decks: int) -> None:
        """
        Initialize a new deck of cards and shuffle.
        """
        self._decks = decks
        self.cards = self._generate_cards()
        self._shuffle_deck()

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

    def _generate_cards(self) -> list[Card]:
        """
        Generate list of cards.
        """
        cards = [
            Card(suit, rank)
            for suit in range(len(Card.SUITS))
            for rank in range(len(Card.RANKS))
            for _ in range(self._decks)
        ]
        return cards

    def _shuffle_deck(self) -> None:
        """
        Shuffle the deck.
        """
        random.shuffle(self.cards)
