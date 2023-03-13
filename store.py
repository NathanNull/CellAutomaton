tsize = 12
size = tuple(s*tsize for s in (64, 66))

def gen_tiled(tile, sv, sh):
    tilelist = [list(map(int, str(n).zfill(2).split(","))) for n in tile.split()]
    offsets = [(i,j) 
            for i in range(0, (size[0]//(tsize*sh))*sh, sh) 
            for j in range(0, (size[1]//(tsize*sv))*sv, sv)]
    return [(o[0]+g[0], o[1]+g[1]) for g in tilelist for o in offsets]

tiled_setups = [
gen_tiled("""
    1,0 2,0 3,0 4,0
0,1             4,1
                4,2
0,3         3,3
""", 6, 8),
gen_tiled("""
    1,0
        2,1
0,2 1,2 2,2
""", 5, 5)
]

setup = tiled_setups[0]