import copy
from colorama import init as cinit
from colorama import Fore, Back, Style
from time import monotonic as clock, sleep

from sympy import true

from sprite import Sprite
from ImageLoader import *
from groups import *

class Arrow(Sprite):
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

    def update(self, screen_scroll):
        dx, dy = 0, 0
        self.rect.x += screen_scroll
        
        min = 1000000
        closest_building = None
        if building_group.sprite_list:
            for build in building_group.sprite_list:
                dist = (build.midpoint[0] - self.rect.x) ** 2 + (
                    build.midpoint[1] - self.rect.y
                ) ** 2
                if min >= dist:
                    min = dist
                    closest_building = build

        if closest_building:
            if self.rect.x > closest_building.midpoint[0]:
                self.direction = -1
            else:
                self.direction = 1
            dx += self.direction * self.speed

            if self.rect.y > closest_building.midpoint[1]:
                self.y_direction = -1
            else:
                self.y_direction = 1
            dy += self.y_speed * self.y_direction


        else:
            arrow_group.remove(self)

        # update co ordinates
        self.rect.x += dx
        self.rect.y += dy

        self.midpoint = (
            self.rect.x + (self.rect.width // 2),
            self.rect.y + (self.rect.height // 2),
        )

        # check for collisions with building
        rect = copy.deepcopy(self.rect)
        if Sprite.spritecollide(rect, building_group, False):
            for build in Sprite.spritecollide(rect, building_group, False):
                build.hp -= self.damage
                break

            arrow_group.remove(self)
        elif closest_building:
            if min <= self.speed:
                closest_building.hp -= self.damage
                arrow_group.remove(self)

