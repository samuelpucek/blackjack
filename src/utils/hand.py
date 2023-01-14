from .card import Card


class Hand:
    def __init__(self, cards: list) -> None:
        """
        Initialize a new hand of cards.
        """
        self.cards: list[Card] = cards
        self.black_jack_dislabled = False

    def __str__(self, second_card_hidden: bool = False) -> str:
        """
        Print the hand.
        """
        if second_card_hidden:
            return f"{self.cards[0].__str__()} XX"
        else:
            hand_written = ""
            for card in self.cards:
                hand_written += card.__str__() + " "
            return hand_written.strip()

    def hand_value(self, second_card_hidden: bool = False) -> int:
        """
        Return total hand value, no matter what the value is.
        It takes into account soft/hard hand and 21 logic.

        Hand example: 2 A 3 A 9 K
        """
        if second_card_hidden:
            return self.cards[0].card_value()
        else:
            soft_hand: bool = False
            hand_value: int = 0

            for card in self.cards:
                if soft_hand:
                    card_value = card.card_value(ace_as_one=True)
                    if hand_value + card_value <= 21:
                        hand_value += card_value
                    else:
                        hand_value += card_value - 10
                        soft_hand = False
                else:
                    if card.is_ace_card:
                        if hand_value + 11 <= 21:
                            hand_value += 11
                            soft_hand = True
                        else:
                            hand_value += 1
                    else:
                        hand_value += card.card_value()
            return hand_value

    def print_hand_and_hand_value(
        self, msg: str, second_card_hidden: bool = False
    ) -> None:
        """
        Print both the hand and the hand value in a nice way.
        """
        cards = self.__str__(second_card_hidden)
        value = self.hand_value(second_card_hidden)
        print(f"{msg}: {cards} [{value}]")

    def busted(self) -> bool:
        """
        Check if the hand is busted or not.
        """
        return self.hand_value() > 21

    def black_jack(self) -> bool:
        """
        Check if the hand is Black Jack or not.
        """
        return self.hand_value() == 21 and len(self.cards) == 2

    def hand_of_pairs(self) -> bool:
        """
        Check if the hand is a hand of pairs or not e.g., 5s.
        """
        if len(self.cards) == 2:
            return self.cards[0].rank == self.cards[1].rank
        else:
            return False

    def hand_of_double_aces(self) -> bool:
        """
        Check if the hand is a hand of double aces or not i.e., A A.
        """
        if len(self.cards) == 2:
            return self.cards[0].rank == self.cards[1].rank == 12
        else:
            return False
