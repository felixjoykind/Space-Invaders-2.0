import pygame
from settings import *

class Item():
    ITEMS_MAP = [
        SPEED_ITEM,
        DAMAGE_ITEM
    ]

    def __init__(self, x, y, killed_bosses):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.killed_bosses = killed_bosses
        self.img = pygame.transform.scale(self.ITEMS_MAP[self.killed_bosses], (self.width, self.height))
        self.bonus = 'speed'

        if self.ITEMS_MAP[self.killed_bosses] == SPEED_ITEM:
            self.bonus = 'speed'
        elif self.ITEMS_MAP[self.killed_bosses] == DAMAGE_ITEM:
            self.bonus = 'damage'
            self.width = 160
            self.height = 160

        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        self.img = pygame.transform.scale(self.ITEMS_MAP[self.killed_bosses], (self.width, self.height))
        window.blit(self.img, (self.x, self.y))
