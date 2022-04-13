import os
import sys
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import copy

from time import monotonic as clock, sleep

import config as conf
from input import input_to, Get
from sprite import *
from groups import *
from ImageLoader import barbarian
from Level import level

rows, cols = os.popen("stty size", "r").read().split()
height = int(rows) - conf.BUFFER_DOWN
width = int(cols) - conf.BUFFER_RIGHT

scroll_thresh = 10


class Player:
    def __init__(self, character, x, y, color=""):
        self.speed = 3
        self.y_speed = 1
        self.img_left = []
        self.img_right = []
        for i in range(4):
            self.img_left.append(character[i].foreground_color(color))
        for i in range(4):
            self.img_right.append(character[i].invert_y(color))
        self.attack = 30
        self.attack_range = self.speed
        self.attack_counter = 0
        self.attack_sequence = False
        self.index = 0
        self.counter = 0
        self.direction = 1
        self.img = []
        self.rect = character[i].get_rect()
        self.rect.x = x
        self.rect.y = y
        self.level = level
        self.leviathan_range = self.speed * 2
        self.y_leviathan_range = self.speed * 2
        self.leviathan_damage = self.attack // 2 
        self.leviathan_sequence = False
        self.leviathan_counter = 0

        self.troops = conf.BARBARIAN_COUNT
        self.barbarians = 0
        self.archers = 0
        self.balloons = 0

        if self.direction == -1:
            self.img = self.img_left[self.index]
        elif self.direction == 1:
            self.img = self.img_right[self.index]

        self.isF = False

        if len(sys.argv) > 1:
            if os.path.exists(sys.argv[1]):
                self.f = open(sys.argv[1], "r")
                self.isF = True
            else:
                self.f = open("replays/"+str(clock()) + ".txt", "w")
                self.f.write("k")


        else:
            self.f = open("replays/"+str(clock()) + ".txt", "w")
            self.f.write("k")

        self.midpoint = (
            self.rect.x + (self.rect.width // 2),
            self.rect.y + (self.rect.height // 2),
        )

        self.max_hp = 1000
        self.hp = self.max_hp

        self.used_heal = False
        self.used_rage = False
        self.heal_counter = 0
        self.rage_counter = 0

        from spell import Heal_spell, Rage_spell
        self.heal_spell = Heal_spell(conf.HEAL_COOLDOWN, conf.HEAL_FACTOR)
        self.rage_spell = Rage_spell(conf.RAGE_COOLDOWN, conf.RAGE_FACTOR)

    def show(self):

        for i in self.img:
            for j in i:
                print(j, end="")
            print()
        print(self.rect.height, self.rect.width)

    def animate(self):
        walk_cooldown = 0
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.img_left):
                self.index = 0
        if self.direction == -1:
            self.img = self.img_left[self.index]
        if self.direction == 1:
            self.img = self.img_right[self.index]

    def use_attack(self):
        if self.attack_sequence == False:
            self.attack_sequence = True
            print("\a")
            rect = copy.deepcopy(self.rect)
            if self.direction == -1:
                    rect.x += self.attack_range * self.direction
            rect.width += self.attack_range*2
            collided = Sprite.spritecollide(rect, wall_group, False)
            if collided:
                for build in collided:
                    build.hp -= self.attack
            else:
                collided = Sprite.spritecollide(rect, building_group, False)    
                if collided:
                    for build in collided:
                        build.hp -= self.attack
        else:
            pass

    def use_leviathan_axe(self):
        if self.leviathan_sequence == False:
            self.leviathan_sequence = True
            print("\a")
            rect = copy.deepcopy(self.rect)
            rect.x += self.leviathan_range * -1
            rect.width += self.leviathan_range*2
            rect.y += self.y_leviathan_range * -1
            rect.height += self.y_leviathan_range*2
            collided = Sprite.spritecollide(rect, building_group, False)
            if collided:
                for build in collided:
                    build.hp -= self.attack
            
            collided = Sprite.spritecollide(rect, wall_group, False)
            if collided:
                for build in collided:
                    build.hp -= self.attack
        else:
            pass 

    def spawn_barb(self, x, y, color):
        import barbarian as barbare

        barb = barbare.Barbarian(barbarian, x, y, color)
        barbarian_group.add(barb)

    def spawn_arch(self, x, y, color):
        import archer as arche
        arch = arche.Archer(archer, x, y, color)
        barbarian_group.add(arch)

    def spawn_ball(self, x, y, color):
        import balloon as ballo
        ball = ballo.Balloon(hot_air_ballooon, x, y, color)
        balloon_group.add(ball)

    def update(self, screen, spawn_scroll,world):

        screen_scroll = 0
        dx = 0
        dy = 0
        # get key presses

        if self.isF:
            out = self.f.read(1)
        else:
            out = input_to(Get())
            if out:
                self.f.write(out)
            else:
                self.f.write("-")
        if out == "w" and self.hp > 0:
            dy -= self.y_speed
        if out == "s" and self.hp > 0:
            dy += self.y_speed
        if out == "a" and self.hp > 0:
            self.direction = -1
            dx += self.speed * self.direction
            self.counter += 1
        if out == "d" and self.hp > 0:
            self.direction = 1
            dx += self.speed * self.direction
            self.counter += 1
        elif out == "1" and self.barbarians < self.troops:
            self.spawn_barb(
                conf.SPAWN1_x + spawn_scroll,
                conf.SPAWN1_y,
                conf.BARBARIAN_COLOR,
            )

            self.barbarians += 1

        elif out == "2" and self.barbarians < self.troops:
            self.spawn_barb(
                conf.SPAWN2_x + spawn_scroll,
                conf.SPAWN2_y,
                conf.BARBARIAN_COLOR,
            )
            self.barbarians += 1
        elif out == "3" and self.barbarians < self.troops:
            self.spawn_barb(
                conf.SPAWN3_x + spawn_scroll,
                conf.SPAWN3_y,
                conf.BARBARIAN_COLOR,
            )
            self.barbarians += 1
        elif out == "4" and self.archers < self.troops:
            self.spawn_arch(
                conf.SPAWN1_x + spawn_scroll,
                conf.SPAWN1_y,
                conf.ARCHER_COLOR,
            )
            self.archers += 1

        elif out == "5" and self.archers < self.troops:
            self.spawn_arch(
                conf.SPAWN2_x + spawn_scroll,
                conf.SPAWN2_y-3,
                conf.ARCHER_COLOR,
            )
            self.archers += 1

        elif out == "6" and self.archers < self.troops:
            self.spawn_arch(
                conf.SPAWN3_x + spawn_scroll,
                conf.SPAWN3_y,
                conf.ARCHER_COLOR,
            )
            self.archers += 1

        elif out == "7" and self.balloons < self.troops:
            self.spawn_ball(
                conf.SPAWN1_x + spawn_scroll,
                conf.SPAWN1_y,
                conf.BALLOON_COLOR,
            )
            self.balloons += 1

        elif out == "8" and self.balloons < self.troops:
            self.spawn_ball(
                conf.SPAWN2_x + spawn_scroll,
                conf.SPAWN2_y - 10,
                conf.BALLOON_COLOR,
            )
            self.balloons += 1

        elif out == "9" and self.balloons < self.troops:
            self.spawn_ball(
                conf.SPAWN3_x + spawn_scroll,
                conf.SPAWN3_y,
                conf.BALLOON_COLOR,
            )
            self.balloons += 1

        if out == " " and self.hp > 0:
            self.use_attack()
        
        if out == "x" and self.hp > 0:
            self.use_leviathan_axe()

        if out == "o":
            if self.used_rage == False:
                self.used_rage = True
                self.rage_spell.effect(self)
        if out == "p":
            if self.used_heal == False:
                self.used_heal = True
                self.heal_spell.effect(self)

        if out == "f":
            self.f.close()
            os.system("stty echo")
            exit(0)

        if self.hp > 0:

            attack_cooldown = 5
            leviathan_cooldown = 10
            

            # handle spell updates

            # if self.used_heal:
            #     self.heal_spell.effect()
            #     self.heal_counter += 1

            # if self.used_rage:
            #     self.rage_spell.effect()
            #     self.rage_counter += 1

            # if self.rage_counter >= conf.RAGE_COOLDOWN:
            #     self.rage_counter = 0
            #     self.used_rage = False
            # if self.heal_counter >= conf.HEAL_COOLDOWN:
            #     self.heal_counter = 0
            #     self.used_heal = False

            # handle animations
            self.animate()

            # handle attacks
            if self.attack_sequence == True:
                self.attack_counter += 1

            if self.attack_counter >= attack_cooldown:
                self.attack_counter = 0
                self.attack_sequence = False

            if self.leviathan_sequence == True:
                self.leviathan_counter += 1

            if self.leviathan_counter >= leviathan_cooldown:
                self.leviathan_counter = 0
                self.leviathan_sequence = False

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

            if Sprite.spritecollide(rect, building_group, False):
                dx = 0

            # check y
            rect = copy.deepcopy(self.rect)
            rect.y += dy

            if Sprite.spritecollide(rect, building_group, False):
                dy = 0

            # check for collisions with walls

            # check x
            rect = copy.deepcopy(self.rect)
            rect.x += dx

            if Sprite.spritecollide(rect, wall_group, False):
                dx = 0

            # check y
            rect = copy.deepcopy(self.rect)
            rect.y += dy

            if Sprite.spritecollide(rect, wall_group, False):
                dy = 0

            # update co ordinates
            self.rect.x += dx
            self.rect.y += dy

            self.midpoint = (
                self.rect.x + (self.rect.width // 2),
                self.rect.y + (self.rect.height // 2),
            )

            # update scroll
            if (
                self.rect.x + self.rect.width - 1 > (width - scroll_thresh)
                and self.direction == 1
            ) or (self.rect.x < scroll_thresh and self.direction == -1):
                self.rect.x -= dx
                screen_scroll = -dx

        screen.blit(self.img, self.rect)

        return screen_scroll
