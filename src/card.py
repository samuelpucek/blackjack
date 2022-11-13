class Card:
    SUITS = ["\u2666", "\u2665", "\u2663", "\u2660"]
    RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
    VALUES = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]

    def __init__(self, suit, rank) -> None:
        self.suit = suit
        self.rank = rank

    def __str__(self) -> str:
        """Print the card in a nice way."""
        return f"{Card.SUITS[self.suit]}{Card.RANKS[self.rank]}"

    def card_value(self, ace_as_one: bool = False) -> int:
        # TODO: fix "A"
        # Ace is counted as 11, only if the hand value exceeds 21 Ace is counted as 1
        if ace_as_one and self.rank == 12:
            return 1
        else:
            return Card.VALUES[self.rank]

    def is_ace_card(self) -> bool:
        return self.rank == 12
