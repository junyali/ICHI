# 18/12/2024

## // Imports \\ ##
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import sys
import pygame
import random
import timeit

## // Constants \\ ##
colours = [
    "red",
    "yellow",
    "green",
    "blue",
]

values = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "skip",
    "reverse",
    "draw_2",
    "wild",
    "draw_4",
]

## // Classes \\ ##

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

    def __init__(self, value: str, colour: str):
        self.value = value
        self.colour = colour
        # self.action = action

    def get_info(self):
        return "[{}, {}]".format(self.value.upper(), self.colour.upper())

    def set_colour(self, new_colour: str):
        self.colour = new_colour

    def set_value(self, new_value: str):
        self.value = new_value

    def can_play(self, top_card):
        return (

            self.colour == top_card.colour or
            self.value == top_card.value or
            self.colour == "colourless"

        )

class Deck:
    def __init__(self):
        self.deck = []
        for colour in colours:
            for value in values:
                if value == "wild" or value == "draw_4":
                    self.deck.append(Card(value, "colourless"))
                elif value == "0":
                    self.deck.append(Card(value, colour))
                else:
                    for i in range(2):
                        self.deck.append(Card(value, colour))
        random.shuffle(self.deck)
class Game:
    def __init__(self):
        self.deck = Deck()

if __name__ == '__main__':
    deck = Deck()
    for d in deck.deck:
        print(d.get_info())