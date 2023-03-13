from pygame import sprite
import pygame
from functools import lru_cache
from wrapgrid import Wrapgrid
import store

class images:
    @classmethod
    @lru_cache()
    def make_rect(_, col, lcol=(230, 230, 230)):
        return images.mr_raw(col, lcol)

    @classmethod
    def mr_raw(cls, col, lcol=(230, 230, 230)):
        img = pygame.Surface((store.tsize, store.tsize))
        img.fill(col)
        lcol = tuple((a+2*b)/3 for a,b in zip(lcol, col))
        pygame.draw.rect(img, lcol, pygame.Rect(0,0,store.tsize,store.tsize), 1)
        return img 
images.img_k = images.mr_raw((0,0,0))
images.img_r = images.mr_raw((255,0,0))
images.img_g = images.mr_raw((0,255,0))
images.img_b = images.mr_raw((0,0,255))

class states:
    dead=0
    alive=1
    img={dead:images.img_k, alive:images.img_b}

setup = store.setup

class Cell(sprite.Sprite):
    def __init__(self, gpos, *groups) -> None:
        self.pos = gpos
        self.state = states.alive if gpos in setup else states.dead

        super().__init__(*groups)
        self.rect = self.image.get_rect()
        self.rect.topleft = tuple(p*store.tsize for p in gpos)
    
    @property
    def image(self):
        return states.img[self.state]

    def update(self, curr_states: Wrapgrid[int]) -> None:
        neighbours = curr_states.surrounding(self.pos)
        living = [i for r in neighbours for i in r].count(states.alive)

        match self.state:
            case states.alive if living-1 not in [2,3]:
                self.state = states.dead
            case states.dead if living==3:
                self.state = states.alive
            case _:
                pass
        return