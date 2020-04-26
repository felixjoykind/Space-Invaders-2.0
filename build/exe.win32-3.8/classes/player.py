import pygame
from settings import *
from classes.ship import Ship

# Player class
class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.damage = 10
        self.final_off_screen = False

    # Moving lasers
    def move_lasers(self, vel, objs):
        self.cooldown() # Cooling down the gun
        # Moving all lasers
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT): # If laser is off the screen
                self.lasers.remove(laser) # Hide it
            else:
                for obj in objs:
                    # If lasers is colliding with boss
                    if obj.type == 'boss' and laser.collision(obj) and obj.health > 0:
                        obj.health -= 10
                        if laser in self.lasers:
                            self.lasers.remove(laser)
                    # If lasers is colliding with enemy
                    elif laser.collision(obj) and obj.type != 'boss':
                        obj.health -= self.damage
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    # Drawing the player
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    # Drawing the healthbar
    def healthbar(self, window):
        if self.health < self.max_health:
            pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
            pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

    def final_scene(self):
        # Player final scene moving logic
        if self.y > -100:
            self.y -= 2
        else:
            self.final_off_screen = True
