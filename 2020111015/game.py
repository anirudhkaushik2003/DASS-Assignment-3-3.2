import os
import warnings
from colorama import init as cinit
from colorama import Fore, Back, Style
from time import monotonic as clock, sleep

import sys

sys.path.append("./src")

import config as conf
warnings.simplefilter(action="ignore", category=FutureWarning) # ignore a warning, what could possibly go wrong - jejus krist circa 1969

from screen import Screen
from ImageLoader import *
from sprite import *
from groups import *
from Level import level
import player
import player2
import numpy as np
import random
from building import Building
from turret import Turret
from tower import Tower
from walls import Walls

########################################################################################################################################
rows, cols = os.popen("stty size", "r").read().split()
height = int(rows) - conf.BUFFER_DOWN
width = int(cols) - conf.BUFFER_RIGHT
if height < conf.MIN_HEIGHT or width < conf.MIN_WIDTH:
    print(
        Fore.RED
        + "Error: Switch to fullscreen to play, I can't fit something so big in a place this small my dude"
    )
    raise SystemExit

rows, cols = os.popen("stty size", "r").read().split()
height = int(rows) - conf.BUFFER_DOWN
width = int(cols) - conf.BUFFER_RIGHT

totoro_list = []
totoro_list.append(totoro)
totoro_list.append(totoro1)
totoro_list.append(totoro2)
totoro_list.append(totoro3)

kotoro_list = []
kotoro_list.append(kotoro)
kotoro_list.append(kotoro1)
kotoro_list.append(kotoro2)
kotoro_list.append(kotoro3)


choice = "k"
isF = False
if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]):
        f = open(sys.argv[1], "r")
        isF = True

if isF:
    choice = f.read(1)
    f.close()
else:
    choice = input("Choose Barbarian King(K) or Archer Queen(Q): ")
if choice == "k":
    king = player.Player(totoro_list, 22, height - 6 - conf.GND_HEIGHT,conf.PLAYER_COLOR)  # load player
elif choice == "q":
    king = player2.Player2(kotoro_list, 22, height - 6 - conf.GND_HEIGHT,conf.PLAYER_COLOR)  # load player
else:
    king = player.Player(totoro_list, 22, height - 6 - conf.GND_HEIGHT,conf.PLAYER_COLOR)  # load player

########################################################################################################################################


def victory():
    print("\033[0K", end="")
    os.system("clear")
    print()
    for i in gameOver.load():
        for j in i:
            print(j, end="")
        print()
    print()
    for i in victory_1.load():
        for j in i:
            print(j, end="")
        print()
    print("\n\nyou won!")


def defeat():
    print("\033[0K", end="")
    os.system("clear")
    print()
    for i in gameOver.load():
        for j in i:
            print(j, end="")
        print()
    print()
    for i in defeat_1.load():
        for j in i:
            print(j, end="")
        print()
    print("\n\nyou lost!")


