from deck import Deck
from participant import Player, Dealer


class Game:
    MIN_BET = 10
    def __init__(self) -> None:
        self.dealer = Dealer()
        self.player = Player(min_bet=Game.MIN_BET)
        self.deck = Deck()
        self.deck_init_length = len(self.deck)
        self.game_count = 0
        # TODO: save played cards
        self.played_cards = []

    def _reset_hands(self) -> None:
        self.dealer.empty_hand()
        self.player.empty_hand()

    def _draw_new_card(self, who) -> None:
        # TODO: this is a bit weird that the "game" pushed player/dealer cards into the hand
        # IMHO the "hand" manipulation should be covered with internal nethod (in Participant)
        who.hand += [self.deck.cards.pop()]

    def _dealers_turn(self) -> None:
        if not self.player.busted():
            while self.dealer.hand_value(second_card_hidden=False) < 17:
                self._draw_new_card(self.dealer)

    def _players_turn(self) -> None:
        while (
            not self.player.busted()
            and not self.player.black_jack()
            and self.player.hand_value() < 21
            # and self.player.human_draw_new_card()
            and self.player.primitive_auto_draw_new_card()
        ):
            self._draw_new_card(self.player)
            self.player.print_hand_and_value()

    def _deal_the_cards(self) -> None:
        self._draw_new_card(self.player)
        self._draw_new_card(self.dealer)
        self._draw_new_card(self.player)
        self._draw_new_card(self.dealer)

        self.dealer.print_hand_and_value(second_card_hidden=True)
        self.player.print_hand_and_value()

    def _evaluate_game(self) -> None:
        if self.player.busted():
            print(f" >> Dealer won [losing ${self.player.bet:,.0f}]")

        elif self.dealer.busted():
            prize = 2 * self.player.bet
            self.player.balance += prize
            print(f" >> Player won [winning ${prize:,.0f}]")

        elif self.player.hand_value() == self.dealer.hand_value(second_card_hidden=False):
            self.player.balance += self.player.bet
            print(" >> Even game")

        elif self.player.black_jack():
            prize = 2.5 * self.player.bet
            print(f" >> Black Jack 21!!! [winning ${prize:,.0f}]")
            self.player.balance += prize

        elif self.player.hand_value() > self.dealer.hand_value(second_card_hidden=False):
            prize = 2 * self.player.bet
            self.player.balance += prize
            print(f" >> {self.player.__class__.__name__} won! [winning ${prize:,.0f}]")

        else:
            print(f"Dealer won [losing ${self.player.bet:,.0f}]")

    def _new_game(self) -> bool:
        print("------------NewGame------------")
        if self.player.make_bet():
            self._reset_hands()
            self._deal_the_cards()
            self._players_turn()
            self._dealers_turn()
            self.dealer.print_hand_and_value(second_card_hidden=False)
            self._evaluate_game()
            return True
        else:
            print("--------------End--------------")
            return False

    def _deck_below_threshold(self) -> bool:
        THRESHOLD = 0.2
        deck_below_threshold = (len(self.deck) / self.deck_init_length) < THRESHOLD
        if deck_below_threshold:
            print(f"Deck has less than {THRESHOLD:.0%}, last game.")
            return True
        else:
            return False

    def _play_new_game(self) -> bool:
        answer = input("Play new game? Press random key if exit.")
        return len(answer) == 0

    def _print_summary(self) -> None:
        print("------------Summary------------")
        print(f"Games : {self.game_count}")
        print(f"Player balance : ${self.player.balance:,.0f}")

    def play_game(self):
        while not self._deck_below_threshold():
            if not self._new_game():
                break
            self.game_count += 1
        self._print_summary()
