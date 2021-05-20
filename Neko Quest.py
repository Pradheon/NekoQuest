# !/usr/bin/python3.9
#
# Neko Quest
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
pygame.mixer.init()

win = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Neko Quest")

walkRight = [pygame.image.load(r'C:\Neko Quest\images\sprites\RunR-0.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\RunR-1.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\RunR-2.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\RunR-3.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\RunR-4.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\RunR-5.png')]
walkLeft = [pygame.image.load(r'C:\Neko Quest\images\sprites\RunL-0.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\RunL-1.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\RunL-2.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\RunL-3.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\RunL-4.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\RunL-5.png')]
jumpUp = [pygame.image.load(r'C:\Neko Quest\images\sprites\Jump-0.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\Jump-1.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\Jump-2.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\Jump-3.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\Jump-4.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\Jump-5.png'),
    pygame.image.load(r'C:\Neko Quest\images\sprites\Jump-6.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\Jump-7.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\Jump-8.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\Jump-9.png')]
bg = pygame.image.load(r'C:\Neko Quest\images\bgLvl.png')
charR = [pygame.image.load(r'C:\Neko Quest\images\sprites\StandR-0.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\StandR-1.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\StandR-2.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\StandR-3.png')]
charL = [pygame.image.load(r'C:\Neko Quest\images\sprites\StandL-0.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\StandL-1.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\StandL-2.png'), pygame.image.load(r'C:\Neko Quest\images\sprites\StandL-3.png')]

walkRightM = [pygame.image.load(r'C:\Neko Quest\images\sprites2\RunRm-0.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunRm-1.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunRm-2.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunRm-3.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunRm-4.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunRm-5.png')]
#walkLeftM = [pygame.image.load(r'C:\Neko Quest\images\sprites2\RunLm-0.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunLm-1.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunLm-2.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunLm-3.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunLm-4.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunLm-5.png')]

cl = pygame.time.Clock()
#score = 0

hitSound = pygame.mixer.Sound(r'C:\Neko Quest\sounds\Chocola_Nya.mp3')
bgm = pygame.mixer.music.load(r'C:\Neko Quest\sounds\Cyberangel (Instrumental).mp3')
pygame.mixer.music.play(-1)


