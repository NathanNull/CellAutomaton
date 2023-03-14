from typing import TypeVar, Generic, Tuple, Dict, Callable

T = TypeVar("T")
T2 = TypeVar("T2")
Vec2 = Tuple[int, int]

class Wrapgrid(Generic[T], Dict[Vec2, T]):
    def __init__(self, size: Vec2, baseval: T | Callable[[Vec2], T], offgrid: T|None=None, wh=True, wv=False):
        self.size = size
        self.baseval = baseval
        self.offgrid = offgrid
        self.wh, self.wv = wh, wv
    
    def convert(self, conversion: Callable[[T], T2], offgrid=None) -> 'Wrapgrid[T2]':
        data = self.todict()
        new_grid = Wrapgrid[T2](self.size, lambda p: conversion(data[p]), offgrid, self.wh, self.wv)
        new_grid.tolist() # just do a read of every element to get it to set them
        return new_grid
    
    def wrap(self, key) -> Vec2 | None:
        if not hasattr(self, "wv"):
            #basically if we're in the process of unpickling
            return key # we don't have the vars to do anything else yet
        if not (self.wv or 0 <= key[1] < self.size[1]):
            return None
        if not (self.wh or 0 <= key[0] < self.size[0]):
            return None
        return (key[0] % self.size[0], key[1] % self.size[1])

    def __getitem__(self, __key: Vec2) -> T|None:
        k = self.wrap(__key)
        if k == None:
            return self.offgrid
        
        try:
            return super().__getitem__(k)
        except KeyError:
            if callable(self.baseval):
                val = self.baseval(k)
                self[k] = val
                return val
            return self.baseval
    
    def __setitem__(self, __key: Vec2, __value: T):
        k = self.wrap(__key)
        return super().__setitem__(k, __value)

    def _coord_iter(self):
        return ((x,y) for x in range(self.size[0]) for y in range(self.size[1]))

    def tolist(self) -> list[T]:
        return [self[(x,y)] for x,y in self._coord_iter()]

    def todict(self) -> dict[Tuple[int, int], T]:
        return {(x,y):self[(x,y)] for x,y in self._coord_iter()}
    
    def surrounding(self, pos: Vec2, rad=1):
        itms = []
        for y in range(pos[1]-rad, pos[1]+rad+1):
            itms.append([])
            for x in range(pos[0]-rad, pos[0]+rad+1):
                itms[-1].append(self[(x,y)])
        return itms