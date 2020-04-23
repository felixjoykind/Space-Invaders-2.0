import pygame

# Laser class
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window): # Drawing
        window.blit(self.img, (self.x, self.y))

    def move(self, vel): # Moving
        self.y += vel

    def off_screen(self, height): # Is off the screen
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj): # Is colliding with something
        return collide(obj, self)

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (int(offset_x), int(offset_y))) != None
