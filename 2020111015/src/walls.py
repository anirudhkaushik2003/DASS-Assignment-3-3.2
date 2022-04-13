from ImageLoader import *
from sprite import Sprite
from groups import wall_group

class Walls(Sprite):
    def __init__(self,img,x,y,color=""):
        self.max_hp = 20
        self.hp = self.max_hp
        self.img = img.foreground_color(color)
        self.rect = img.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self,screen_scroll):
        self.rect.x += screen_scroll

        if self.hp <= 0:
            wall_group.remove(self)
    

