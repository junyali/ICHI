# ICHI - A Card Game
A Python implementation of the fun board game UNO, in PyGame.

## How to run

### Requirements:

**Python3.12:** This program was written with Python3.12, though ICHI may be run on slightly older versions.

**PyGame:** Needed to display the GUI Interface for ICHI
```console
$ pip install pygame
```
**Windows 10 19044:** This program was written and tested on Windows 10, however ICHI may run on other operating systems provided they have the required packages.

Download the latest source  of the repository and simply run the following command:
```console
$ python main.py
```

## Info

- This game ONLY supports 2 players. There is internally support for more players, though this hasn't been implemented in PyGame yet
- Action cards are quite unreliable
  - Skip cards do not work as intended
  - Wild and draw 4 cards work with some flaws
- Clicks aren't unreliable
- This program is painfully slow
- After completing each turn, pass the machine to the other player to proceed to next turn
