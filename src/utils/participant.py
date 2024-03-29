from .hand import Hand


class Player:
    def __init__(self, name: str, balance: int) -> None:
        self.name = name
        self.hands: list[Hand] = []
        self.played_hands: list[Hand] = []
        self.balance = balance
        self.bet: int = 0
        self.split_count: int = 0
        self.winnings_count: int = 0
        self.loosings_count: int = 0
        self.draws_count: int = 0

    def new_hand(self) -> None:
        """
        Initialize a new empty hand.
        """
        self.hands = [Hand(cards=[])]

    def reset_played_hands(self) -> None:
        """
        Reset played hands.
        """
        self.played_hands = []

    def make_bet(self, bet: int) -> bool:
        """
        Make a new bet if the player has enough balance.
        """
        if self.balance > bet:
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


class Dealer:
    def __init__(self, name: str) -> None:
        self.name = name
        self.hand = Hand(cards=[])

    def new_hand(self) -> None:
        """
        Initialize a new empty hand.
        """
        self.hand = Hand(cards=[])
