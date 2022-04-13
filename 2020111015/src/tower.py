import copy
import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock, sleep

import config as conf
from image import Image, Rect
from sprite import Sprite
from ImageLoader import shell
from groups import *
import bigbullet


class Tower(Sprite):
    def __init__(self, img, x, y, type=6, color=""):
        self.type = type
        self.img = img.foreground_color(color)
        self.max_hp = 100
        self.hp = self.max_hp
        self.fire_rate = 2
        self.rect = img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.preserve = img
        self.midpoint = (
            self.rect.x + (self.rect.width // 2),
            self.rect.y + (self.rect.height // 2),
        )

        self.attack_sequence = False
        self.attack_counter = 0

    def update(self, arguments):
        screen_scroll = arguments[0]
        king = arguments[1]
        self.rect.x += screen_scroll

        attack_cooldown = 10

        self.midpoint = (
            self.rect.x + (self.rect.width // 2),
            self.rect.y + (self.rect.height // 2),
        )
        if self.hp >= 0.5 * self.max_hp:
            self.img = self.preserve.foreground_color(conf.HALF_HEALTH)
        elif self.hp >= 0.2 * self.max_hp:
            self.img = self.preserve.foreground_color(conf.LOWER_HALF_HEALTH)
        elif self.hp > 0 * self.max_hp:
            self.img = self.preserve.foreground_color(conf.FIFTH_HEALTH)
        if self.hp <= 0:
            building_group.remove(self)

        if balloon_group.sprite_list:
            if self.attack_sequence == False:
                self.attack_sequence = True
                bullet_1 = bigbullet.BigBullet(
                    shell, self.midpoint[0], self.midpoint[1],5000, conf.SHELL_COLOR
                )
                BigBullet_group.add(bullet_1)
        elif barbarian_group.sprite_list:
            if self.attack_sequence == False:
                self.attack_sequence = True
                bullet_1 = bigbullet.BigBullet(
                    shell, self.midpoint[0], self.midpoint[1],5000, conf.SHELL_COLOR
                )
                BigBullet_group.add(bullet_1)
        elif king.hp > 0:
            if self.attack_sequence == False:
                self.attack_sequence = True
                bullet_1 = bigbullet.BigBullet(
                    shell, self.midpoint[0], self.midpoint[1],5000, conf.SHELL_COLOR
                )
                BigBullet_group.add(bullet_1)

        if self.attack_sequence == True:
            self.attack_counter += 1

        if self.attack_counter >= attack_cooldown:
            self.attack_counter = 0
            self.attack_sequence = False
