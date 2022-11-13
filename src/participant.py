from card import Card


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

    def hand_value(self, ace_as_one: bool = False) -> int:
        return sum([card.card_value(ace_as_one) for card in self.hand])

    def print_hand_value(self) -> None:
        print(f"{self.__class__.__name__} value: {self.hand_value()}")

    def print_hand_and_value(self) -> None:
        self.print_hand()
        self.print_hand_value()

    def busted(self) -> bool:
        return self.hand_value() > 21

    def black_jack(self) -> bool:
        return self.hand_value() == 21 and len(self.hand) == 2

    def ace_in_hand(self):
        ace_in_hand = False
        for card in self.hand:
            if card.is_ace_card():
                ace_in_hand = True
        return ace_in_hand

    def ace_in_hand_as_one(self) -> bool:
        return not self.black_jack() and self.ace_in_hand()


class Player(Participant):
    def __init__(self, balance: int = 100) -> None:
        self.balance = balance
        self.bet = 0
        super().__init__()

    def make_bet(self, bet: int = 10) -> None:
        """Make a new bet if the player has enough balance."""
        if self.balance >= bet:
            print(f" >> {self.__class__.__name__} balance ${self.balance}")
            self.bet = bet
            self.balance -= self.bet
            print(f" >> {self.__class__.__name__} bet ${self.bet}")
        else:
            print(f" >> Player bankrupted :(")
            print(f" >> Remaining balance ${self.balance}")

    def human_draw_new_card(self) -> bool:
        """Hit new card operated from the keyboard."""
        # TODO: this should be "Hand's" operation
        players_input = input("Next card?")
        return len(players_input) == 0

    def primitive_auto_draw_new_card(self) -> bool:
        """Hit new card if hand value is less than 17."""
        return self.hand_value() < 17

    # TODO: player has "Ace"


class Dealer(Participant):
    def print_hand(self, second_card_hidden: bool = True) -> None:
        if second_card_hidden:
            print(f"{self.__class__.__name__} hand: {self.hand[0]}")
        else:
            super().print_hand()

    def hand_value(self, second_card_hidden: bool = True) -> int:
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
