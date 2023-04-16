from .card import Card
from .deck import Deck
from .hand import Hand
from .participant import Player, Dealer


class Game:
    MIN_BET = 10
    DECKS = 6

    def __init__(self) -> None:
        self.dealer = Dealer("Dealer")
        self.player = Player(name="Player 1", balance=1_000)
        self.deck = Deck(decks=self.DECKS)
        self.game_count = 0
        self.already_played_cards: list[Card] = []  # TODO: save played cards

    def _reset_hands(self) -> None:
        self.dealer.new_hand()
        self.player.new_hand()
        self.player.reset_played_hands()
        self.player.split_count = 0

    def _draw_new_card_from_deck(self, hand: Hand) -> None:
        """
        Draw new card from the deck and stick it in the hand.
        """
        hand.cards.append(self.deck.cards.pop())

    def _deal_the_cards(self) -> None:
        """
        Deal the cards at the beginning of the round.
        """
        for _ in range(2):
            for hand in self.player.hands + [self.dealer.hand]:
                self._draw_new_card_from_deck(hand)

        print(" >> Deal the cards")

        self.dealer.hand.print_hand_and_hand_value(
            msg=f"{self.dealer.name}", second_card_hidden=True
        )

        for players_hand in self.player.hands:
            players_hand.print_hand_and_hand_value(msg=f"{self.player.name}")

        print(" >> Play <<")

    def _evaluate_hand(self, player: Player, players_hand: Hand) -> None:
        """
        Evaluate player's hand.
        """
        # TODO: Check this method carefully!
        # What if player doubled down?

        players_hand.print_hand_and_hand_value(
            msg=f"Evaluate {self.player.name}"
        )

        if players_hand.busted():
            print(" >> Player busted")
            print(f" >> Dealer won [losing ${player.bet:,.0f}]")
            player.loosings_count += 1

        elif self.dealer.hand.busted():
            prize = 2 * player.bet
            player.balance += prize
            print(" >> Dealer busted")
            print(f" >> Player won [winning ${prize:,.0f}]")
            player.winnings_count += 1

        elif players_hand.hand_value() == self.dealer.hand.hand_value():
            player.balance += player.bet
            print(" >> Draw")
            player.draws_count += 1

        elif (
            players_hand.black_jack() and not players_hand.black_jack_dislabled
        ):
            # TODO: BlackJack payout won't work if the dealer busted (step 2)
            prize = 2.5 * player.bet
            player.balance += prize
            print(f" >> Black Jack 21!!! [winning ${prize:,.0f}]")
            player.winnings_count += 1

        elif players_hand.hand_value() > self.dealer.hand.hand_value():
            prize = 2 * player.bet
            player.balance += prize
            print(" >> Player higher cards")
            print(
                f" >> {player.__class__.__name__} won! [winning ${prize:,.0f}]"
            )
            player.winnings_count += 1

        else:
            print(" >> Dealer higher cards")
            print(f" >> Dealer won [losing ${player.bet:,.0f}]")
            player.loosings_count += 1

    def _double_down(self, player: Player, hand: Hand) -> bool:
        """
        Check if double down is good choice.
        If yes, then double down with player's hand.
        """
        if (
            self.player.balance > self.player.bet
            and 6 < hand.hand_value() < 12
            and self.dealer.hand.hand_value(second_card_hidden=True) < 7
        ):
            print(f" >> Doubleeee down, betting ${self.player.bet:,.0f}")
            self.player.balance -= self.player.bet
            self.player.bet += self.player.bet
            # TODO: What if you change global self.player.bet value?
            # There will be conflict if you split and then double
            # one of two hands.
            self._draw_new_card_from_deck(hand)  # draw only one new card
            hand.print_hand_and_hand_value(msg=f"{player.name}")
            player.played_hands.append(hand)
            return True
        else:
            return False

    def _split_pairs(self, player: Player, hand: Hand) -> bool:
        """
        Check if splitting pairs is a good idea.
        If yes, then split the pairs.
        """
        if player.balance > player.bet and player.split_count < 3:
            player.make_bet(bet=player.bet)
            print(" >> Split the cards")

            left_hand = Hand(cards=[hand.cards[0]])
            self._draw_new_card_from_deck(hand=left_hand)
            left_hand.print_hand_and_hand_value(msg="Player's left hand")

            right_hand = Hand(cards=[hand.cards[1]])
            self._draw_new_card_from_deck(hand=right_hand)
            right_hand.print_hand_and_hand_value(msg="Player's right hand")

            # Black Jack in the Split is counted as 21, not as BJ
            for new_hand in [left_hand, right_hand]:
                if new_hand.black_jack():
                    new_hand.black_jack_dislabled = True

            # Aces can be split only once with one drawn card only
            if hand.hand_of_double_aces():
                player.played_hands += [right_hand, left_hand]
            else:
                player.hands += [right_hand, left_hand]
                player.split_count += 1
            return True
        else:
            print(" >> Not enought balance for split")
            print(" >> Max split count 3 times per hand")
            return False

    def _players_turn(self, player: Player) -> None:
        """
        Player's turn.
        """
        while player.hands:
            hand: Hand = player.hands.pop(0)
            hand.print_hand_and_hand_value(msg=f"Play {player.name}")

            # TODO: Refactor this waterfall if-else
            # split the pairs
            if hand.hand_of_pairs():
                if self._split_pairs(player, hand):
                    continue  # exit
                else:
                    pass  # continue as standard hand

            # double down
            if self._double_down(player, hand):
                continue  # exit

            # standard hand
            # TODO: pack this code into a method _standard_hand()
            while hand.hand_value() < 21 and player.draw_new_card(
                mode="auto primitive", hand=hand
            ):
                self._draw_new_card_from_deck(hand)
                hand.print_hand_and_hand_value(msg=f"{player.name}")

            player.played_hands.append(hand)

    def _dealers_turn(self) -> None:
        """
        Dealer's turn.
        """
        all_hands_busted = min(
            list(map(lambda h: h.busted(), self.player.played_hands))
        )

        if not all_hands_busted:
            while self.dealer.hand.hand_value(second_card_hidden=False) < 17:
                self._draw_new_card_from_deck(hand=self.dealer.hand)

    def _new_game(self) -> bool:
        """
        Play one round of the BlackJack.
        """
        print("------------NewGame------------")
        if self.player.make_bet(bet=Game.MIN_BET):
            self._reset_hands()
            self._deal_the_cards()

            self._players_turn(player=self.player)
            self._dealers_turn()

            self.dealer.hand.print_hand_and_hand_value(
                msg=f"{self.dealer.name}", second_card_hidden=False
            )

            print(" >> Evaluate <<")
            for players_hand in self.player.played_hands:
                self._evaluate_hand(
                    player=self.player, players_hand=players_hand
                )
            return True
        else:
            print("--------------End--------------")
            return False

    def _deck_below_threshold(self) -> bool:
        """
        Check if there are enough remaining cards in the deck.
        """
        THRESHOLD = 0.2
        init_deck_cards_count = self.DECKS * 52
        deck_below_threshold = (
            len(self.deck) / init_deck_cards_count
        ) < THRESHOLD
        if deck_below_threshold:
            print(f"Deck has less than {THRESHOLD:.0%}, last game.")
            return True
        else:
            return False

    def _print_summary(self) -> None:
        """
        Print the game summary.
        """
        print("-------------------------------")
        print("------------Summary------------")
        print("-------------------------------")
        print(f"Games : {self.game_count}")
        print(f"Player balance : ${self.player.balance:,.0f}")
        print("-------------------------------")

    def play_game(self):
        """
        Play the game until ending conditions are met.
        """
        while self.player.balance > self.MIN_BET and self.game_count < 1_000:
            while not self._deck_below_threshold():
                if not self._new_game():
                    break
                self.game_count += 1
            self._print_summary()
            self.deck = Deck(decks=self.DECKS)

        played_hands = (
            self.player.winnings_count
            + self.player.loosings_count
            + self.player.draws_count
        )
        print(f"Winnings: {self.player.winnings_count/played_hands:,.1%}")
        print(f"Loosings: {self.player.loosings_count/played_hands:,.1%}")
        print(f"Draws: {self.player.draws_count/played_hands:,.1%}")
        print("-------------------------------")
        played_hands = self.player.winnings_count + self.player.loosings_count
        player_ratio = self.player.winnings_count / played_hands
        house_ratio = self.player.loosings_count / played_hands
        print(f"Player vs House: {player_ratio:,.1%} : {house_ratio:,.1%}")
        print("-------------------------------")
        print("-------------------------------")
        print("--------------End--------------")
