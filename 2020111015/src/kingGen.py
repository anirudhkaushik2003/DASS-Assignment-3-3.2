import os

import player 
import player2
from ImageLoader import *
import config as conf
import sys
from time import monotonic as clock,sleep
from Level import level

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

rows, cols = os.popen("stty size", "r").read().split()
height = int(rows) - conf.BUFFER_DOWN
width = int(cols) - conf.BUFFER_RIGHT

choice = "0"
isF = False
if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]):
        f = open(sys.argv[1], "r")
        isF = True


# while True:
#     choice = input("Choose Barbarian King(K) or Archer Queen(Q): ")
#     if isF:
#         choice = f.read(1)
#         f.close()
#     if choice == "k":
#         king = player.Player(totoro_list, 22, height - 6 - conf.GND_HEIGHT,conf.PLAYER_COLOR)  # load player
#         break
#     elif choice == "q":
#         king = player2.Player2(kotoro_list, 22, height - 6 - conf.GND_HEIGHT,conf.PLAYER_COLOR)  # load player
#         break
