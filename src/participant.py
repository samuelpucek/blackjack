class Participant:
    def __init__(self) -> None:
        # TODO: "Hand" will need to be separate class / object - one player can have multiple hands
        self.hand = []

    def empty_hand(self) -> None:
        self.hand = []

    def print_hand(self) -> None:
        print(f"{self.__class__.__name__} hand: ", end="")
        for card in self.hand:
            print(card, end=" ")
        print()

    def hand_value(self) -> int:
        """
        Return total hand value, no matter what the value is.
        It takes into account soft/hard hand and 21 logic.
        Example of a hand: 2 A 3 A 9 K
        """
        soft_hand = False
        hand_value = 0
        for card in self.hand:
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

    def print_hand_value(self) -> None:
        print(f"{self.__class__.__name__} value: {self.hand_value()}")

    def print_hand_and_value(self) -> None:
        self.print_hand()
        self.print_hand_value()

    def busted(self) -> bool:
        return self.hand_value() > 21

    def black_jack(self) -> bool:
        return self.hand_value() == 21 and len(self.hand) == 2


class Player(Participant):
    def __init__(self, min_bet: int = 10, balance: int = 100) -> None:
        # TODO: It's weird why `min_bet` is Player's business
        self.balance = balance
        self.bet = 0
        self.min_bet = min_bet
        super().__init__()

    def bankrupted(self) -> bool:
        return self.balance < self.min_bet

    def make_bet(self, bet: int = 10) -> bool:
        """Make a new bet if the player has enough balance."""
        if not self.bankrupted():
            print(f" >> {self.__class__.__name__} balance ${self.balance:,.0f}")
            self.bet = bet
            self.balance -= self.bet
            print(f" >> {self.__class__.__name__} bet ${self.bet:,.0f}")
            return True
        else:
            print(f" >> Player bankrupted :(")
            print(f" >> Remaining balance ${self.balance:,.0f}")
            return False

    def human_draw_new_card(self) -> bool:
        """Hit new card operated from the keyboard."""
        # TODO: this should be "Hand's" operation
        players_input = input("Next card?")
        return len(players_input) == 0

    def primitive_auto_draw_new_card(self) -> bool:
        """Hit new card if hand value is less than 17."""
        return self.hand_value() < 17

    def hand_of_pairs(self) -> bool:
        """Check if the player has hand of pairs e.g., 5s."""
        if len(self.hand) == 2:
            card_0 = self.hand[0]
            card_1 = self.hand[1]
            return card_0.rank == card_1.rank
        else:
            return False

class Dealer(Participant):
    def print_hand(self, second_card_hidden: bool = True) -> None:
        if second_card_hidden:
            print(f"{self.__class__.__name__} hand: {self.hand[0]}")
        else:
            super().print_hand()

    def hand_value(self, second_card_hidden: bool = False) -> int:
        if second_card_hidden:
            return self.hand[0].card_value()
        else:
            return super().hand_value()

    def print_hand_value(self, second_card_hidden: bool = True) -> None:
        print(
            f"{self.__class__.__name__} value: {self.hand_value(second_card_hidden=second_card_hidden)}"
        )

    def print_hand_and_value(self, second_card_hidden: bool = True) -> None:
        self.print_hand(second_card_hidden=second_card_hidden)
        self.print_hand_value(second_card_hidden=second_card_hidden)

    def first_card_ace(self) -> bool:
        return self.hand[0].rank == 12