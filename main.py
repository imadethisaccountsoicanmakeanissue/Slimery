import pygame
import numpy
import math
import os 
import sys
import time
CAMERAA = 350
CAMERAB = 350
VERSION = "ALPHA v1.5 MAPOVERHAUL"
print('press 1 to load level1')
print('press 2 to load level2')
print('press q to load custom level')
level = 1
### Use this function To attach files to the exe file (eg - png, txt, jpg etc) using pyinstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
#preload
loading = False
def isloaded(level):
    if os.path.exists(resource_path("level"+str(level)+".txt")):
        return True
    return False
class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, t):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image = pygame.image.load(resource_path(t+".png"))
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
        surface.blit(self.image, (self.rect.x - cx + CAMERAA, self.rect.y - cy + CAMERAB))

class End(Box):
    thisisathing = True

class Player(pygame.sprite.Sprite):
    
    def __init__(self, x, y):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((64, 64))
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
        self.cool = False

    def draw(self, surface, cx, cy):
        """ Draw on surface """
        surface.blit(self.image, (self.rect.x - cx + CAMERAA, self.rect.y - cy + CAMERAB))

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
        global level
        global loading
        self.rect.move_ip([x, y])
        collide = pygame.sprite.spritecollideany(self, grounds)
        if collide.__class__ == End:
            if level != 0:
                loading = True
            
        self.rect.move_ip([-x, -y])
        
        return collide
        


pygame.init()

# CREATING CANVAS
print(VERSION)
canvas = pygame.display.set_mode((700, 700))
icon = pygame.image.load(resource_path("icon.png"))

pygame.display.set_icon(icon)

# TITLE OF CANVAS
pygame.display.set_caption("py")
exit = False

def load(player: Player, level: str):
    boxes = pygame.sprite.Group()
    # format = "00 00 00 00"
    #          "01 01 01 01"
    # load the level by reading the 2 letters then going a space then the two letters, etc
    start= (0, 0)
    with open(resource_path(level), "r") as f:
        level_data = f.read()
    level_data = level_data.split("\n")
    print(level_data)
    for row in level_data:
        rowr = row.split(" ")
    
        #print(row)
        for col in rowr:
            if col == "00":
                print()
                rowr.remove(col)
            elif col == "01":
                boxes.add(Box(level_data.index(row)*64, rowr.index(col)*64, 64, 64, "grass"))
                rowr.remove(col)
            elif col == "02":
                boxes.add(Box(level_data.index(row)*64, rowr.index(col)*64, 64, 64, "bricks"))
                rowr.remove(col)
            elif col == "03":
                boxes.add(End(0, 0, 64, 64, "end"))
                rowr.remove(col)
            elif col == "04":
                start = [level_data.index(row)*64, rowr.index(col)*64]
                rowr.remove(col)
            print(str(level_data.index(row)*64) + " " + str(rowr.index(col)*64)  )


    
    return (boxes, start)
def tileBackground(screen: pygame.display, image: pygame.Surface, cx, cy) -> None:
    screenWidth, screenHeight = screen.get_size()
    imageWidth, imageHeight = image.get_size()
    
    # Calculate how many tiles we need to draw in x axis and y axis
    tilesX = math.ceil(screenWidth / imageWidth)
    tilesY = math.ceil(screenHeight / imageHeight)
    
    # Loop over both and blit accordingly
    for x in range(tilesX):
        for y in range(tilesY):
            screen.blit(image, (x * imageWidth - cx + CAMERAA, y * imageHeight - cy + CAMERAB))
start = (0, 0)
camerax = 0
cameray = 0
player = Player(-10, -100)
clock = pygame.time.Clock()
boxes, start = load(player, resource_path("level1.txt"))
font = pygame.font.SysFont("Arial", 36)
def loadup(levell):
    level = levell
    boxes.empty()
    boxes = None
    boxes, start = load(player, resource_path("level"+str(levell)+".txt"))
    player.rect.x = start[0]
    player.rect.y = start[1]

while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    key = pygame.key.get_pressed()
    if key[pygame.K_1]:
        loadup(1)
    if key[pygame.K_2]:
        loadup(2)
    if key[pygame.K_q]:
        level = 0
        boxes.empty()
        boxes = None
        boxes, start = load(player, input("Enter level name:"))
        player.rect.x = start[0]
        player.rect.y = start[1]
    

    player.update(boxes) # update the player position
    if loading:
        loading = False
        level += 1
        if isloaded(level):
            boxes.empty()
            boxes = None
            boxes = load(player, resource_path("level"+str(level)+".txt"))
        else:
            level -= 1
    camerax += ((player.rect.x - camerax) / 4)
    cameray += ((player.rect.y - cameray) / 4)
    canvas.fill((178,255,255)) # fill the canvas with white color
    for box in boxes:
        box.draw(canvas, camerax, cameray)
    player.draw(canvas, cx=camerax, cy=cameray) # draw the player on the canvas
    font = pygame.font.SysFont("Arial", 36)
    txtsurf = font.render(str(round(clock.get_fps()))+"FPS", True, (0,0,0))
    canvas.blit(txtsurf,(600 - txtsurf.get_width() // 2, 100 - txtsurf.get_height() // 2))
    pygame.display.update() # update the canvas
    clock.tick(60)
    

pygame.quit()