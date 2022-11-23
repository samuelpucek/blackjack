from .card import Card
from .deck import Deck
from .hand import Hand
from .participant import Player, Dealer


class Game:
    MIN_BET = 10

    def __init__(self) -> None:
        self.dealer = Dealer("Dealer D")
        self.player = Player(
            name="Player 1", balance=100, min_bet=Game.MIN_BET
        )
        self.deck = Deck(decks=6)
        self.deck_init_length = len(self.deck)
        self.game_count = 0
        self.already_played_cards: list(Card) = []  # TODO: save played cards

    def _reset_hands(self) -> None:
        self.dealer.new_hand()
        self.player.new_hand()
        self.player.reset_played_hands()

    def _draw_new_card_from_deck(self, hand: Hand) -> None:
        hand.cards.append(self.deck.cards.pop())

    def _deal_the_cards(self) -> None:
        """
        Deal the cards at the beginning of the round.
        """
        players_hand: Hand = self.player.hands[0]
        dealers_hand: Hand = self.dealer.hands[0]

        self._draw_new_card_from_deck(hand=players_hand)
        self._draw_new_card_from_deck(hand=dealers_hand)
        self._draw_new_card_from_deck(hand=players_hand)
        self._draw_new_card_from_deck(hand=dealers_hand)

        print(" >> Deal the cards")
        dealers_hand.print_hand_and_hand_value(
            msg=f"{self.dealer.name}", second_card_hidden=True
        )
        players_hand.print_hand_and_hand_value(msg=f"{self.player.name}")
        print(" >> Go")

    def _evaluate_hand(self, player: Player, players_hand: Hand) -> None:
        dealers_hand: Hand = self.dealer.hands[0]

        if players_hand.busted():
            print(" >> Player busted")
            print(f" >> Dealer won [losing ${player.bet:,.0f}]")

        elif dealers_hand.busted():
            prize = 2 * player.bet
            player.balance += prize
            print(" >> Dealer busted")
            print(f" >> Player won [winning ${prize:,.0f}]")

        elif players_hand.hand_value() == dealers_hand.hand_value():
            player.balance += player.bet
            print(" >> Even game")

        elif players_hand.black_jack():
            prize = 2.5 * player.bet
            print(f" >> Black Jack 21!!! [winning ${prize:,.0f}]")
            player.balance += prize

        elif players_hand.hand_value() > dealers_hand.hand_value():
            prize = 2 * player.bet
            player.balance += prize
            print(" >> Player higher cards")
            print(
                f" >> {player.__class__.__name__} won! [winning ${prize:,.0f}]"
            )

        else:
            print(" >> Dealer higher cards")
            print(f"Dealer won [losing ${player.bet:,.0f}]")

    def _double_down(self, hand: Hand) -> bool:
        dealers_hand: Hand = self.dealer.hands[0]
        if (
            self.player.balance > self.player.bet
            and 6 < hand.hand_value() < 12
            and dealers_hand.hand_value(second_card_hidden=True) < 7
        ):
            print(f" >> Doubleeee down, betting ${self.player.bet:,.0f}")
            self.player.balance -= self.player.bet
            self.player.bet += self.player.bet
            self._draw_new_card_from_deck(hand)  # draw only one new card
            return True
        else:
            return False

    def _split_pairs(self, player: Player, hand: Hand) -> bool:
        if player.make_bet(bet=Game.MIN_BET):
            print(" >> Split the cards")
            left_hand = Hand(cards=[hand.cards[0]])
            self._draw_new_card_from_deck(hand=left_hand)
            left_hand.print_hand_and_hand_value(msg="Player's left hand")

            right_hand = Hand(cards=[hand.cards[1]])
            self._draw_new_card_from_deck(hand=right_hand)
            right_hand.print_hand_and_hand_value(msg="Player's right hand")

            player.hands = [right_hand, left_hand] + player.hands

            return True
        else:
            print(" >> Not enought balance for split")
            return False

    def _players_turn(self, player: Player) -> None:
        while player.hands:
            hand: Hand = player.hands.pop(0)
            hand.print_hand_and_hand_value(msg=f"{player.name}")

            # split the pairs
            if hand.hand_of_pairs():
                if self._split_pairs(player, hand):
                    continue  # exit
                else:
                    pass  # continue as standard hand

            # double down
            if self._double_down(hand):
                hand.print_hand_and_hand_value(msg=f"{player.name}")
                player.played_hands.append(hand)
                continue  # exit

            # standard hand
            while (
                not hand.busted()
                and not hand.black_jack()
                and hand.hand_value() < 21
                and player.draw_new_card(mode="auto primitive", hand=hand)
            ):
                self._draw_new_card_from_deck(hand)
                hand.print_hand_and_hand_value(msg=f"{player.name}")

            player.played_hands.append(hand)

    def _dealers_turn(self) -> None:
        all_hands_busted = True
        for players_hand in self.player.played_hands:
            all_hands_busted = min(all_hands_busted, players_hand.busted())

        if not all_hands_busted:
            dealers_hand: Hand = self.dealer.hands[0]
            while dealers_hand.hand_value(second_card_hidden=False) < 17:
                self._draw_new_card_from_deck(hand=self.dealer.hands[0])

    def _new_game(self) -> bool:
        print("------------NewGame------------")
        if self.player.make_bet(bet=Game.MIN_BET):
            self._reset_hands()
            self._deal_the_cards()

            self._players_turn(player=self.player)
            self._dealers_turn()

            dealers_hand: Hand = self.dealer.hands[0]
            dealers_hand.print_hand_and_hand_value(
                msg=f"{self.dealer.name}", second_card_hidden=False
            )

            for players_hand in self.player.played_hands:
                self._evaluate_hand(
                    player=self.player, players_hand=players_hand
                )
            return True
        else:
            print("--------------End--------------")
            return False

    def _deck_below_threshold(self) -> bool:
        THRESHOLD = 0.2
        deck_below_threshold = (
            len(self.deck) / self.deck_init_length
        ) < THRESHOLD
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
