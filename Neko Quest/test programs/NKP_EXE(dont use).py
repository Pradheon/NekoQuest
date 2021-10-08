#!/usr/bin/python
#
# Nekopara Minigame
# A minigame based off of Nekopara
#
# Released under the Creative Commons License

VERSION = "0.1"

#[Load Modules]
try:
    import sys
    import random
    import math
    import os
    import getopt
    import pygame
    from socket import *
    from pygame.locals import *
except ImportError(err):
    print("Couldn't load module. %s" % (err))
    sys.exit(2)

#[Resource Handling Functions]
def load_png(name):
    """load image and return image object"""
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

def redrawWindow():
    screen.fill((240, 216, 172))

def fade(width, height):
    fade = pygame.Surface((width, height))
    fade.fill((0, 0, 0))
    for alpha in range(0, 300):
        fade.set_alpha(alpha)
        redrawWindow()
        screen.blit(fade, (0, 0))
        pygame.display.update()
        pygame.time.delay(3)

#[Game Object Classes]
class Logo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('logo.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        #[function (methods) here]
        #[e.g. a function to calculate a new position]
        #[and a function to check if it hits the side]
        
class chibiChocola(pygame.sprite.Sprite):
    """A chibi character of Chocola that will move across the screen
    Returns: character object
    Function: update, calcnewpos
    Attributes:"""
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png('chibi cho.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        #[function (methods) here]
        #[e.g. a function to calculate a new position]
        #[and a function to check if it hits the side]

class chibiVanilla(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load('chibi van.png')
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        #[function (methods) here]
        #[e.g. a function to calculate a new position]
        #[and a function to check if it hits the side]

def main():
    #initialize screen
    pygame.init()
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('Nekopara Minigame')

    #fill bg
    bg = pygame.Surface(screen.get_size())
    bg = bg.convert()
    bg.fill((240, 216, 172))

    #blit to screen
    screen.blit(bg, (0, 0))
    pygame.display.flip()

    #Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

            screen.blit(bg, (0, 0))
            pygame.display.flip()


if __name__ == '__main__': main()
