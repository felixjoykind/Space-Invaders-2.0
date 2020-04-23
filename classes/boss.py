import pygame
import random
from settings import *
from classes.laser import Laser
from classes.ship import Ship

# Boss class
class Boss(Ship):
    COLOR_MAP = [
        (RED_SPACE_SHIP, RED_LASER),
        (GREEN_SPACE_SHIP, GREEN_LASER),
        (BLUE_SPACE_SHIP, BLUE_LASER)
    ]

    def __init__(self, x, y, killed_bosses, health=1200):
        super().__init__(x, y, health)
        self.ship_img = pygame.transform.scale(self.COLOR_MAP[killed_bosses][0], (250, 200))
        self.laser_img = pygame.transform.scale(self.COLOR_MAP[killed_bosses][1], (150, 150))
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.vel_y = 1.5
        self.vel_x = 1.5
        self.type = 'boss'
        self.max_health = health
        self.come = False
        self.killed_bosses = killed_bosses
        self.killed = False

    def move(self, vel):
        # Boss moving logic
        self.y += self.vel_y

        if self.y >= 100 and not self.come:
            self.come = True

        if self.health <= 0 and not self.killed: # If boss is killed - stop boss movement
            self.vel_x = 0
            self.vel_y = 0
            self.killed = True
            self.health += 30

        if self.come: # Start moving right and left when boss is on the screen (self.come)
            self.x += self.vel_x

        # Bouncing off the walls
        if self.x + self.ship_img.get_width() >= WIDTH:
            self.vel_x = -random.randint(1, 3)
        elif self.x <= 0:
            self.vel_x = random.randint(1, 3)
        elif self.y + self.ship_img.get_height() >= HEIGHT:
            self.vel_y = -random.randint(1, 3)
        elif self.y <= 0 and self.come:
            self.vel_y = random.randint(1, 3)

    # Shoot logic
    def shoot(self):
        if self.cool_down_counter == 0 and not self.killed:
            # Tripple shot
            laser1 = Laser(self.x+20, self.y, self.laser_img)
            laser2 = Laser(self.x+60, self.y, self.laser_img)
            laser3 = Laser(self.x+100, self.y, self.laser_img)
            self.lasers.append(laser1)
            self.lasers.append(laser2)
            self.lasers.append(laser3)
            self.cool_down_counter = 1

    # Drawing the boss
    def draw(self, window):
        super().draw(window)
        if self.come:
            self.healthbar(window)

    # Drawing healthbar
    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (165, 10, WIDTH-165*2, 10))
        if not self.killed:
            pygame.draw.rect(window, (0, 255, 0), (165, 10, (WIDTH-(165*2)) * (self.health/self.max_health), 10))
