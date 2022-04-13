import copy
from colorama import init as cinit
from colorama import Fore, Back, Style
from time import monotonic as clock, sleep

from sympy import true

from sprite import Sprite
from ImageLoader import *
from groups import *


class Bullet(Sprite):
    def __init__(self, img, x, y, bull_range,color=""):
        self.img = img.foreground_color(color)
        self.rect = img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 5
        self.damage = 30
        self.direction = 1
        self.y_speed = 2
        self.y_direction = 1
        self.midpoint = (
            self.rect.x + (self.rect.width // 2),
            self.rect.y + (self.rect.height // 2),
        )
        self.range = bull_range

    def show(self):

        for i in self.img:
            for j in i:
                print(j, end="")
            print()
        print(self.rect.height, self.rect.width)

    def update(self, arguments):
        screen_scroll = arguments[0]
        king = arguments[1]

        dx, dy = 0, 0
        self.rect.x += screen_scroll
        if king.hp > 0:
            min = (king.midpoint[0] - self.midpoint[0]) ** 2 + (
                king.midpoint[1] - self.midpoint[1]
            ) ** 2
        else:
            min = 1000000
        closest_barbarian = None
        if barbarian_group.sprite_list:
            for barbarians in barbarian_group.sprite_list:
                dist = (barbarians.midpoint[0] - self.rect.x) ** 2 + (
                    barbarians.midpoint[1] - self.rect.y
                ) ** 2
                if min >= dist:
                    min = dist
                    closest_barbarian = barbarians

        if min <= self.range:

            if closest_barbarian:
                if self.rect.x > closest_barbarian.midpoint[0]:
                    self.direction = -1
                else:
                    self.direction = 1
                dx += self.direction * self.speed

                if self.rect.y > closest_barbarian.midpoint[1]:
                    self.y_direction = -1
                else:
                    self.y_direction = 1
                dy += self.y_speed * self.y_direction

            elif king.hp > 0:
                if self.midpoint[0] > king.midpoint[0]:
                    self.direction = -1
                else:
                    self.direction = 1
                dx += self.direction * self.speed

                if self.midpoint[1] > king.midpoint[1]:
                    self.y_direction = -1
                else:
                    self.y_direction = 1
                dy += self.y_speed * self.y_direction

            else:
                bullet_group.remove(self)

        else:
            bullet_group.remove(self)

        # update co ordinates
        self.rect.x += dx
        self.rect.y += dy

        self.midpoint = (
            self.rect.x + (self.rect.width // 2),
            self.rect.y + (self.rect.height // 2),
        )

        # check for collisions with barbarian
        rect = copy.deepcopy(self.rect)
        if Sprite.spritecollide(rect, barbarian_group, False):
            for barbarian in Sprite.spritecollide(rect, barbarian_group, False):
                barbarian.hp -= self.damage
                break

            bullet_group.remove(self)
        elif closest_barbarian:
            if min <= self.speed:
                closest_barbarian.hp -= self.damage
                bullet_group.remove(self)

        elif self.rect.colliderect(king.rect):
            king.hp -= self.damage
            bullet_group.remove(self)
