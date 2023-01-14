from .hand import Hand


# TODO: try dataclass
class Participant:
    def __init__(self, name: str) -> None:
        """
        One Participant can have one or multiple hands.
        """
        self.name = name
        self.hands: list[Hand] = []

    def new_hand(self) -> None:
        """
        Initialize a new hand.
        """
        self.hands = [Hand(cards=[])]


class Player(Participant):
    def __init__(self, name: str, balance: int, min_bet: int) -> None:
        super().__init__(name)
        self.played_hands: list[Hand] = []
        self.balance = balance
        self.bet = 0
        self.min_bet = min_bet
        self.split_count = 0
        self.winnings_count = 0
        self.loosings_count = 0
        self.draws_count = 0

    def reset_played_hands(self) -> None:
        """
        Reset played hands.
        """
        self.played_hands = []

    def _bankrupted(self) -> bool:
        """
        Check if the player is bankrupted or not.
        """
        return self.balance < self.min_bet

    def make_bet(self, bet: int) -> bool:
        """
        Make a new bet if the player has enough balance.
        """
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
        """
        Return if the player should draw a new card or not.
        """
        if mode == "auto primitive":
            return hand.hand_value() < 17
        elif mode == "human":
            players_input = input("Next card?")
            return len(players_input) == 0
        else:
            raise ValueError("Not supported draw new card opperation.")


class Dealer(Participant):
    pass
