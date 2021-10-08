# !/usr/bin/python3.9
#
# Nekopara Minigame
# Based off of the Nekopara series developed by NEKOWORKs, published by Sekai Project
# Minigame developed by Joshan Rai
#
# Released under the Creative Commons License


# Load Modules
try:
    import sys
    import os
    import random
    import math
    import getopt
    import pygame
    from pygame.locals import *
    from pygame.sprite import Sprite
    from socket import *
except ImportError(err):
    print("Couldn't load module. %s" % (err))
    sys.exit(2)

# Version, Screen, Colors
VERSION = "0.1"


# Resource Handling Functions
def load_png(name):
    '''load image and return image object'''
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error(message):
        print("Cannot load image:", fullname)
        raise SystemExit(message)
    return image, image.get_rect()

def redrawScreen():
    screen.fill(self.NYALLOW)

def fade(width, height):
    fade = pygame.Surface((width, height))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        redrawScreen()
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(3)


# Game Object Classes
class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self. mid_h = self.display.DISPLAY_W / 2, self.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = - 100

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.screen.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self,starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_dislay = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.NYALLOW)
            self.game.draw_text('Neko Quest', 20, self.display.DISPLAY_W / 2, self.DISPLAY_H / 2 - 20)
            self.game.draw_text('Start', 20, self.startx, self.starty)
            self.game.draw_text('Options', 20, self.optionsx, self.optionsy)
            self.game.draw_text('Credits', 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()
            
    def  move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            self.run_display = False

class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Volume'
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlx, self.controly = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.NYALLOW)
            self.game.draw_text('Options', 20, self.display.DISPLAY_W / 2, self.DISPLAY_H / 2 - 30)
            self.game.draw_text("Volume", 15, self.volx, self.voly)
            self.game.draw_text("Controls", 15, self.controlx, self.controly)
            self.draw_cursor()
            self.blit_screen()

    def check_input():
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlx, + self.offset, self.controly)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            # Create Volume and Controls Menu
            pass

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.NYALLOW)
            self.game.draw_text('Credits', 20, self.display.DISPLAY_W / 2, self.DISPLAY_H / 2 - 20)
            self.game.draw_text('Made by Joshan Rai', 15, self.display.DISPLAY_W / 2, self.DISPLAY_H / 2 + 10)
            self.blit_screen()
    
class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1280, 720
        self.display = pygame.Surface(((self.display.DISPLAY_W, self.DISPLAY_H))
        self.screen = pygame.display.set_mode(((self.display.DISPLAY_W, self.DISPLAY_H)))
        self.font_name = '8-BIT WONDER.TTF'
        self.NYALLOW, self.NYARPLE, self.NYAGOLD, self.NYAHITE, self.NYALACK = (240, 216, 172), (84, 47, 67), (245, 197, 47), (255, 255, 255), (0, 0, 0)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            pygame.display.fill(self.NYALLOW)
            self.draw_text('Thanks for Playing', 20, self.display.DISPLAY_W / 2, self.DISPLAY_H / 2)
            self.screen.blit(self.display, (0, 0))
            pygame.display.update()
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if evetn.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
            if event.key == pygame.K_BACKSPACE:
                self.BACK_KEY = True
            if event.key == pygame.K_DOWN:
                self.DOWN_KEY = True
            if event.key == pygame.K_UP:
                self.UP_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.NYARPLE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

# Main Program
g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()
