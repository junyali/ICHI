# 18/12/2024

## // Imports \\ ##
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import random
from playsound3 import playsound

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
        self.current_player_index = 0
        self.direction = "clockwise"
        self.game_over = False
        self.winner = None
        self.current_action = None
        self.confirm_next = True

        # Pygame stuff
        self.screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        self.clock = pygame.time.Clock()
        self.game_font = pygame.font.SysFont("Franklin Gothic Medium", 48)
        self.discard_rect = pygame.Rect(640 + (180 - 60), 360 - (90), 120, 180)
        self.draw_rect = pygame.Rect(640 - (180 + 60), 360 - (90), 120, 180)
        self.current_hand_card_rects = []
        self.colour_rects = [
            ("red", pygame.Rect(560, 280, 75, 75), (255, 85, 85)),
            ("blue", pygame.Rect(645, 280, 75, 75), (85, 85, 255)),
            ("green", pygame.Rect(560, 365, 75, 75), (85, 170, 85)),
            ("yellow", pygame.Rect(645, 365, 75, 75), (255, 170, 0))
        ]
        self.confirm_rect = pygame.Rect(0, 0, 1280, 160)

    def return_current_player(self):
        return self.players[self.current_player_index]

    def return_next_player(self):
        if self.direction == "clockwise":
            return self.players[(self.current_player_index + 1) % len(self.players)]
        else:
            return self.players[(self.current_player_index - 1 + len(self.players)) % len(self.players)]

    def start_round(self):
        for player in self.players:
            for i in range(7):
                player.hand.append(self.deck.deck.pop(-1))

        self.discard.append(self.deck.deck.pop(-1))

    def update_game_state(self):
        if self.game_over:
            return

        if not self.current_action:
            return

        current_player = self.return_current_player()

        if self.current_action[0] == "draw":
            if len(self.deck.deck) > 0:
                new_card = self.deck.deck.pop(-1)
                current_player.hand.append(new_card)
            self.current_action = None
            playsound("./assets/sfx/click_high.wav", False)
            self.confirm_next = False
            self.next_turn()
        elif self.current_action[1] and self.current_action[0].startswith("play"):
            card_to_play = self.current_action[1]
            print("b", card_to_play.get_info())

            if card_to_play in current_player.hand and card_to_play.can_play(self.discard[-1]):
                current_player.hand.remove(card_to_play)
                self.discard.append(card_to_play)

                # Handle special cards below
                card_info = card_to_play.get_info()
                print(card_info)
                if self.direction == "clockwise":
                    next_player = (self.current_player_index + 1) % len(self.players)
                else:
                    next_player = (self.current_player_index - 1 + len(self.players)) % len(self.players)
                next_player = self.players[next_player]

                if card_info[0] == "draw_2":
                    for _ in range(2):
                        if len(self.deck.deck) > 0:
                            next_player.hand.append(self.deck.deck.pop(-1))
                            playsound("./assets/sfx/click_high.wav", False)
                    self.next_turn()
                elif card_info[0] == "draw_4":
                    for _ in range(4):
                        if len(self.deck.deck) > 0:
                            next_player.hand.append(self.deck.deck.pop(-1))
                    self.current_action = ("colour_change", None)
                    playsound("./assets/sfx/colourless.wav", False)
                elif card_info[0] == "wild":
                    self.current_action = ("colour_change", None)
                    playsound("./assets/sfx/colourless.wav", False)
                elif card_info[0] == "skip":
                    for _ in range(2):
                        self.next_turn()
                    playsound("./assets/sfx/click_high.wav", False)
                elif card_info[0] == "reverse":
                    self.direction = "anticlockwise" if self.direction == "clockwise" else "clockwise"
                    if len(self.players) == 2:
                        self.next_turn()
                    playsound("./assets/sfx/click_high.wav", False)

                if len(current_player.hand) == 0:
                    self.game_over = True
                    self.winner = current_player
                elif self.current_action[0] != "colour_change" or self.current_action[0] != "finish_colour":
                    self.next_turn()
            if self.current_action[0] != "colour_change" or self.current_action[0] == "finish_colour":
                self.confirm_next = False
                self.current_action = None
            self.current_hand_card_rects = []

            if len(self.deck.deck) <= 4:
                discarded = self.discard[:-1]
                self.discard = [self.discard[-1]]
                random.shuffle(discarded)
                self.deck.deck.extend(discarded)
        elif self.current_action[0] == "colour_change":
            pass
        elif self.current_action[0] == "finish_colour":
            self.confirm_next = False
            self.next_turn()
            self.current_action = None

    def next_turn(self):
        if self.direction == "clockwise":
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
        else:
            self.current_player_index = (self.current_player_index - 1 + len(self.players)) % len(self.players)

    def handle_event(self, event):
        if self.game_over:
            return
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if not self.confirm_next and self.confirm_rect.collidepoint(mouse_pos):
                self.confirm_next = True
            elif self.current_action and self.current_action[0] == "colour_change":
                for i, rect in enumerate(self.colour_rects):
                    if rect[1].collidepoint(mouse_pos):
                        self.discard[-1].set_colour(rect[0])
                        self.current_action = ("finish_colour", None)
                        playsound("./assets/sfx/select.wav", False)
                        break
            elif self.draw_rect.collidepoint(mouse_pos):
                playsound("./assets/sfx/draw.wav", False)
                self.current_action = ("draw", None)
            else:
                for i, rect in enumerate(self.current_hand_card_rects):
                    if rect[1].collidepoint(mouse_pos):
                        self.current_action = ("play", rect[0])
                        playsound("./assets/sfx/click_normal.wav", False)
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
        non_playing_player = self.return_next_player()
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
        for count, card in enumerate(playing_player.get_hand()):
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

        # Colour change
        if self.current_action and self.current_action[0] == "colour_change":
            for i, rect in enumerate(self.colour_rects):
                pygame.draw.rect(self.screen, rect[2], rect[1])
                print(1)

        if self.game_over:
            win_text = self.game_font.render(f"Player {self.winner.get_name()} wins!", True, (255, 255, 255))
            self.screen.blit(win_text,(640 - (win_text.get_rect().width / 2), 720 - (80 + win_text.get_rect().height)))

        pygame.display.update()
        self.clock.tick(FRAME_RATE)

    def display_confirm_next(self):
        self.screen.fill((20, 20, 20))
        pygame.draw.rect(self.screen, (255, 255, 255), (0, 0, 1280, 160))
        confirm_next_text = self.game_font.render("Please pass to the next player and click to confirm next turn", True, (0, 0, 0))
        self.screen.blit(confirm_next_text, (640 - (confirm_next_text.get_rect().width / 2), 20))

        pygame.display.update()
        self.clock.tick(FRAME_RATE)

    def render(self):
        if self.confirm_next or self.game_over:
            self.draw_grid()
        else:
            self.display_confirm_next()

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
    player_number = 2
    players = []

    for i in range(0, player_number):
        player_name = input("Player {}, what's your name? >> ".format(i + 1))
        players.append(Human(player_name, i))

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("ICHI")

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

if __name__ == '__main__':
    main()