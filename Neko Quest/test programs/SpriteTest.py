import pygame
pygame.init()

win = pygame.display.set_mode((1280, 720))

pygame.display.set_caption("Test Sprites")

walkRight = [pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunR-0.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunR-1.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunR-2.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunR-3.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunR-4.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunR-5.png')]
walkLeft = [pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunL-0.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunL-1.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunL-2.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunL-3.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunL-4.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\RunL-5.png')]
jumpUp = [pygame.image.load(r'C:\Nekopara Minigame\images\sprites\Jump-0.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\Jump-1.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\Jump-2.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\Jump-3.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\Jump-4.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\Jump-5.png')]
bg = pygame.image.load(r'C:\Nekopara Minigame\images\bgLvl.png')
charR = [pygame.image.load(r'C:\Nekopara Minigame\images\sprites\StandR-0.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\StandR-1.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\StandR-2.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\StandR-3.png')]
charL = [pygame.image.load(r'C:\Nekopara Minigame\images\sprites\StandL-0.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\StandL-1.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\StandL-2.png'), pygame.image.load(r'C:\Nekopara Minigame\images\sprites\StandL-3.png')]

clock = pygame.time.Clock()

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

    def draw(self, win):
        if self.walkCount + 1 >= 18:
            self.walkCount = 0
            
        if self.left:
            win.blit(walkLeft[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif self.idleR:
            win.blit(charR[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1
        elif self.idleL:
            win.blit(charL[self.walkCount//3], (self.x, self.y))
            self.walkCount += 1

def redrawGameWindow():
    win.blit(bg, (0, 0))
    ko.draw(win)
    
    pygame.display.update()

ko = player(200, 410, 80, 80)
run = True
while run:
    clock.tick(18)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and ko.x > ko.vel:
        ko.x -= ko.vel
        ko.left = True
        ko.right = False
        ko.idle = False
    elif keys[pygame.K_RIGHT] and ko.x < 1280 - ko.w - ko.vel:
        ko.x += ko.vel
        ko.right = True
        ko.left = False
        ko.idle = False
    else:
        ko.right = False
        ko.left = False
        ko.idleR = True
        ko.walkCount = 0
        
    if not(ko.isJump):
        if keys[pygame.K_SPACE]:
            ko.isJump = True 
            ko.right = False
            ko.left = False
            ko.idle = False
            ko.walkCount = 0
    else:
        if ko.jumpCount >= -10:
            neg = 1
            if ko.jumpCount < 0:
                neg = -1
            ko.y -= (ko.jumpCount ** 2) * 0.5 * neg
            ko.jumpCount -= 1
        else:
            ko.isJump = False
            ko.jumpCount = 10
            
    redrawGameWindow()

pygame.quit()
