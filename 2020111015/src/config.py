"""
this file contains all relevant game constants
"""

# probabilities heavily depend on frame rate

from colorama import Fore, Back, Style

BUFFER_RIGHT = 10
BUFFER_DOWN = 5

MIN_HEIGHT = 20
MIN_WIDTH = 100

BARBARIAN_COUNT = 7

BG_COLOR = "\033[48;5;232m"

#building colors
BUILDING_COLOR = "\u001b[38;5;116m"
BUILDING_COLOR1 = "\u001b[38;5;147m"
BUILDING_COLOR2 = "\u001b[38;5;135m"
BUILDING_COLOR3 = "\u001b[38;5;13m"
BUILDING_COLOR4 = "\u001b[38;5;123m"
BUILDING_COLOR5 = "\u001b[38;5;40m"

PLAYER_COLOR = Fore.LIGHTCYAN_EX
CLOUD_COLOR = "\u001b[38;5;159m"
GND_COLOR = ""
GRASS_COLOR = Back.GREEN
WATER_COLOR = Back.LIGHTBLUE_EX
SKY_COLOR = Back.MAGENTA
BARBARIAN_COLOR = "\u001b[38;5;45m"
BARBARIAN_HALF_HEALTH = "\u001b[38;5;126m"
BARBARIAN_LOWER_HALF_HEALTH = "\u001b[38;5;206m"
BARBARIAN_FIFTH_HEALTH = "\u001b[38;5;225m"

BALLOON_COLOR = "\u001b[38;5;45m"
BALLOON_HALF_HEALTH = "\u001b[38;5;126m"
BALLOON_LOWER_HALF_HEALTH = "\u001b[38;5;206m"
BALLOON_FIFTH_HEALTH = "\u001b[38;5;225m"

ARCHER_COLOR = "\u001b[38;5;19m"
ARCHER_HALF_HEALTH = "\u001b[38;5;20m"
ARCHER_LOWER_HALF_HEALTH = "\u001b[38;5;21m"
ARCHER_FIFTH_HEALTH = "\u001b[38;5;22m"



BAR_HEIGHT = 2
BAR_DEFAULT_COLOR = Back.GREEN


# Building Health Color
HALF_HEALTH = Fore.LIGHTGREEN_EX
LOWER_HALF_HEALTH = Fore.LIGHTYELLOW_EX
FIFTH_HEALTH = Fore.LIGHTRED_EX

#WALLS
WALL_COLOR = "\u001b[38;5;229m"

GND_HEIGHT = 2
SKY_DEPTH = 3

# spawn points
SPAWN_COLOR = "\u001b[38;5;209m"

# spawn 1
SPAWN1_X = 1
SPAWN1_Y = 12
SPAWN1_x = 4
SPAWN1_y = 23

# spawn 2
SPAWN2_X = 170
SPAWN2_Y = 30
SPAWN2_x = 173
SPAWN2_y = 41


# spawn 3
SPAWN3_X = 280
SPAWN3_Y = 12
SPAWN3_x = 283
SPAWN3_y = 23

#SHELL
SHELL_COLOR = "\u001b[38;5;226m"
ARROW_COLOR = "\u001b[38;5;86m"


#SPELLS
HEAL_COOLDOWN = 20
HEAL_FACTOR = 1.5
HEAL_DURATION = 10

RAGE_COOLDOWN = 20
RAGE_FACTOR = 2
RAGE_DURATION = 10
