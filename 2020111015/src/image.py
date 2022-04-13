import os
from re import L

import numpy as np
from colorama import init as cinit
from colorama import Fore, Back, Style
import random
from time import monotonic as clock, sleep

import config as conf
from input import input_to, Get


class Image:
    def __init__(self, img):
        self.img = []
        idx = 0
        for i in img:
            self.img.append([])
            for j in i:
                for p in j:
                    self.img[idx].append(p)
            idx += 1

    def load(self):
        return np.array(self.img)

    def foreground_color(self, color):
        colored = []
        idx = 0
        for i in self.img:
            colored.append([])
            for j in i:
                colored[idx].append(Style.BRIGHT + color+j+Fore.RESET+Style.RESET_ALL)
            idx += 1
        return np.array(colored)

    def get_rect(self):
        return Rect(np.shape(self.img))

    def invert_y(self,color=""):
        inverted = []
        idx = 0
        for i in self.img:
            inverted.append([])
            for j in reversed(i):
                if j == "(":
                    j = ")"
                elif j == ")":
                    j = "("
                elif j == "{":
                    j = "}"
                elif j == "}":
                    j = "{"
                elif j == "/":
                    j = "\\"
                elif j == "\\":
                    j = "/"
                elif j == "b":
                    j = "d"
                elif j == "d":
                    j = "b"
                elif j == "<":
                    j = ">"
                elif j == "]":
                    j = "["
                elif j == ">":
                    j = "<"
                elif j == "[":
                    j = "]"

                inverted[idx].append(conf.BG_COLOR+Style.BRIGHT+color+j+Fore.RESET+Style.RESET_ALL+Back.RESET)
            idx += 1
        return np.array(inverted)


class Rect:
    def __init__(self, shape):
        self.height = shape[0]
        self.width = shape[1]
        self.x = 0
        self.y = 0

    def colliderect(self, rect):
        # test if rect of our image overlaps with the rect provided
        if self.x + self.width -1 >= rect.x and rect.x >= self.x:
            if self.y + self.height -1 >= rect.y and self.y <= rect.y:
                return True
            if self.y + self.height -1 >= rect.y + rect.height -1 and self.y <= rect.y + rect.height -1:
                return True
            if self.y >= rect.y and self.y+self.height -1 <= rect.y + rect.height -1:
                return True
            if self.y <= rect.y and self.y+self.height -1 >= rect.y + rect.height -1:
                return True
        if self.x + self.width -1 >= rect.x and rect.x + rect.width -1 >= self.x:
            if self.y + self.height -1 >= rect.y and self.y <= rect.y:
                return True
            if self.y + self.height -1 >= rect.y + rect.height -1 and self.y <= rect.y + rect.height -1:
                return True
            if self.y >= rect.y and self.y+self.height -1 <= rect.y + rect.height -1:
                return True
            if self.y <= rect.y and self.y+self.height -1 >= rect.y + rect.height -1:
                return True
        if self.x <= rect.x and self.x + self.width -1 >= rect.x + rect.width -1:
            if self.y + self.height -1 >= rect.y and self.y <= rect.y:
                return True
            if self.y + self.height -1 >= rect.y + rect.height -1 and self.y <= rect.y + rect.height -1:
                return True
            if self.y >= rect.y and self.y+self.height -1 <= rect.y + rect.height -1:
                return True
            if self.y <= rect.y and self.y+self.height -1 >= rect.y + rect.height -1:
                return True
        if self.x >= rect.x and self.x + self.width -1 <= rect.x + rect.width -1:

            if self.y + self.height -1 >= rect.y and self.y <= rect.y:
                return True
            if self.y + self.height -1 >= rect.y + rect.height -1 and self.y <= rect.y + rect.height -1:
                return True
            if self.y >= rect.y and self.y+self.height -1 <= rect.y + rect.height -1:
                return True
            if self.y <= rect.y and self.y+self.height -1 >= rect.y + rect.height -1:
                return True
        return False


