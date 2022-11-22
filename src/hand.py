# from card import Card


class Hand:
    def __init__(self, cards: list) -> None:
        # self.cards: list(Card) = cards
        self.cards = cards

    def hand_value(self) -> int:
        """
        Return total hand value, no matter what the value is.
        It takes into account soft/hard hand and 21 logic.
        Example of a hand: 2 A 3 A 9 K
        """
        soft_hand = False
        hand_value = 0
        for card in self.cards:
            if soft_hand:
                card_value = card.card_value(ace_as_one=True)
                if hand_value + card_value <= 21:
                    hand_value += card_value
                else:
                    hand_value += card_value - 10
                    soft_hand = False
            else:
                if card.is_ace_card():
                    if hand_value + 11 <= 21:
                        hand_value += 11
                        soft_hand = True
                    else:
                        hand_value += 1
                else:
                    hand_value += card.card_value()
        return hand_value

    def busted(self) -> bool:
        return self.hand_value() > 21

    def black_jack(self) -> bool:
        return self.hand_value() == 21 and len(self.cards) == 2

    def hand_of_pairs(self) -> bool:
        """Check if the player has a hand of pairs e.g., 5s."""
        if len(self.cards) == 2:
            return self.cards[0].rank == self.cards[1].rank
        else:
            return False

    def print_hand(self) -> None:
        for card in self.cards:
            print(card, end=" ")
        print()

    def print_hand_and_hand_value(self, msg: str) -> None:
        print(f"{msg}: ", end="")
        self.print_hand()
        print(f"{msg} value: {self.hand_value()}")
