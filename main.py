from cell import Cell
from wrapgrid import Wrapgrid
import store, time, pygame
import multiprocessing.pool as mp

def avg(iter):
    iter = list(iter)
    return sum(iter) / max(len(iter), 1)

def update(c: 'Cell', states: Wrapgrid[int]):
    c.update(states)
    return c.state

if __name__ == "__main__":
    # init
    pygame.init()
    screen = pygame.display.set_mode(store.size, display=1)
    clock = pygame.time.Clock()

    # grid stuff
    grid = Wrapgrid[Cell](tuple(s//store.tsize for s in store.size), lambda p: Cell(p), wv=True)
    grid_sprites = pygame.sprite.Group(grid.tolist())
    print(grid.size[0]*grid.size[1], "cells running")

    # fps tracker setup
    fps = []
    fps_t = pygame.event.custom_type()
    pygame.time.set_timer(pygame.event.Event(fps_t), 5000)

    p = mp.ThreadPool()

    # --------------------- MAIN LOOP ---------------------------
    run = True
    while run:
        ti = time.time() * 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == fps_t:
                print(f"est: {1000/avg(f[0] for f in fps):.4f}\nreal: {1000/avg(f[1] for f in fps):.4f}")
                fps = []
        
        t1 = time.time() * 1000

        states = grid.convert(lambda c: c.state)
        states.baseval = None
        p.starmap(update, ((s, states) for s in grid_sprites.sprites()))

        t2 = time.time() * 1000

        screen.fill((0,0,0))
        grid_sprites.draw(screen)
        pygame.display.update()
        fps.append([clock.tick(10)])

        tf = time.time() * 1000
        fps[-1].append(tf-ti)
    pygame.quit()