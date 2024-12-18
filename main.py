# 18/12/2024

## // Imports \\ ##
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import sys
import pygame
import random
import timeit

class Player:

    def __init__(self, name: str, player_id: int):
        self.name = name
        self.player_id = player_id

        self.hand = []

class Bot(Player):

    def __init__(self, name: str, player_id: int, intelligence: int):
        super().__init__(name, player_id)
        self.intelligence = intelligence

class Human(Player):

    def __init__(self, name: str, player_id: int):
        super().__init__(name, player_id)

class Card:

    def __init__(self, value: str, colour: str, action: str):
        self.value = value
        self.colour = colour
        self.action = action

    def can_play(self, top_card):
        return (

            self.colour == top_card.colour or
            self.value == top_card.value or
            self.colour == "colourless"

        )


if __name__ == '__main__':
    print("Hello ICHI!")