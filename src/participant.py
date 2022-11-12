from card import Card


class Participant:
    def __init__(self) -> None:
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
    def __init__(self, balance: int) -> None:
        self.balance = balance
        self.bet = 0
        super().__init__()

    def print_balance(self) -> None:
        print(f"${self.balance:,}")

    def draw_new_card(self) -> bool:
        players_input = input("Next card?")
        if len(players_input) == 0:
            return True
        else:
            return False

    # TODO: player has "Ace"


class Dealer(Participant):
    def print_hand_start(self) -> None:
        print(f"{self.__class__.__name__} hand: ", end="")
        print(self.hand[0])

    def hand_value_start(self) -> int:
        return self.hand[0].card_value()

    def print_hand_value_start(self) -> None:
        print(f"{self.__class__.__name__} value: {self.hand_value_start()}")

    def print_hand_and_value_start(self) -> None:
        self.print_hand_start()
        self.print_hand_value_start()

    def hand_value_game(self) -> int:
        if self.black_jack():
            return self.hand_value()
        else:
            return self.hand_value(self.ace_in_hand_as_one())

    def print_hand_value_game(self) -> None:
        print(f"{self.__class__.__name__} value: {self.hand_value_game()}")

    def print_hand_and_value_game(self) -> None:
        self.print_hand()
        self.print_hand_value_game()
