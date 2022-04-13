import copy
import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock, sleep


from building import Building
import config as conf
from image import Image, Rect
from sprite import Sprite
import arrow

from groups import building_group
from ImageLoader import castle1
from groups import barbarian_group, wall_group

#Note: movement speed must not be greater than your own width, same for y_speed and height

class Barbarian(Sprite):
    def __init__(self, character, x, y, color=""):
        self.preserve = character
        self.speed = 2
        self.direction = 1
        self.attack = 10
        self.max_hp = 50
        self.hp = self.max_hp
        self.y_speed = 1
        self.y_direction = 1
        self.attack_range = self.speed
        self.y_attack_range = self.y_speed
        self.attack_counter = 0
        self.attack_sequence = False
        self.img_left = character.foreground_color(color)
        self.img_right = character.invert_y(color)
        self.img = self.img_right
        if self.direction == -1:
            self.img = self.img_left
        elif self.direction == 1:
            self.img = self.img_right
        self.rect = character.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.midpoint = (
            self.rect.x + (self.rect.width // 2),
            self.rect.y + (self.rect.height // 2),
        )

        self.isAttacking = False

    def show(self):

        for i in self.img:
            for j in i:
                print(j, end="")
            print()
        print(self.rect.height, self.rect.width)

    def choose_target_and_move(self):
        dx,dy = 0,0
        min = 10000000
        closest_building = None
        for buildings in building_group.sprite_list:
            dist = (buildings.midpoint[0] - self.midpoint[0]) ** 2 + (
                buildings.midpoint[1] - self.midpoint[1]
            ) ** 2
            if min >= dist:
                min = dist
                closest_building = buildings

        if closest_building:
            if self.midpoint[0] > closest_building.midpoint[0]:
                self.direction = -1
            else:
                self.direction = 1
            dx += self.direction * self.speed

            if self.midpoint[1] > closest_building.midpoint[1]:
                self.y_direction = -1
            else:
                self.y_direction = 1
            dy += self.y_speed * self.y_direction

        else:
            pass

        return dx, dy

    def use_attack(self):
        if self.attack_sequence == False:
                self.attack_sequence = True
                rect = copy.deepcopy(self.rect)
                if self.direction == -1:
                    rect.x += self.attack_range * self.direction
                if self.y_direction == -1:
                    rect.y += self.y_attack_range * self.y_direction
                rect.width += self.attack_range
                rect.height += self.y_attack_range
                collided = Sprite.spritecollide(rect, wall_group, False)
                if collided:
                    for build in collided:
                        build.hp -= self.attack
                else:
                    collided = Sprite.spritecollide(rect, building_group, False)
                    if collided:
                        for build in collided:
                            build.hp -= self.attack

    def update(self, arguments):
        screen_scroll = arguments[0]
        world = arguments[1]
        dx, dy = 0, 0
        attack_cooldown = 4
        self.rect.x += screen_scroll
        if self.hp >= 0.5 * self.max_hp:
            self.img_left = self.preserve.foreground_color(conf.BARBARIAN_HALF_HEALTH)
            self.img_right = self.preserve.invert_y(conf.BARBARIAN_HALF_HEALTH)

        elif self.hp >= 0.2 * self.max_hp:
            self.img_left = self.preserve.foreground_color(
                conf.BARBARIAN_LOWER_HALF_HEALTH
            )
            self.img_right = self.preserve.invert_y(conf.BARBARIAN_LOWER_HALF_HEALTH)

        elif self.hp > 0 * self.max_hp:
            self.img_left = self.preserve.foreground_color(conf.BARBARIAN_FIFTH_HEALTH)
            self.img_right = self.preserve.invert_y(conf.BARBARIAN_FIFTH_HEALTH)

        if self.hp <= 0:
            barbarian_group.remove(self)
        else:
            self.isAttacking = False
            dx,dy = self.choose_target_and_move()

            if self.direction == -1:
                self.img = self.img_left
            elif self.direction == 1:
                self.img = self.img_right

            # check for collisions with world
            for tile in world.tile_list:
                    if tile[2] == True:
                        # check for collision in x direction
                        rect = copy.deepcopy(self.rect)
                        rect.x += dx
                        if tile[1].colliderect(rect):
                            dx = 0
                        # check for collision in y direction
                        rect = copy.deepcopy(self.rect)
                        rect.y += dy
                        if tile[1].colliderect(rect):
                            dy = 0

            # check for collisions with buildings

            # check x
            rect = copy.deepcopy(self.rect)
            rect.x += dx

            self.isAttacking = False

            if Sprite.spritecollide(rect, building_group, False):
                dx = 0
                self.isAttacking = True

            # check y
            rect = copy.deepcopy(self.rect)
            rect.y += dy

            if Sprite.spritecollide(rect, building_group, False):
                dy = 0
                self.isAttacking = True

            # check for collision with walls

            # check x
            rect = copy.deepcopy(self.rect)
            rect.x += dx


            if Sprite.spritecollide(rect, wall_group, False):
                dx = 0
                self.isAttacking = True

            # check y
            rect = copy.deepcopy(self.rect)
            rect.y += dy

            if Sprite.spritecollide(rect, wall_group, False):
                dy = 0
                self.isAttacking = True

            # handle attacks
            if self.isAttacking == True:
                self.use_attack()

            if self.attack_sequence == True:
                self.attack_counter += 1

            if self.attack_counter >= attack_cooldown:
                self.attack_counter = 0
                self.attack_sequence = False

            # update co ordinates
            self.rect.x += dx
            self.rect.y += dy

            self.midpoint = (
                self.rect.x + (self.rect.width // 2),
                self.rect.y + (self.rect.height // 2),
            )
