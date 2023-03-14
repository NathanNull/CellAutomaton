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
    ant_d=[2,3,4,5]
    ant_a=[6,7,8,9]
    img={dead:images.img_k, alive:images.img_b}
up,dn,lf,rt = 0,1,2,3
states.img.update({states.ant_d[i]:images.img_r for i in range(4)})
states.img.update({states.ant_a[i]:images.img_g for i in range(4)})

class Cell(sprite.Sprite):
    def __init__(self, gpos, *groups) -> None:
        self.pos = gpos
        self.state = states.ant_a[0] if gpos == (20, 20) else states.dead
        if gpos == (20,20):
            print(self.state)
        #self.state = states.alive if gpos in store.setup else states.dead

        super().__init__(*groups)
        self.rect = self.image.get_rect()
        self.rect.topleft = tuple(p*store.tsize for p in gpos)
    
    @property
    def image(self):
        return states.img[self.state]

    def update(self, curr_states: Wrapgrid[int]) -> None:
        nbs = curr_states.surrounding(self.pos)

        match self.state:
            case s if s in states.ant_d:
                self.state = states.alive
            case s if s in states.ant_a:
                self.state = states.dead
            case s if nbs[1][0] in [states.ant_d[up], states.ant_a[dn]]:
                self.state = states.ant_d[rt]+(4*s)
            case s if nbs[1][2] in [states.ant_d[dn], states.ant_a[up]]:
                self.state = states.ant_d[lf]+(4*s)
            case s if nbs[0][1] in [states.ant_d[rt], states.ant_a[lf]]:
                self.state = states.ant_d[dn]+(4*s)
            case s if nbs[2][1] in [states.ant_d[lf], states.ant_a[rt]]:
                self.state = states.ant_d[up]+(4*s)
            case _: 
                pass
        return