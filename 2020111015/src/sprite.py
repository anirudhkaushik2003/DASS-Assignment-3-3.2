import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock, sleep
import config as conf

from image import Image, Rect
from ImageLoader import *


class Sprite:
    def spritecollide(sprite, group, dokill):
        collided = []
        removed = []
        for i in group.sprite_list:
            if i != sprite:
                if sprite.colliderect(i.rect):
                    if dokill:
                        removed.append(i)
                    else:
                        collided.append(i)
        for i in removed:
            group.remove(i)
        return collided

    def draw(self, screen):
        screen.blit(self.img, self.rect)

    class Group:
        def __init__(self):
            self.sprite_list = []

        def add(self, sprites):
            self.sprite_list.append(sprites)

        def remove(self, sprites):
            self.sprite_list.remove(sprites)

        def draw(self, screen):
            for sprites in self.sprite_list:
                sprites.draw(screen)

        def clear(self):
            self.sprite_list.clear()

        def update(self, arguments):
            for sprites in self.sprite_list:
                sprites.update(arguments)
