from deck import Deck
from participant import Player, Dealer


class Game:
    def __init__(self) -> None:
        self.dealer = Dealer()
        self.player = Player()
        self.deck = Deck()
        self.deck_init_length = len(self.deck)
        # TODO: save played cards
        self.played_cards = []

    def _reset_hands(self) -> None:
        self.dealer.empty_hand()
        self.player.empty_hand()

    def _draw_new_card(self, who) -> None:
        who.hand += [self.deck.cards.pop()]

    def _deal_the_cards(self) -> None:
        self._draw_new_card(self.player)
        self._draw_new_card(self.dealer)
        self._draw_new_card(self.player)
        self._draw_new_card(self.dealer)

        self.dealer.print_hand_and_value_start()
        self.player.print_hand_and_value()

    def _evaluate_game(self) -> None:
        if self.player.busted():
            print(f" >> Dealer won [losing ${self.player.bet:,.1f}]")

        elif self.dealer.busted():
            prize = 2 * self.player.bet
            self.player.balance += prize
            print(f" >> Player won [winning ${prize:,.1f}]")

        elif self.player.hand_value() == self.dealer.hand_value_game():
            self.player.balance += self.player.bet
            print(" >> Even game")

        elif self.player.black_jack():
            prize = 2.5 * self.player.bet
            print(f" >> Black Jack 21!!! [winning ${prize:,.1f}]")
            self.player.balance += prize

        elif self.player.hand_value() > self.dealer.hand_value_game():
            prize = 2 * self.player.bet
            self.player.balance += prize
            print(f" >> {self.player.__class__.__name__} won! [winning ${prize:,.1f}]")

        else:
            print(f"Dealer won [losing ${self.player.bet:,.1f}]")

    def _new_game(self) -> None:
        print("------------NewGame------------")
        self.player.make_bet()
        self._reset_hands()
        self._deal_the_cards()

        while (
            not self.player.busted()
            and not self.player.black_jack()
            and self.player.hand_value() < 21
            and self.player.draw_new_card()
        ):
            self._draw_new_card(self.player)
            self.player.print_hand_and_value()

        # self.dealer.print_hand_and_value()
        self.dealer.print_hand_and_value_game()

        if not self.player.busted():

            while self.dealer.hand_value_game() < 17:
                self._draw_new_card(self.dealer)

            self.dealer.print_hand_and_value_game()

        self._evaluate_game()

    def _deck_below_threshold(self) -> bool:
        THRESHOLD = 0.3
        deck_below_threshold = (len(self.deck) / self.deck_init_length) < THRESHOLD
        if deck_below_threshold:
            print(f"Deck has less than {THRESHOLD:.0%}, last game.")

    def _play_new_game(self) -> bool:
        answer = input("Play new game? Press random key if exit.")
        return len(answer) == 0

    def play_game(self):
        while self._play_new_game() and not self._deck_below_threshold():
            self._new_game()
