# 18/12/2024

## // Imports \\ ##
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import sys
import pygame
import random
import timeit

## // Constants \\ ##
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

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
        return [self.value, self.colour]

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
    def __init__(self, players):
        self.deck = Deck()
        self.discard = []
        self.players = players
        self.current_player = 0
        self.direction = "clockwise"

    def return_current_player(self):
        for player in self.players:
            if player.player_id == self.current_player:
                return player


def main():

    """
    old

    pygame.init()
    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    deck = Deck()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))

        sheet = pygame.image.load("./assets/spritesheets/standard_card_pack.png")
        pos_x, pos_y = 0, 0

        count = 0

        for card in deck.deck:
            card_info = card.get_info()
            if card_info[1] == "colourless":
                pos_x = 3120
                if card_info[0] == "wild":
                    pos_y = 0
                elif card_info[0] == "draw_4":
                    pos_y = 1440
            elif card_info[1] == "red":
                pos_y = 0
            elif card_info[1] == "yellow":
                pos_y = 360
            elif card_info[1] == "green":
                pos_y = 720
            elif card_info[1] == "blue":
                pos_y = 1080

            if card_info[1] != "colourless":
                pos_x = values.index(card_info[0]) * 240

            sheet.set_clip(pygame.Rect(pos_x, pos_y, 240, 360))
            draw = sheet.subsurface(sheet.get_clip())
            draw = pygame.transform.scale(draw, (240, 360))

            backdrop = pygame.Rect(count * 160, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

            screen.blit(draw, backdrop)

            count += 1

        pygame.display.flip()

    pygame.quit()
    sys.exit(0)
    """

    player_number = int(input("How many players are there? >> "))
    players = []

    for i in range(0, player_number):
        player_name = input("Player {}, what's your name? >> ".format(i + 1))
        players.append(Human(player_name, i))

    Round = Game(players)

    for player in Round.players:
        for i in range(7):
            player.hand.append(Round.deck.deck.pop(-1))

    Round.discard.append(Round.deck.deck.pop(-1))

    while True:
        player = Round.return_current_player()

        print("DISCARD Pile: {} {}".format(Round.discard[-1].get_info()[1].upper(), Round.discard[-1].get_info()[0].upper()))

        print("It is player {}'s turn.".format(str(player.name)))

        print("{}, you have the following {} cards in your hand: ".format(player.name,str(len(player.hand))))
        for card in player.hand:
            card_info = card.get_info()
            print("{} {}".format(card_info[1].upper(), card_info[0].upper()))

        card_playing = None
        valid = False

        while not valid:
            card_to_play = str(input("{}, which card would you like to play, or [draw] from the deck? >> ".format(player.name))).lower()

            if card_to_play == "draw":
                new_card = Round.deck.deck.pop(-1)
                player.hand.append(new_card)

                print("You drew {} {}".format(new_card.get_info()[1].upper(), new_card.get_info()[0].upper()))

                valid = True
                continue

            for card in player.hand:
                card_info = card.get_info()
                if "{colour} {value}".format(colour=card_info[1], value=card_info[0]) == card_to_play:
                    card_playing = card
                    break

            if card_playing is None:
                print("You do not have that card.")
                continue

            if card_playing.can_play(Round.discard[-1]):
                player.hand.pop(player.hand.index(card_playing))
                Round.discard.append(card_playing)

                if Round.discard[-1].get_info()[1] == "colourless":
                    colour_valid = False

                    while not colour_valid:
                        new_colour = str(input("What is the new colour ? >> ")).lower()

                        if new_colour in colours:
                            Round.discard[-1].set_colour(new_colour)
                            colour_valid = True
                        else:
                            print("That is not a valid colour.")

                if Round.discard[-1].get_info()[0] == "draw_2":
                    for i in range(2):
                        if Round.direction == "clockwise":
                            next_player = 0 if Round.current_player == len(Round.players) - 1 else Round.current_player + 1
                            Round.players[next_player].hand.append(Round.deck.deck.pop(-1))
                            Round.current_player = next_player
                        elif Round.direction == "anticlockwise":
                            next_player = len(Round.players) - 1 if Round.current_player == 0 else Round.current_player - 1
                            Round.players[next_player].hand.append(Round.deck.deck.pop(-1))
                            Round.current_player = next_player
                elif Round.discard[-1].get_info()[0] == "draw_4":
                    for i in range(4):
                        if Round.direction == "clockwise":
                            next_player = 0 if Round.current_player == len(Round.players) - 1 else Round.current_player + 1
                            Round.players[next_player].hand.append(Round.deck.deck.pop(-1))
                            Round.current_player = next_player
                        elif Round.direction == "anticlockwise":
                            next_player = len(Round.players) - 1 if Round.current_player == 0 else Round.current_player - 1
                            Round.players[next_player].hand.append(Round.deck.deck.pop(-1))
                            Round.current_player = next_player
                elif Round.discard[-1].get_info()[0] == "skip":
                    if Round.direction == "clockwise":
                        Round.current_player = 0 if Round.current_player == len(Round.players) - 1 else Round.current_player + 1
                    elif Round.direction == "anticlockwise":
                        Round.current_player = len(Round.players) - 1 if Round.current_player == 0 else Round.current_player - 1
                elif Round.discard[-1].get_info()[0] == "reverse":
                    if Round.direction == "clockwise":
                        Round.direction = "anticlockwise"
                    elif Round.direction == "anticlockwise":
                        Round.direction = "clockwise"

                valid = True
            else:
                print("You can't play that card.")

        if len(player.hand) == 0:
            print("{} wins.".format(player.name))
            break

        if Round.current_player == len(Round.players) - 1:
            Round.current_player = 0
        else:
            Round.current_player += 1


if __name__ == '__main__':
    main()