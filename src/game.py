from deck import Deck
from participant import Player, Dealer


class Game:
    def __init__(self) -> None:
        self.dealer = Dealer()
        self.player = Player(balance=100)
        self.deck = Deck()
        self.deck_init_length = len(self.deck)
        # TODO: save played cards
        self.played_cards = []

    def _reset_hands(self):
        self.dealer.empty_hand()
        self.player.empty_hand()

    def _draw_new_card(self, who) -> None:
        who.hand += [self.deck.cards.pop()]

    def _deal_the_cards(self):
        self._draw_new_card(self.player)
        self._draw_new_card(self.dealer)
        self._draw_new_card(self.player)
        self._draw_new_card(self.dealer)

        self.dealer.print_hand_and_value_start()
        self.player.print_hand_and_value()

    def _evaluate_game(self):
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

    def _new_game(self):
        print("------------NewGame------------")
        print(f" >> {self.player.__class__.__name__} balance ${self.player.balance}")
        self.player.bet = 10
        self.player.balance -= self.player.bet
        print(f" >> {self.player.__class__.__name__} bet ${self.player.bet}")

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

    def play_game(self):
        play_new_game = True
        deck_over_limit = False

        while play_new_game and not deck_over_limit:
            self._new_game()
            play_new_game = len(input("Play game?")) == 0
            deck_over_limit = (len(self.deck) / self.deck_init_length) < 0.25
            if deck_over_limit:
                print(f"{(len(self.deck) / self.deck_init_length):,.2f} deck status")