def get_health_bar():
    return np.array([Back.GREEN+" " for i in range(king.hp // 50)])


def print_stats():
    print(Style.RESET_ALL + Style.BRIGHT, end="")
    print("\033[0K", end="")
    print("HEALTH: ", end="")
    print(Fore.GREEN+"[",end="")
    health_bar = get_health_bar()
    for i in health_bar:
        print(i, end="")
    print(Back.RESET+"]"+Fore.RESET)

    print("HEAL SPELL: ", end="")
    if not king.used_heal:
        print("READY",end="\t")
    else:
        print("USED ",end="\t")

    print("RAGE SPELL: ", end="")
    if not king.used_rage:
        print("READY",end="\t")
    else:
        print("USED ",end="\t")

    print("ATTACK USED: ", end="")
    if choice == "k":
        if king.attack_sequence:
            print("BARBARIAN SWORD",end="\t")
        elif king.leviathan_sequence:
            print("LEVIATHAN AXE  ",end="\t")
        else:
            print("               ",end="\t")
    else:
        if king.attack_sequence:
            print("CUCCOO ATTACK",end="\t")
        elif king.leviathan_sequence:
            print("EAGLE ARROW  ",end="\t")
        else:
            print("               ",end="\t")

    print("NUMBER OF TROOPS: ",end="\t")
    print("  FIGHTING: ", end="")
    if (len(barbarian_group.sprite_list) + len(balloon_group.sprite_list)) < 10:
        print(len(barbarian_group.sprite_list) + len(balloon_group.sprite_list),end="  \t")
    else:
        print(len(barbarian_group.sprite_list) + len(balloon_group.sprite_list),end=" \t")
    print("  DEAD: ", end="")
    if king.barbarians + king.archers + king.balloons -len(balloon_group.sprite_list) - len(barbarian_group.sprite_list) < 10:
        print(king.barbarians + king.archers + king.balloons -len(balloon_group.sprite_list) - len(barbarian_group.sprite_list),end=" \t")
    else:
        print(king.barbarians + king.archers + king.balloons -len(balloon_group.sprite_list) - len(barbarian_group.sprite_list),end="\t")
    print("  STANDBY: ", end="")
    if 3*king.troops - king.barbarians - king.balloons - king.archers < 10:
        print(3*king.troops - king.barbarians - king.balloons - king.archers,end=" \t")
    else:
        print(3*king.troops - king.barbarians - king.balloons - king.archers,end="\t")
    print("BUILDINGS LEFT: ",end="")
    if len(building_group.sprite_list) < 10:
        print(len(building_group.sprite_list),end=" \t")
    else:
        print(len(building_group.sprite_list),end="\t")


def check_end():
    cond = False
    ending = ""
    if not building_group.sprite_list:
        if level < 3:
            ending = ""
        else:
            ending = "victory"
        cond = True
    elif king.barbarians == king.troops and king.balloons == king.troops and king.archers == king.troops and king.hp <= 0:
        if not barbarian_group.sprite_list and not balloon_group.sprite_list:
            ending = "defeat"
            cond = True

    return cond, ending

class World:
    def __init__(self, data):
        self.tile_list = []
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile[0] == 1:
                    img = Tree
                    img.rect = img.get_rect()
                    img.rect.x = col_count
                    img.rect.y = row_count
                    block = (img.foreground_color(Fore.GREEN), img.rect, tile[1])
                    self.tile_list.append(block)
                if tile[0] == 3:
                    building = Building(
                        castleLarge,
                        col_count,
                        row_count,
                        tile[0],
                        random.choice(
                            [
                                conf.BUILDING_COLOR1,
                                conf.BUILDING_COLOR2,
                                conf.BUILDING_COLOR3,
                                conf.BUILDING_COLOR4,
                                conf.BUILDING_COLOR5,
                            ]
                        ),
                        250,
                    )
                    building_group.add(building)
                if tile[0] == 2:
                    building = Building(
                        castle1,
                        col_count,
                        row_count,
                        tile[0],
                        random.choice(
                            [
                                conf.BUILDING_COLOR1,
                                conf.BUILDING_COLOR2,
                                conf.BUILDING_COLOR3,
                                conf.BUILDING_COLOR4,
                                conf.BUILDING_COLOR5,
                            ]
                        ),
                        120,
                    )
                    building_group.add(building)
                if tile[0] == 4:####
                    img = cloudCluster
                    img.rect = img.get_rect()
                    img.rect.x = col_count
                    img.rect.y = row_count
                    block = (img.foreground_color(conf.CLOUD_COLOR), img.rect, tile[1])
                    self.tile_list.append(block)
                if tile[0] == 5:
                    img = ground_block
                    img.rect = img.get_rect()
                    img.rect.x = col_count
                    img.rect.y = row_count
                    block = (img.foreground_color(Fore.RED), img.rect, tile[1])
                    self.tile_list.append(block)
                if tile[0] == 6:
                    turret_1 = Turret(
                        turret, col_count, row_count, tile[0], conf.BUILDING_COLOR
                    )
                    building_group.add(turret_1)
                if tile[0] == 9:
                    turret_2 = Tower(
                        wiz_tower, col_count, row_count, 6, conf.BUILDING_COLOR
                    )
                    building_group.add(turret_2)
                if tile[0] == 7:
                    img = spawn_point
                    img.rect = img.get_rect()
                    img.rect.x = col_count
                    img.rect.y = row_count
                    block = (img.foreground_color(conf.SPAWN_COLOR), img.rect, tile[1])
                    self.tile_list.append(block)
                if tile[0] == 8:
                    wall_1 = Walls(wall_block, col_count, row_count, conf.WALL_COLOR)
                    wall_group.add(wall_1)

                col_count += 1
            row_count += 1

    def draw(self, screen, screen_scroll):
        for tile in self.tile_list:
            tile[1].x += screen_scroll
            screen.blit(tile[0], tile[1])

###### WORLD DATA LOADER #####################


data1 = np.array(
    [[[0, True] for j in range(width * 2)] for i in range(height)],
    dtype="object",
)

data1[0][0] = [4, True]
data1[0][50] = [4, True]
data1[0][100] = [4, True]
data1[0][150] = [4, True]
data1[0][200] = [4, True]
data1[0][250] = [4, True]
# town hall
data1[11][90] = [3, True]
# turrets
data1[14][68] = [6, True]
data1[17][158] = [6, True]
data1[12][30] = [9,True]
data1[12][230] = [9,True]


# buildings
data1[11][50] = [2, True]
data1[20][50] = [2, True]
data1[24][68] = [2, True]
data1[27][55] = [2, True]

data1[24][208] = [2, True]
data1[11][208] = [2, True]

# spwn points
data1[conf.SPAWN1_Y][conf.SPAWN1_X] = [7, False]
data1[conf.SPAWN2_Y][conf.SPAWN2_X] = [7, False]
data1[conf.SPAWN3_Y][conf.SPAWN3_X] = [7, False]

# place walls
for i in range(10, height - 12):
    data1[i][48] = [8, True]
for i in range(48, 148):
    data1[height - 12][i] = [8, True]
for i in range(25, height - 11):
    data1[i][148] = [8, True]

for i in range(148, 200):
    data1[25][i] = [8, True]
for i in range(10, 26):
    data1[i][200] = [8, True]


last_j = 0
for i in range(0, height, 10):
    for j in range(301, width * 2 - 1, 20):
        data1[i][j] = [1, False]
        last_j = j

for i in range(0, height, 10):
    for j in range(last_j, width * 2, 20):
        data1[i][j] = [1, True]


for i in range(height - 2, height):
    for j in range(width * 2):
        data1[i][j] = [5, True]
for i in range(1, height - 2):
    data1[i][0] = [5, True]



data2 = np.array(
    [[[0, True] for j in range(width * 2)] for i in range(height)],
    dtype="object",
)

data2[0][0] = [4, True]
data2[0][50] = [4, True]
data2[0][100] = [4, True]
data2[0][150] = [4, True]
data2[0][200] = [4, True]
data2[0][250] = [4, True]
# town hall
data2[11][90] = [3, True]
# turrets
data2[14][68] = [6, True]
data2[17][158] = [6, True]
data2[12][30] = [9,True]
data2[12][230] = [9,True]
data2[20][68] = [9,True]
data2[37][220] = [6,True]


# buildings
data2[11][50] = [2, True]
data2[20][50] = [2, True]
data2[27][55] = [2, True]
data2[24][208] = [2, True]
data2[11][208] = [2, True]

# spwn points
data2[conf.SPAWN1_Y][conf.SPAWN1_X] = [7, False]
data2[conf.SPAWN2_Y][conf.SPAWN2_X] = [7, False]
data2[conf.SPAWN3_Y][conf.SPAWN3_X] = [7, False]

# place walls
for i in range(10, height - 12):
    data2[i][48] = [8, True]
for i in range(48, 148):
    data2[height - 12][i] = [8, True]
for i in range(25, height - 11):
    data2[i][148] = [8, True]

for i in range(148, 200):
    data2[25][i] = [8, True]
for i in range(10, 26):
    data2[i][200] = [8, True]


last_j = 0
for i in range(0, height, 10):
    for j in range(301, width * 2 - 1, 20):
        data2[i][j] = [1, False]
        last_j = j

for i in range(0, height, 10):
    for j in range(last_j, width * 2, 20):
        data2[i][j] = [1, True]


for i in range(height - 2, height):
    for j in range(width * 2):
        data2[i][j] = [5, True]
for i in range(1, height - 2):
    data2[i][0] = [5, True]


data3 = np.array(
    [[[0, True] for j in range(width * 2)] for i in range(height)],
    dtype="object",
)

data3[0][0] = [4, True]
data3[0][50] = [4, True]
data3[0][100] = [4, True]
data3[0][150] = [4, True]
data3[0][200] = [4, True]
data3[0][250] = [4, True]
# town hall
data3[11][90] = [3, True]
# turrets
data3[14][68] = [6, True]
data3[17][158] = [6, True]
data3[12][30] = [9,True]
data3[12][230] = [9,True]
data3[20][255] = [9,True]

data3[20][68] = [9,True]
data3[30][220] = [6,True]
data3[37][130] = [6,True]



# buildings
data3[11][50] = [2, True]
data3[27][50] = [2, True]
data3[20][52] = [2, True]
data3[30][205] = [2, True]
data3[20][206] = [2, True]
data3[11][208] = [2, True]
data3[37][232] = [2,True]
data3[11][257] = [2,True]
data3[27][276] = [2,True]




# spwn points
data3[conf.SPAWN1_Y][conf.SPAWN1_X] = [7, False]
data3[conf.SPAWN2_Y][conf.SPAWN2_X] = [7, False]
data3[conf.SPAWN3_Y][conf.SPAWN3_X] = [7, False]

# place walls
for i in range(10, height - 12):
    data3[i][48] = [8, True]
for i in range(48, 148):
    data3[height - 12][i] = [8, True]
for i in range(25, height - 11):
    data3[i][148] = [8, True]

for i in range(148, 200):
    data3[25][i] = [8, True]
for i in range(10, 26):
    data3[i][200] = [8, True]


last_j = 0
for i in range(0, height, 10):
    for j in range(301, width * 2 - 1, 20):
        data3[i][j] = [1, False]
        last_j = j

for i in range(0, height, 10):
    for j in range(last_j, width * 2, 20):
        data3[i][j] = [1, True]


for i in range(height - 2, height):
    for j in range(width * 2):
        data3[i][j] = [5, True]
for i in range(1, height - 2):
    data3[i][0] = [5, True]

#############################################
world = World(data1)


os.system("stty -echo")
while level < 4:
    if level >= 4:
        break
    screen = Screen(height, width)
    screen_scroll = 0
    spawn_scroll = 0
    ending = ""

    cinit()
    print("\033[2J")  # clear screen
    while True:
        start = clock()
        screen.clear()  ## calling here is better than after screen.display, prolly a buffer issue
        screen_scroll = king.update(screen, spawn_scroll,world)
        spawn_scroll += screen_scroll

        # update barbarians
        barbarian_group.update([screen_scroll,world])
        barbarian_group.draw(screen)

        # update buildings
        building_group.update([screen_scroll,king])
        building_group.draw(screen)

        # update bullets
        bullet_group.update([screen_scroll,king])
        bullet_group.draw(screen)

        # update BigBullets
        BigBullet_group.update([screen_scroll,king])
        BigBullet_group.draw(screen)

        # update arrows
        arrow_group.update(screen_scroll)
        arrow_group.draw(screen)

        # update queen_arrows
        queen_arrow_group.update(screen_scroll)
        queen_arrow_group.draw(screen)

        # update walls
        wall_group.update(screen_scroll)
        wall_group.draw(screen)

        #update balloons
        balloon_group.update([screen_scroll,world])
        balloon_group.draw(screen)

        # draw the world
        world.draw(screen, screen_scroll)
        

        # display the screen
        screen.display()

        print(Style.RESET_ALL + Style.BRIGHT, end="")
        print("\033[0K", end="")
        print_stats()

        cond, ending = check_end()
        if cond:
            break

        while clock() - start < 0.1:
            pass

    level += 1

    if level < 4:
        if ending == "defeat":
            defeat()
            print(ending)
            break
        os.system("clear")
        print("\033[0K", end="")
        building_group.clear() 
        barbarian_group.clear() 
        bullet_group.clear() 
        wall_group.clear() 
        balloon_group.clear() 
        arrow_group.clear() 
        BigBullet_group.clear() 
        queen_arrow_group.clear() 
        screen_scroll = 0
        if level == 2:
            world = World(data2)
        elif level == 3:
            world = World(data3)
        else:
            break
        if choice == "k":
            king = player.Player(totoro_list, 22, height - 6 - conf.GND_HEIGHT,conf.PLAYER_COLOR)  # load player
        else:
            king = player2.Player2(kotoro_list, 22, height - 6 - conf.GND_HEIGHT,conf.PLAYER_COLOR)  # load player


    else:
        if ending == "victory":
            victory()
            print(ending)

        elif ending == "defeat":
            defeat()
            print(ending)
        break
    
king.f.close()
os.system("stty echo")
exit(0)
