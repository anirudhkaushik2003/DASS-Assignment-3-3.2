import os
import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock, sleep

import config as conf


class Screen:
    """
    encapsulates printing and screen management
    in each frame, all objects are added to the screen according to updated positions, sizes and representations provided by them, and screen prints it all
    manages a static background array and a dynamic foreground array
    """

    def __init__(self, height, width):
        self.CURSOR_0 = "\033[0;0H"
        self.CLEAR = "\033[2J"
        self.BELL = "\a"
        self.height = height
        self.width = width
        self.surface = np.array(
            [[conf.BG_COLOR for j in range(self.width)] for i in range(self.height)],
            dtype="object",
        )

        for i in range (self.height-2, self.height):
            for j in range(self.width):
                self.surface[i][j] = conf.GND_COLOR

        # for i in range(0,11):
        #     for j in range(self.width):
        #         self.surface[i][j] = conf.SKY_COLOR
        # for i in range(0, 3):
        #     for j in range(self.width):
        #         if random.random() < conf.ACCENT_AMT:  # random black dots
        #             self.surface[i][j] = Back.WHITE
        #             if random.random() < conf.ACCENT_AMT:
        #                 self.surface[i][j] = Back.WHITE
        #             if random.random() < conf.ACCENT_AMT:
        #                 self.surface[i + 1][j] = Back.WHITE
        #             if random.random() < conf.ACCENT_AMT:
        #                 self.surface[i][j-1] = Back.WHITE
        #             if random.random() < conf.ACCENT_AMT:
        #                 self.surface[i][j+1] = Back.WHITE
        #                 self.surface[i][j+2] = Back.WHITE
        #                 self.surface[i][j+3] = Back.WHITE
        #             if random.random() < conf.ACCENT_AMT:
        #                 self.surface[i][j+2] = Back.WHITE
        #                 self.surface[i][j+3] = Back.WHITE
        #                 self.surface[i ][j+4] = Back.WHITE



        # self.surface = np.array([[Back.BLACK for j in range(self.width)] for i in range(self.height)], dtype='object')

        self.foreground = np.array(
            [[" " for j in range(self.width)] for i in range(self.height)],
            dtype="object",
        )

    def display(self):
        print(self.CURSOR_0)
        for i in range(self.height):
            for j in range(self.width):
                print(self.surface[i][j] + self.foreground[i][j], end='')
            print('')
        

    def blit(self, img, rect):
        x_i_cap = rect.x
        x_i = 0
        x_j_cap = rect.x + rect.width
        x_j = rect.width
        y_start = rect.y
        y_start_ = 0
        y_end = rect.y + rect.height
        y_end_ = rect.height

        # Now make sure if half the object is visible, it is rendered correctly

        if x_i_cap < 0:
            x_i = 0 - x_i_cap
            x_i_cap = 0

        if y_start < 0:
            y_start_ = 0 - y_start
            y_start = 0

        if x_j_cap > self.width:
            x_j = self.width - rect.x
            x_j_cap = self.width

        if y_end > self.height:
            y_end_ = self.height - rect.y
            y_end = self.height

        try:
            self.foreground[y_start:y_end, x_i_cap:x_j_cap] = img[
                y_start_:y_end_, x_i:x_j
            ]
        except:
            return

    def clear(self):
        for i in range(self.height):
            for j in range(self.width):
                self.foreground[i][j] = " "
