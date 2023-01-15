# blackjack

**Python project simulating casino banking game Blackjack.**

It provides Blackjack game with standard actions, i.e. hit, stand, double down, split, surrender and insurance.

## Further development

The goal is to add Reinforcement Learning agent on top of the game. The agent should learn how to play Blackjack on its own, and wisely use strategy when the game is "hot".

## Run and cotribute

To get started, clone the repo and use `Makefile` for quick environment setup.

```bash
git clone git@github.com:samuelpucek/blackjack.git
cd blackjack
make install
```

To run the game, do

```bash
make run
```

To run the unit tests and validate the code, do

```bash
make check
```