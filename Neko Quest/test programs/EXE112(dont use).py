import os, sys
import pygame

if not pg.font:
    print("Warning: Fonts Disabled")
if not pg.mixer:
    print("Warning: Sound Disabled")

main_dir = os.path.split(os.path.abspath(__Nekopara_Minigame__))[0]
data_dir = os.path.join(main_dir, "images")

#functions for rss
def load_images(name, colorkey=None):
    fullname = os.path.join(data_dir, name)
    try:
        image = pg.image.load(fullname)
    except pg.error:
        print("Cannot load image:", fullname)
        raise SystemExit(str(geterror()))
    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()

def load_sound(name):
    class NoneSound:
        def play(self):
            pass

        if not pg.mixer or not pg.mixer.get_init():
            return NoneSound()
        fullname = os.path.join(data_dir, name)
        try:
            sound = pg.mixer.Sound(fullname)
        except pg.error:
            print("Cannot load sound: %s" % fullname)
            raise SystemExit(str(geterror()))
        return sound

#classes for objects
class Shi(pg.sprite.Sprite):
    """moves a chibi character on the screen, following the mouse"""

    def __init__(self):
        pg.sprite.Sprite.__init__(self) #sprite initializer
        self.image, self.rect = load_image("chibi shi.png", -1)
        self.meow = 0

    def update(self):
        """moves the chibi based on mouse position"""
        pose = pg.mouse.get_pos()
        self.rect.midtop = pos
        if self.meow:
            self.rect.move_ip(5, 10)

    def meow(self, target):
        """returns true if the chibi collides with target"""
        if not self.meow:
            self.meow = 1
            hitbox - self.rect.inflate(-5, 5)
            return hitbox.colliderect(target.rect)

    def unmeow(self):
        """called to pull chibi back"""
        self.meow = 0

class Cho(pg.sprite.Sprite):
    """moves the chibi chocola across the screen. it can sping when caught."""

    def __init__(self):
        pg.sprite.Sprite.__init__(self) #sprite initializer
        self.image, self.rect = load_image("chibi cho.png", -1)
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 10
        self.move = 9
        self.dizzy = 0

    def update(self):
        """walk or spin, depends on state of character"""
        if self.dizzy:
            self._sping()
        else:
            self._walk()

    def _walk(self):
        """moves the chr across the screen, turns at end"""
        newpos = self.rect.move((self.move, 0))
        if not self.area.contains(newpose):
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.move = -self.move
                newpose = self.rect.move((self.move, 0))
                self.image = pg.transform.flip(self.image, 1, 0)
            self.rect = newpose

    def _spin(self):
        """sping the chr"""
        center = self.rect.center
        self.diszzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pg.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def meowed(self):
        """this will cause chr to spin"""
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image

def main():
    """called when program starts. initializes everything, then runins in loop until fin"""
    #Initializes
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    pg.display.set_caption('Nekopara Minigame')
    pg.mouse.set_visible(0)

    #Create bg
    bg = pg.Surface(screen.get_size())
    bg = bg.convert()
    bg.fill((240, 216, 172))

    #Display Background
    screen.blit(bg, (0, 0))
    pg.display.flip()

    #Prepare objects
    clock = pg.time.Clock()
    whiff_sound = load_sound("vibrant_game_negative_affirmation.mp3")
    meow_sound = load_sound("Chocola-Nya-Audio.mp3")
    cho = Cho()
    shi = Shi()
    allsprites = pg.sprite.RenderPlain((shi, cho))

    #Main loop
    going = True
    while going:
        clock.tick(60)

        #Input events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                going = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                if sho.meow(cho):
                    meow_sound.play() #meow
                    cho.meowed()
                else:
                    whiff_sound.play() #miss
            elif event.type == pg.MOUSEBUTTONUP:
                sho.unmeow()

        allsprites.update()

        #Draw everything
        screen.blit(bg, (0, 0))
        allsprited.draw(screen)
        pg.display.flip()

    pg.quit()

#Game Over

#calls 'main' function when executed
if __name__ == "__main__":
    main()
    