# Resource Handling Functions
def redrawScreen():
    screen.fill(NYARPLE)

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
        self.jump = False
        self.left = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = 10
        self.idle = True
        self.hitbox = (self.x + 22, self.y + 5, 35, 75) #(top left x, top left y, width, height)

    def draw(self, win):
        if self.walkCount + 1 >= 32:
            self.walkCount = 0

        if not(self.idle):
            if self.right:
                win.blit(walkRight[self.walkCount//8], (self.x, self.y))
                self.walkCount += 1
            elif self.left:
                win.blit(walkLeft[self.walkCount//8], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(charR[self.walkCount//8], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(charL[self.walkCount//8], (self.x, self.y))
                self.walkCount += 1
        self.hitbox = (self.x + 22, self.y + 5, 35, 75)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit(self):
        self.isJump = False
        self.jumpCount = 10
        self.x = 100
        self.y = 500
        self.walkCount = 0
        font1 = pygame.font.SysFont('8-bit-pusab.ttf', 100)
        txt = font1.render("-5", 1, (255, 0, 0))
        win.blit(txt, (250 - (txt.get_width() / 2), 200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()


class neko(object):
    walkRightM = [pygame.image.load(r'C:\Neko Quest\images\sprites2\RunRm-0.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunRm-1.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunRm-2.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunRm-3.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunRm-4.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunRm-5.png')]
    walkLeftM = [pygame.image.load(r'C:\Neko Quest\images\sprites2\RunLm-0.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunLm-1.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunLm-2.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunLm-3.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunLm-4.png'), pygame.image.load(r'C:\Neko Quest\images\sprites2\RunLm-5.png')]

    def __init__(self, x, y, w, h, end):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.path = [x, end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 22, self.y + 10, 35, 70)
        self.health = 10
        self.visible = True

    def draw(self, win):
        self.move()
        if self.visible:
            if self.walkCount + 1 >= 32:
                self.walkCount = 0

            if self.vel > 0:
                win.blit(walkRightM[self.walkCount//8], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeftM[self.walkCount//8], (self.x, self.y))
                self.walkCount += 1
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 128, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - (5 * (10 - self.health)), 10))
            self.hitbox = (self.x + 22, self.y + 10, 35, 70)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def move(self):
        if self.vel > 0:
            if self.x < self.path[1] + self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0
        else:
            if self.x > self.path[0] - self.vel:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.x += self.vel
                self.walkCount = 0

    def hit(self):
        hitSound.play()
        if self.health > 0:
            self.health -= 1
        else:
            self.visible = False
        print("hit")


class projectile(object):
    def __init__(self, x, y, r, color, facing):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.vel = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.r)


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
            self.game.bgS = pygame.image.load(r'C:\Neko Quest\images\bgStart.png').convert()
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
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.bgO = pygame.image.load(r'C:\Neko Quest\images\bgOptions.png').convert()
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
            if self.state == 'Volume':
                self.game.curr_menu = self.game.volume
            if self.state == 'Controls':
                self.game.curr_menu = self.game.controls
            self.run_display = False

class VolumeMenu(Menu):
    #TO-DO: Implement Volume Controls as well as sound
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.options
                self.run_display = False
            self.game.bgCtrl = pygame.image.load(r'C:\Neko Quest\images\bgVol2.png').convert()
            self.game.display.blit(self.game.bgCtrl, (0, 0))
            self.game.draw_text('Coming Soon...', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2)
            self.blit_screen()

class ControlsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.options
                self.run_display = False
            self.game.bgCtrl = pygame.image.load(r'C:\Neko Quest\images\bgCtrl.png').convert()
            self.game.display.blit(self.game.bgCtrl, (0, 0))
            self.game.draw_text('Menu Controls', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 260)
            self.game.draw_text('UP KEY', 20, self.game.DISPLAY_W / 2 - 320, self.game.DISPLAY_H / 2 - 210)
            self.game.draw_text('Navigate Up', 20, self.game.DISPLAY_W / 2 + 320, self.game.DISPLAY_H / 2 - 210)
            self.game.draw_text('DOWN KEY', 20, self.game.DISPLAY_W / 2 - 320, self.game.DISPLAY_H / 2 - 160)
            self.game.draw_text('Navigate Down', 20, self.game.DISPLAY_W / 2 + 320, self.game.DISPLAY_H / 2 - 160)
            self.game.draw_text('ENTER', 20, self.game.DISPLAY_W / 2 - 320, self.game.DISPLAY_H / 2 - 110)
            self.game.draw_text('Start', 20, self.game.DISPLAY_W / 2 + 320, self.game.DISPLAY_H / 2 - 110)
            self.game.draw_text('BACKSPACE', 20, self.game.DISPLAY_W / 2 - 320, self.game.DISPLAY_H / 2 - 60)
            self.game.draw_text('Back', 20, self.game.DISPLAY_W / 2 + 320, self.game.DISPLAY_H / 2 - 60)
            self.game.draw_text('Player Controls', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 110)
            self.game.draw_text('LEFT KEY', 20, self.game.DISPLAY_W / 2 - 320, self.game.DISPLAY_H / 2 + 160)
            self.game.draw_text('Move Left', 20, self.game.DISPLAY_W / 2 + 320, self.game.DISPLAY_H / 2 + 160)
            self.game.draw_text('RIGHT KEY', 20, self.game.DISPLAY_W / 2 - 320, self.game.DISPLAY_H / 2 + 210)
            self.game.draw_text('Move Right', 20, self.game.DISPLAY_W / 2 + 320, self.game.DISPLAY_H / 2 + 210)
            self.game.draw_text('UP KEY', 20, self.game.DISPLAY_W / 2 - 320, self.game.DISPLAY_H / 2 + 260)
            self.game.draw_text('Jump', 20, self.game.DISPLAY_W / 2 + 320, self.game.DISPLAY_H / 2 + 260)
            self.game.draw_text('SPACEBAR', 20, self.game.DISPLAY_W / 2 - 320, self.game.DISPLAY_H / 2 + 310)
            self.game.draw_text('Shoot', 20, self.game.DISPLAY_W / 2 + 320, self.game.DISPLAY_H / 2 + 310)
            self.blit_screen()

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
            self.game.bgC = pygame.image.load(r'C:\Neko Quest\images\bgCredits.png').convert()
            self.game.display.blit(self.game.bgC, (0, 0))
            self.game.draw_text('Credits', 35, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 50)
            self.game.draw_text('Developed by Joshan Rai', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 10)
            self.game.draw_text('Artwork by NEKOWORKs', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 40)
            self.game.draw_text('Special Thanks', 25, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 120)
            self.game.draw_text('Aaroniter (Game Tester)', 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 + 160)
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
        self.font = pygame.font.SysFont('8-bit-pusab.ttf', 30, True)
        #self.font_name = pygame.font.get_default_font()
        self.NYALLOW, self.NYARPLE, self.NYAGOLD, self.NYAANGE = (240, 216, 172), (84, 47, 67), (245, 197, 47), (254, 154, 0)
        self.NYAREDO, self.NYAROWN, self.NYALACK, self.NYAHITE = (255, 76, 76), (239, 133, 83), (0, 0, 0), (255, 255, 255)
        self.main_menu = MainMenu(self)
        self.options = OptionsMenu(self)
        self.volume = VolumeMenu(self)
        self.controls = ControlsMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_menu = self.main_menu
        self.player = player(1200, 500, 80, 80)
        self.neko = neko(10, 500, 80, 80, 1200)
        self.shootLoop = 0
        self.bullets = []
        self.ko = self.player
        self.nk = self.neko
        self.score = 0

    def game_loop(self):
        while self.playing:
            cl.tick(30)

            if self.nk.visible == True:
                if self.ko.hitbox[1] < self.nk.hitbox[1] + self.nk.hitbox[3] and self.ko.hitbox[1] + self.ko.hitbox[3] > self.nk.hitbox[1]:
                    if self.ko.hitbox[0] + self.nk.hitbox[2] > self.nk.hitbox[0] and self.ko.hitbox[0] < self.nk.hitbox[0] + self.nk.hitbox[2]:
                        self.ko.hit()
                        self.score -= 5

            if self.shootLoop > 0:
                self.shootLoop += 1
            if self.shootLoop > 3:
                self.shootLoop = 0

            self.check_events()
            if self.BACK_KEY:
                self.playing = False

            for self.bullet in self.bullets:
                if self.bullet.y - self.bullet.r < self.neko.hitbox[1] + self.neko.hitbox[3] and self.bullet.y + self.bullet.r > self.neko.hitbox[1]:
                    if self.bullet.x + self.bullet.r > self.neko.hitbox[0] and self.bullet.x - self.bullet.r < self.neko.hitbox[0] + self.neko.hitbox[2]:
                        hitSound.play()
                        self.neko.hit()
                        self.score += 1
                        self.bullets.pop(self.bullets.index(self.bullet))
                if self.bullet.x < 1280 and self.bullet.x > 0:
                    self.bullet.x += self.bullet.vel
                else:
                    self.bullets.pop(self.bullets.index(self.bullet))

            if self.score == 11:
                #Find way to reset score, send to end screen, possibly draw more enemeies and make progressvely harder.
                self.score = 0

            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] and self.shootLoop == 0:
                if self.ko.left:
                    self.facing = -1
                else:
                    self.facing = 1
                if len(self.bullets) < 2:
                    self.bullets.append(projectile(round(self.ko.x + self.ko.w // 2), round(self.ko.y + self.ko.h // 2), 6, (0, 0, 0), self.facing))
                self.shootLoop = 1
            if keys[pygame.K_LEFT] and self.ko.x > self.ko.vel:
                self.ko.x -= self.ko.vel
                self.ko.left = True
                self.ko.right = False
                self.ko.idle = False
            elif keys[pygame.K_RIGHT] and self.ko.x < 1280 - self.ko.w - self.ko.vel:
                self.ko.x += self.ko.vel
                self.ko.right = True
                self.ko.left = False
                self.ko.idle = False
            else:
                self.ko.idle = True
                self.ko.jump = True

            if not(self.ko.isJump):
                if keys[pygame.K_UP]:
                    self.ko.isJump = True
                    self.ko.right = False
                    self.ko.left = False
                    self.ko.jump = True
            else:
                if self.ko.jumpCount >= -10:
                    neg = 1
                    if self.ko.jumpCount < 0:
                        neg = -1
                    self.ko.y -= (self.ko.jumpCount ** 2) * 0.5 * neg
                    self.ko.jumpCount -= 1
                else:
                    self.ko.isJump = False
                    self.ko.jumpCount = 10

            self.redrawGameWindow()
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
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.NYAREDO)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface,text_rect)

    def redrawGameWindow(self):
        win.blit(bg, (0, 0))
        self.txt = self.font.render("Score: " + str(self.score), 1, self.NYAGOLD)
        win.blit(self.txt, (10, 10))
        self.ko.draw(win)
        self.nk.draw(win)
        for self.bullet in self.bullets:
            self.bullet.draw(win)

        pygame.display.update()

# Main Program
g = Game()

while g.running:
    g.curr_menu.display_menu()
    g.game_loop()
    cl.tick(60)

pygame.quit()
