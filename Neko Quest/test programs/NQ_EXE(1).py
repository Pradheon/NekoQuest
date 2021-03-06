# !/usr/bin/python3.9
#
# Nekopara Minigame
# Based off of the Nekopara series developed by NEKOWORKs, published by Sekai Project
# Neko Quest developed by Joshan Rai
# Uses arrow keys to move
#
# Released under the Creative Commons License


# Load Modules
import sys
import os
import random
import math
import getopt
import pygame
import json
from pygame.locals import *
from pygame.sprite import Sprite
from socket import *


# Version, Clock, Images, Screen
VERSION = "0.1"

win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Neko Quest")

walkRight = [pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunR-0.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunR-1.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunR-2.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunR-3.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunR-4.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunR-5.png')]
walkLeft = [pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunL-0.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunL-1.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunL-2.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunL-3.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunL-4.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunL-5.png')]
jumpUp = [pygame.image.load(r'C:\Nekopara Minigame\images\sprites\Jump-0.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\Jump-1.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\Jump-2.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\Jump-3.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\Jump-4.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\Jump-5.png')]
bg = pygame.image.load(r'C:\Nekopara Minigame\images\bgLvl.png')
charR = [pygame.image.load(r'C:\Nekopara Minigame\images\sprites\StandR-0.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\StandR-1.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\StandR-2.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\StandR-3.png')]
charL = [pygame.image.load(r'C:\Nekopara Minigame\images\sprites\StandL-0.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\StandL-1.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\StandL-2.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\StandL-3.png')]

cl = pygame.time.Clock()


# Resource Handling Functions
def redrawScreen():
    screen.fill(NYARPLE)

def redrawGameWindow():
    self.window.blit(bg, (0, 0))
    ko.draw(self.window)

    pygame.display.update()

def fade(width, height):
    fade = pygame.Surface((width, height))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        redrawScreen()
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(3)


# Game Object Classes
class player(object):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vel = 5
        self.isJump = False
        self.left = False
        self.right = False
        self.idleR = False
        self.idleL = False
        self.walkCount = 0
        self.jumpCount = 10

    def draw(self, self.window):
        if self.walkCount + 1 >= 18:
            self.walkCount = 0

        if self.left:
            self.window.blit(walkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            self.window.blit(walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif self.idleR:
            self.window.blit(charR[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif self.idleL:
            self.window.blit(charL[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 15, 15)
        self.offset = - 90

    def draw_cursor(self):
        self.game.draw_text('>', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 40
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 80
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 120
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.bgS = pygame.image.load(r'C:\Nekopara Minigame\images\bgStart.png').convert()
            self.game.display.blit(self.game.bgS, (0, 0))
            self.game.draw_text('Neko Quest', 50, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 50)
            self.game.draw_text("Start", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
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
        self.volx, self.voly = self.mid_w, self.mid_h + 30
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.bgO = pygame.image.load(r'C:\Nekopara Minigame\images\bgOptions.png').convert()
            self.game.display.blit(self.game.bgO, (0, 0))
            self.game.draw_text('Options', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 40)
            self.game.draw_text("Volume", 20, self.volx, self.voly)
            self.game.draw_text("Controls", 20, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == 'Volume':
                self.state = 'Controls'
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == 'Controls':
                self.state = 'Volume'
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            # TO-DO: Create a Volume Menu and a Controls Menu
            pass

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.bgC = pygame.image.load(r'C:\Nekopara Minigame\images\bgCredits.png').convert()
            self.game.display.blit(self.game.bgC, (0, 0))
            self.game.draw_text('Credits', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 50)
            self.game.draw_text('Developed by Joshan Rai', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 20)
            self.blit_screen()

class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1280, 720
        self.display = pygame.Surface((self.DISPLAY_W,self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W,self.DISPLAY_H)))
        self.font_name = '8-bit-pusab.ttf'
        #self.font_name = pygame.font.get_default_font()
        self.NYALLOW, self.NYARPLE, self.NYAGOLD, self.NYAANGE = (240, 216, 172), (84, 47, 67), (245, 197, 47), (254, 154, 0)
        self.NYAREDO, self.NYAROWN, self.NYALACK, self.NYAHITE = (255, 76, 76), (239, 133, 83), (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu

    def game_loop(self):
        ko = player(200, 410, 80, 80)
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False
            self.bg = pygame.image.load(r'C:\Nekopara Minigame\images\bgLvl.png').convert()
            self.window.fill(self.NYARPLE)
            self.window.blit(self.bg, (0, 0))
            pygame.display.update()
            self.reset_keys()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
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

    def draw_text(self, text, size, x, y ):
        font = pygame.font.Font(self.font_name,size)
        text_surface = font.render(text, True, self.NYAREDO)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

# Main Program
g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()
    cl.tick(FPS)
