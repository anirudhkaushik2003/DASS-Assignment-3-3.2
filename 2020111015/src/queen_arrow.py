import copy
from colorama import init as cinit
from colorama import Fore, Back, Style
from time import monotonic as clock, sleep

from sympy import true

from sprite import Sprite
from ImageLoader import *
from groups import *


class QueenArrow(Sprite):
    def __init__(self, img, x, y, bull_range,direction, y_direction,color=""):
        self.direction = direction
        self.y_direction = y_direction
        if self.direction == -1:
            self.img = img.invert_y(color)
        else:
            self.img = img.foreground_color(color)
        self.rect = img.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 4
        self.damage = 40
        self.direction = direction
        self.y_speed = 2
        self.y_direction = y_direction
        self.midpoint = (
            self.rect.x + (self.rect.width // 2),
            self.rect.y + (self.rect.height // 2),
        )
        self.range = bull_range
        self.y_range = bull_range//4

        self.attack_range = 10
        self.y_attack_range = 10
        if self.range == 64:
            self.attack_range = 20
            self.y_attack_range = 20

    def explode(self):
        rect = copy.deepcopy(self.rect)
        rect.x += self.attack_range * -1
        rect.width += self.attack_range*2
        rect.y += self.y_attack_range * -1
        rect.height += self.y_attack_range*2
        collided = Sprite.spritecollide(rect, building_group, False)
        if collided:
            for  build in collided:
                    build.hp -= self.damage
        
        collided = Sprite.spritecollide(rect, wall_group, False)
        if collided:
            for build in collided:
                build.hp -= self.damage
        queen_arrow_group.remove(self)



    def show(self):

        for i in self.img:
            for j in i:
                print(j, end="")
            print()
        print(self.rect.height, self.rect.width)

    def update(self, screen_scroll):
        dx, dy = 0, 0
        
        dx += self.direction*self.speed
        dy += self.y_direction*self.y_speed

        self.range -= self.speed
        if self.range <= 0:
            self.explode()
            # queen_arrow_group.remove(self)
        # update co ordinates
        self.rect.x += dx
        self.rect.y += dy

        self.midpoint = (
            self.rect.x + (self.rect.width // 2),
            self.rect.y + (self.rect.height // 2),
        )

