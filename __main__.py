import pygame

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, l, t, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((w, h))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (250, 250)
        self.movex = 0 # move along X
        self.movey = 0 # move along Y
        self.frame = 0 # count frames
        self.rect.x = x
        self.rect.y = y
        self.rect.left = l
        self.rect.top = t
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
        self.jumping = False
        self.canJump = False
    def handle_keys(self):
        """ Handles Keys """
        key = pygame.key.get_pressed()
        dist = 1 # distance moved in 1 frame, try changing it to 5
        if key[pygame.K_UP]: # up key
            onground = pygame.sprite.spritecollideany(self, boxes)
            if self.jumping and onground:
                self.jumping = False
            if self.canJump:
                
                self.jumping = True
                self.movey = -10

        if key[pygame.K_RIGHT]: # right key
            self.movex += dist # move right
        elif key[pygame.K_LEFT]: # left key
            self.movex -= dist # move left

    def draw(self, surface, cx, cy):
        """ Draw on surface """
        surface.blit(self.image, (self.rect.x - cx + 250, self.rect.y - cy + 250))



    def update(self, floors):
        """ Move the player. """
        self.rect.x += self.movex
        self.rect.y += self.movey
        
        # Check for collison
        onground = pygame.sprite.spritecollideany(self, boxes)
        if self.jumping and onground:
                self.jumping = False
        print(self.jumping, onground, self.canJump)
        if onground:
            self.canJump = True
            if not self.jumping:
                self.rect.y -= 1
            self.jumping = False
        else:
            self.canJump = False
        if self.movex > 0 and not self.movex == 0:
            self.movex -= 0.5
        elif self.movex < 0 and not self.movex == 0:
            self.movex += 0.5
        if not onground:
            self.movey += 0.5
        else:
            self.movey = 0
        if self.movex > 5:
            self.movex = 5
        elif self.movex < -5:
            self.movex = -5
        if self.movey > 5:
            self.movey = 5
        elif self.movey < -5:
            self.movey = -5


pygame.init()

# CREATING CANVAS
canvas = pygame.display.set_mode((500, 500))
icon = pygame.image.load("icon.png")

pygame.display.set_icon(icon)

# TITLE OF CANVAS
pygame.display.set_caption("Slimery")
exit = False

player = Player(-10, 0)
clock = pygame.time.Clock()
boxes = pygame.sprite.Group()
boxes.add(Box(-10, 80, -100, 100, 800, 100))
camerax = 0
cameray = 0
while not exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
    camerax = player.rect.x - camerax / 8
    cameray = player.rect.y - cameray / 8
    player.handle_keys() # handle the keys

    player.update(boxes) # update the player position

    canvas.fill((178,255,255)) # fill the canvas with white color
    for box in boxes:
        box.draw(canvas, camerax, cameray)
    player.draw(canvas, cx=camerax, cy=cameray) # draw the player on the canvas

    pygame.display.update() # update the canvas
    clock.tick(60)

pygame.quit()