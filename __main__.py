import pygame
import numpy
import math
import os 
import sys

### Use this function To attach files to the exe file (eg - png, txt, jpg etc) using pyinstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image = pygame.image.load(resource_path("grass.png"))
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()
        self.rect.center = (250, 250)
        self.movex = 0 # move along X
        self.movey = 0 # move along Y
        self.frame = 0 # count frames
        self.rect.x = x
        self.rect.y = y
        self.rect.width = w
        self.rect.height = h



    def draw(self, surface, cx, cy):
        """ Draw on surface """
        surface.blit(self.image, (self.rect.x - cx + 250, self.rect.y - cy + 250))


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (250, 250)
        self.movex = 0 # move along X
        self.movey = 0 # move along Y
        self.frame = 0 # count frames
        self.rect.x = x
        self.rect.y = y
        self.facing_left = False

        self.speed = 4
        self.jumpspeed = 20
        self.vsp = 0
        self.gravity = 1
        self.min_jumpspeed = 4
        self.prev_key = pygame.key.get_pressed()

    def draw(self, surface, cx, cy):
        """ Draw on surface """
        surface.blit(self.image, (self.rect.x - cx + 250, self.rect.y - cy + 250))

    def update(self, boxes):
        hsp = 0
        onground = self.check_collision(0, 1, boxes)
        # check keys
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.facing_left = True
            hsp = -self.speed
        elif key[pygame.K_RIGHT]:
            self.facing_left = False
            hsp = self.speed

        if key[pygame.K_UP] and onground:
            self.vsp = -self.jumpspeed

        # variable height jumping
        if self.prev_key[pygame.K_UP] and not key[pygame.K_UP]:
            if self.vsp < -self.min_jumpspeed:
                self.vsp = -self.min_jumpspeed

        self.prev_key = key

        # gravity
        if self.vsp < 10 and not onground:  # 9.8 rounded up
            self.vsp += self.gravity

        if onground and self.vsp > 0:
            self.vsp = 0

        # movement
        self.move(hsp, self.vsp, boxes)
    

    def move(self, x, y, boxes):
        dx = x
        dy = y

        while self.check_collision(0, dy, boxes):
            dy -= numpy.sign(dy)

        while self.check_collision(dx, dy, boxes):
            dx -= numpy.sign(dx)

        self.rect.move_ip([dx, dy])

    def check_collision(self, x, y, grounds):
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollideany(self, grounds)
        self.rect.move_ip([-x, -y])
        return collide
        


pygame.init()

# CREATING CANVAS
canvas = pygame.display.set_mode((500, 500))
icon = pygame.image.load(resource_path("icon.png"))

pygame.display.set_icon(icon)

# TITLE OF CANVAS
pygame.display.set_caption("Slimery")
exit = False

player = Player(-10, -100)
clock = pygame.time.Clock()
boxes = pygame.sprite.Group()
wh = 10
map = [
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, False, False, False, False, False, False, False, False],
    [False, False, True, False, False, False, False, False, False, False],
    [False, False, True, False, False, False, False, False, False, False],
    [True, True, True, True, True, False, False, True, True, True, True],
]
for by in range(0,len(map),1):
        for bx in range(0, len(map[by]), 1):
            if map[by][bx]:
                boxes.add(Box(bx*64,by*64, 64, 64))
def tileBackground(screen: pygame.display, image: pygame.Surface) -> None:
    screenWidth, screenHeight = screen.get_size()
    imageWidth, imageHeight = image.get_size()
    
    # Calculate how many tiles we need to draw in x axis and y axis
    tilesX = math.ceil(screenWidth / imageWidth)
    tilesY = math.ceil(screenHeight / imageHeight)
    
    # Loop over both and blit accordingly
    for x in range(tilesX):
        for y in range(tilesY):
            screen.blit(image, (x * imageWidth, y * imageHeight))

camerax = 0
cameray = 0
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    

    player.update(boxes) # update the player position
    camerax += ((player.rect.x - camerax) / 4)
    cameray += ((player.rect.y - cameray) / 4)
    canvas.fill((178,255,255)) # fill the canvas with white color
    for box in boxes:
        box.draw(canvas, camerax, cameray)
    player.draw(canvas, cx=camerax, cy=cameray) # draw the player on the canvas

    pygame.display.update() # update the canvas
    clock.tick(60)

pygame.quit()