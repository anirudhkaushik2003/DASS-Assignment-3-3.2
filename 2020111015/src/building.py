import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock, sleep

import config as conf
from image import Image, Rect
from sprite import Sprite

from groups import building_group


class Building(Sprite):
    def __init__(self, img, x, y, type=2, color="", hp=100):
        self.type = type
        self.preserve = img  # image object store
        self.img = img.foreground_color(color)
        self.rect = img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = hp
        self.max_hp = hp
        self.midpoint = (
            self.rect.x + (self.rect.width // 2), self.rect.y + (self.rect.height // 2)
        )
        self.color = color

    def update(self, arguments):
        screen_scroll = arguments[0]
        self.rect.x += screen_scroll
        self.midpoint = (
            self.rect.x + (self.rect.width // 2), self.rect.y + (self.rect.height // 2)
        )
        if self.hp >= 0.5 * self.max_hp:
            self.img = self.preserve.foreground_color(self.color)
        elif self.hp >= 0.2 * self.max_hp:
            self.img = self.preserve.foreground_color(conf.LOWER_HALF_HEALTH)
        elif self.hp > 0 * self.max_hp:
            self.img = self.preserve.foreground_color(conf.FIFTH_HEALTH)
        if self.hp <= 0:
            building_group.remove(self)
