from deck import Deck
from participant import Participant, Player, Dealer


class Game:
    MIN_BET = 10

    def __init__(self) -> None:
        self.dealer = Dealer()
        self.player = Player(balance=100, min_bet=Game.MIN_BET)
        self.deck = Deck(decks=6)
        self.deck_init_length = len(self.deck)
        self.game_count = 0
        # TODO: save played cards
        self.played_cards = []

    def _reset_hands(self) -> None:
        self.dealer.new_hand()
        self.player.new_hand()

    def _draw_new_card_from_deck(self, who: Participant, which_hand: int) -> None:
        who.hands[which_hand].cards += [self.deck.cards.pop()]

    def _deal_the_cards(self) -> None:
        """Deal the cards at the beginning of the round."""
        self._draw_new_card_from_deck(who=self.player, which_hand=0)
        self._draw_new_card_from_deck(who=self.dealer, which_hand=0)
        self._draw_new_card_from_deck(who=self.player, which_hand=0)
        self._draw_new_card_from_deck(who=self.dealer, which_hand=0)

        self.dealer.print_hand_and_value(second_card_hidden=True)
        self.player.print_hand_and_value(which_hand=0)

    def _evaluate_hand(self, player: Player, hand: int) -> None:
        if player.busted_hand(hand):
            print(f" >> Player busted")
            print(f" >> Dealer won [losing ${player.bet:,.0f}]")

        elif self.dealer.busted_hand():
            prize = 2 * player.bet
            player.balance += prize
            print(f" >> Dealer busted")
            print(f" >> Player won [winning ${prize:,.0f}]")

        elif player.hand_value(hand) == self.dealer.hand_value(
            second_card_hidden=False
        ):
            player.balance += player.bet
            print(" >> Even game")

        elif player.black_jack(hand):
            prize = 2.5 * player.bet
            print(f" >> Black Jack 21!!! [winning ${prize:,.0f}]")
            player.balance += prize

        elif player.hand_value(hand) > self.dealer.hand_value(second_card_hidden=False):
            prize = 2 * player.bet
            player.balance += prize
            print(" >> Player higher cards")
            print(f" >> {player.__class__.__name__} won! [winning ${prize:,.0f}]")

        else:
            print(" >> Dealer higher cards")
            print(f"Dealer won [losing ${player.bet:,.0f}]")

    def _surrender(self) -> None:
        # print(" >> Anyone surrender?")
        pass

    def _double_down(self, which_hand: int) -> bool:
        if (
            self.player.balance > self.player.bet
            and self.player.hand_value(which_hand=which_hand) < 12
            and self.player.hand_value(which_hand=which_hand) > 6
            and self.dealer.hand_value(second_card_hidden=True) < 7
        ):
            print(f" >> Doubleeee down, betting ${self.player.bet:,.0f}")
            self.player.balance -= self.player.bet
            self.player.bet += self.player.bet
            self._draw_new_card_from_deck(who=self.player, which_hand=which_hand)
            return True
        else:
            return False

    def _split_pairs(self, which_hand: int) -> None:
        if self.player.hand_of_pairs(which_hand=which_hand):
            print(" >> Split the cards?")

    def _insurance(self) -> None:
        if self.dealer.first_card_ace():
            print(" >> Insurance anyone?")

    def _players_turn(self, which_hand: int) -> None:
        # double down
        if self._double_down(which_hand):
            self.player.print_hand_and_value(which_hand)
            return None  # exit

        # split the pairs
        self._split_pairs(which_hand)

        # standard turn
        while (
            not self.player.busted_hand(which_hand)
            and not self.player.black_jack(which_hand)
            and self.player.hand_value(which_hand) < 21
            and self.player.draw_new_card(mode="auto primitive", which_hand=which_hand)
        ):
            self._draw_new_card_from_deck(self.player, which_hand)
            self.player.print_hand_and_value(which_hand)

    def _dealers_turn(self) -> None:
        all_hands_busted = True
        for players_hand in self.player.hands:
            all_hands_busted = min(all_hands_busted, players_hand.busted())

        if not all_hands_busted:
            while self.dealer.hand_value(second_card_hidden=False) < 17:
                self._draw_new_card_from_deck(who=self.dealer, which_hand=0)

    def _new_game(self) -> bool:
        print("------------NewGame------------")
        if self.player.make_bet(bet=Game.MIN_BET):
            self._reset_hands()
            self._deal_the_cards()

            self._surrender()
            self._insurance()

            self._players_turn(which_hand=0)
            self._dealers_turn()

            self.dealer.print_hand_and_value(second_card_hidden=False)
            for which_hand, _ in enumerate(self.player.hands):
                self._evaluate_hand(self.player, which_hand)
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
