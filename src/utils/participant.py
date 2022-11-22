from .hand import Hand


class Participant:
    def __init__(self) -> None:
        """One Participant can have one or multiple hands."""
        self.hands: list(Hand) = []
        self.played_hands: list(Hand) = []

    def new_hand(self) -> None:
        pass

    def print_hand(self, which_hand: int) -> None:
        """Print given Participants hand."""
        print(f"{self.__class__.__name__}'s {which_hand} hand: ", end="")
        self.hands[which_hand].print_hand()

    def hand_value(self, which_hand: int) -> int:
        """Return total value given Participants hand"""
        return self.hands[which_hand].hand_value()

    def print_hand_value(self, which_hand: int) -> None:
        print(
            f"{self.__class__.__name__}'s {which_hand} hand value: {self.hand_value(which_hand)}"  # noqa: E501
        )

    def print_hand_and_value(self, which_hand: int) -> None:
        self.print_hand(which_hand)
        self.print_hand_value(which_hand)

    def busted_hand(self, which_hand: int) -> bool:
        return self.hands[which_hand].busted()

    def black_jack(self, which_hand: int) -> bool:
        return self.hands[which_hand].black_jack()


class Player(Participant):
    def __init__(self, balance: int, min_bet: int) -> None:
        self.hands: list(Hand) = []
        self.played_hands: list(Hand) = []
        self.balance = balance
        self.bet = 0
        self.min_bet = min_bet

    def new_hand(self) -> None:
        self.hands = [Hand(cards=[])]

    def reset_played_hands(self) -> None:
        self.played_hands = []

    def _bankrupted(self) -> bool:
        return self.balance < self.min_bet

    def make_bet(self, bet: int) -> bool:
        """Make a new bet if the player has enough balance."""
        if not self._bankrupted():
            print(
                f" >> {self.__class__.__name__} balance ${self.balance:,.0f}"
            )
            self.bet = bet
            self.balance -= self.bet
            print(f" >> {self.__class__.__name__} bet ${self.bet:,.0f}")
            return True
        else:
            print(" >> Player bankrupted :(")
            print(f" >> Remaining balance ${self.balance:,.0f}")
            return False

    def draw_new_card(self, mode: str, hand: Hand) -> bool:
        if mode == "auto primitive":
            return hand.hand_value() < 17
        elif mode == "human":
            players_input = input("Next card?")
            return len(players_input) == 0
        else:
            raise ValueError("Not supported draw new card opperation.")

    def hand_of_pairs(self, which_hand: int) -> bool:
        return self.hands[which_hand].hand_of_pairs()


class Dealer(Participant):
    def __init__(self) -> None:
        self.hands: list(Hand) = []

    def new_hand(self) -> None:
        self.hands = [Hand(cards=[])]

    def print_hand(self, second_card_hidden: bool = True) -> None:
        if second_card_hidden:
            print(
                f"{self.__class__.__name__}'s 0 hand: {self.hands[0].cards[0]}"
            )
        else:
            super().print_hand(0)

    def hand_value(self, second_card_hidden: bool = True) -> int:
        if second_card_hidden:
            return self.hands[0].cards[0].card_value()
        else:
            return super().hand_value(which_hand=0)

    def print_hand_value(self, second_card_hidden: bool = True) -> None:
        print(
            f"{self.__class__.__name__}'s 0 hand value: {self.hand_value(second_card_hidden=second_card_hidden)}"  # noqa: E501
        )

    def print_hand_and_value(self, second_card_hidden: bool = True) -> None:
        self.print_hand(second_card_hidden=second_card_hidden)
        self.print_hand_value(second_card_hidden=second_card_hidden)

    def first_card_ace(self) -> bool:
        first_dealer_card = self.hands[0].cards[0]
        return first_dealer_card.rank == 12

    def busted_hand(self) -> bool:
        return super().busted_hand(0)
