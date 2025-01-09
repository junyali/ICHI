# 18/12/2024

## // Imports \\ ##
import os
from turtledemo.penrose import start

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import sys
import pygame
import random
import timeit

## // Constants \\ ##
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FRAME_RATE = 30

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

    def get_name(self):
        return self.name
    def get_hand(self):
        return self.hand

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
        self.game_over = False
        self.winner = None
        self.current_action = None


        # Pygame stuff
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.SysFont("Franklin Gothic Medium", 48)
        self.draw_rect = pygame.Rect(640 - (180 + 60) + 6, 360 - (90) - 6, 180, 90)
        self.discard_rect = pygame.Rect(640 + (180 - 60), 360 - (90), 120, 180)
        self.current_hand_card_rects = []

    def return_current_player(self):
        for player in self.players:
            if player.player_id == self.current_player:
                return player

    def return_opp_player(self):
        for player in self.players:
            if player.player_id != self.current_player:
                return player

    def start_round(self):
        for player in self.players:
            for i in range(7):
                player.hand.append(self.deck.deck.pop(-1))

        self.discard.append(self.deck.deck.pop(-1))

    def update_game_state(self):
        if self.game_over:
            return

        current_player = self.return_current_player()

        if self.current_action[0] == "draw":
            new_card = self.deck.deck.pop(-1)
            current_player.hand.append(new_card)
            self.current_action = None
            self.next_turn()
        elif self.current_action[1] and self.current_action[0].startswith("play"):
            card_to_play = self.current_action[1]

            if card_to_play.can_play(self.discard[-1]):
                played_card = current_player.hand.pop(current_player.hand.index(card_to_play))
                self.discard.append(played_card)

                # Handle special cards
                card_info = played_card.get_info()

                next_player = None
                if self.direction == "clockwise":
                    next_player = (self.current_player + 1) % len(self.players)
                else:
                    next_player = (self.current_player - 1 + len(self.players)) % len(self.players)
                next_player = self.players[next_player]

                if card_info[0] == "draw_2":
                    for _ in range(2):
                        next_player.hand.append(self.deck.deck.pop(-1))
                    self.next_turn()
                elif card_info[0] == "draw_4":
                    for _ in range(4):
                        next_player.hand.append(self.deck.deck.pop(-1))
                    self.next_turn()
                    # Colour change TBA
                    played_card.set_colour()
                elif card_info[0] == "wild":
                    # Colour change TBA
                    played_card.set_colour()
                elif card_info[0] == "skip":
                    for _ in range(2):
                        self.next_turn()
                elif card_info[0] == "reverse":
                    self.direction = "anticlockwise" if self.direction == "clockwise" else "clockwise"
                    if len(self.players) == 2:
                        self.next_turn()

                if len(current_player.hand) == 0:
                    self.game_over = True
                    self.winner = current_player
                else:
                    self.next_turn()

    def next_turn(self):
        if self.direction == "clockwise":
            self.current_player = (self.current_player + 1) % len(self.players)
        else:
            self.current_player = (self.current_player - 1 + len(self.players)) % len(self.players)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if self.draw_rect.collidepoint(mouse_pos):
                self.current_action = ("draw", None)
            else:
                for i, rect in enumerate(self.current_hand_card_rects):
                    if rect[1].collidepoint(mouse_pos):
                        self.current_action = ("play", rect[0])
                        break

    def draw_grid(self):
        # Fill background
        self.screen.fill((32, 128, 0))
        bg = pygame.image.load("./assets/img/background.png")
        self.screen.blit(bg, (0, 0))

        # DRAW Pile
        for i in range(4):
            draw_sheet = pygame.image.load("./assets/spritesheets/standard_card_face.png")
            draw_sheet = pygame.transform.scale(draw_sheet, (120, 180))
            self.screen.blit(draw_sheet, (640-(180+60) + (i * 2), 360-(90) - (i * 2)))

        # DISCARD Pile
        discard_sheet = pygame.image.load("./assets/spritesheets/standard_card_pack.png")
        discard_pos = get_card_sprite_pos(self.discard[-1].get_info())
        discard_sheet.set_clip(pygame.Rect(discard_pos[0], discard_pos[1], 240, 360))
        discard_sheet = discard_sheet.subsurface(discard_sheet.get_clip())
        discard_sheet = pygame.transform.scale(discard_sheet, (120, 180))
        # discard_sheet = pygame.transform.rotate(discard_sheet, random.randint(-10, 10))
        # ???
        self.screen.blit(discard_sheet, (640+(180-60), 360-(90)))

        # Non-playing Pile
        non_playing_player = self.return_opp_player()
        non_playing_text = self.game_font.render(non_playing_player.get_name(), True, (255, 255, 255))
        self.screen.blit(non_playing_text, (640 - (non_playing_text.get_rect().width / 2), 10))

        cards_amount = len(non_playing_player.get_hand())
        non_playing_index_spacing = 80
        start_pos_x = 640 - ((((cards_amount - 1) * non_playing_index_spacing) + 120) / 2)
        while start_pos_x < 0:
            non_playing_index_spacing -= 1
            if non_playing_index_spacing == 1:
                break
            start_pos_x = 640 - ((((cards_amount - 1) * non_playing_index_spacing) + 120) / 2)
        for i in range(cards_amount):
            card_sheet = pygame.image.load("./assets/spritesheets/standard_card_face.png")
            card_sheet = pygame.transform.scale(card_sheet, (120, 180))
            self.screen.blit(card_sheet, (start_pos_x + (i * non_playing_index_spacing), 60))

        # Playing Pile
        playing_player = self.return_current_player()
        playing_text = self.game_font.render(playing_player.get_name(), True, (255, 255, 255))
        self.screen.blit(playing_text, (640 - (playing_text.get_rect().width / 2), 720 - (10 + playing_text.get_rect().height)))

        cards_amount = len(playing_player.get_hand())
        playing_index_spacing = 80
        start_pos_x = 640 - ((((cards_amount - 1) * non_playing_index_spacing) + 120) / 2)
        while start_pos_x < 0:
            non_playing_index_spacing -= 1
            if non_playing_index_spacing == 1:
                break
            start_pos_x = 640 - ((((cards_amount - 1) * non_playing_index_spacing) + 120) / 2)
        count = 0
        for card in playing_player.get_hand():
            card_pos = get_card_sprite_pos(card.get_info())
            playing_card_sheet = pygame.image.load("./assets/spritesheets/standard_card_pack.png")
            playing_card_sheet.set_clip(pygame.Rect(card_pos[0], card_pos[1], 240, 360))
            playing_card_sheet = playing_card_sheet.subsurface(playing_card_sheet.get_clip())
            playing_card_sheet = pygame.transform.scale(playing_card_sheet, (120, 180))
            self.screen.blit(playing_card_sheet, (start_pos_x + (count * playing_index_spacing), 720 - (60 + 180)))
            if count - 1 != cards_amount:
                self.current_hand_card_rects.append((card, pygame.Rect(start_pos_x + (count * playing_index_spacing), 720 - (60 + 180), playing_index_spacing, 180)))
            else:
                self.current_hand_card_rects.append((card, pygame.Rect(start_pos_x + (count * playing_index_spacing), 720 - (60 + 180), 120, 180)))
            count += 1

        pygame.display.update()
        self.clock.tick(FRAME_RATE)

    def render(self):
        self.draw_grid()

def get_card_sprite_pos(card_info):
    pos_x, pos_y = 0, 0

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

    return pos_x, pos_y


def main():

    # Player count set to 2 for debug purposes
    # player_number = int(input("How many players are there? >> "))
    player_number = 2
    players = []

    for i in range(0, player_number):
        player_name = input("Player {}, what's your name? >> ".format(i + 1))
        players.append(Human(player_name, i))

    pygame.init()
    pygame.font.init()

    NewGame = Game(players)
    NewGame.start_round()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                NewGame.handle_event(event)

        NewGame.update_game_state()
        NewGame.render()

        '''
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
        '''

    pygame.quit()
    sys.exit(0)

    while True:

        if len(Round.deck.deck) <= 25:
            current = Round.deck.deck
            Round.deck = Deck()
            for card in current:
                Round.deck.deck.append(card)

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