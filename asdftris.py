#!/usr/bin/env python

import sys
import pygame as pyg
from pygame.locals import *

SCREEN_SIZE = (10, 25)
SCREEN_BG_COLOR = (0, 0, 0)
SQ_SIZE = 20
SQ_BORDER1 = (204, 204, 204)
SQ_BORDER2 = (0, 0, 0)
BLOCK_COLORS = (
    (0, 255, 255),  # I
    (0, 0, 255),    # J
    (255, 165, 0),  # L
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (160, 32, 240), # T
    (255, 0, 0)     # Z
)

BLOCK_DEF = (
    (((0, 1), (1, 1), (2, 1), (3, 1)), 4), # I
    (((0, 0), (0, 1), (1, 1), (2, 1)), 3), # J
    (((0, 1), (1, 1), (2, 0), (2, 1)), 3), # L
    (((0, 0), (1, 0), (0, 1), (1, 1)), 2), # O
    (((0, 1), (1, 0), (1, 1), (2, 0)), 3), # S
    (((0, 1), (1, 0), (1, 1), (2, 1)), 3), # T
    (((0, 0), (1, 0), (1, 1), (2, 1)), 3)  # Z
)

SQUARES = []

class Block:
    def draw(self, screen):
        for i in range(4):
            for j in range(4):
                if self.c[i][j]:
                    screen.blit(SQUARES[self.type], ((self.pos[0] + i) * SQ_SIZE, (self.pos[1] + j) * SQ_SIZE))

    def create(self, type):
        self.type = type
        self.c = [[False] * 4 for i in range(4)]
        for i in BLOCK_DEF[type][0]: self.c[i[0]][i[1]] = True
        self.size = BLOCK_DEF[type][1]
        self.color = BLOCK_COLORS[type]
        self.pos = [0, 0]

    def rotate(self, dir):
        d = [[False] * 4 for i in range(4)]
        for i in range(4):
            for j in range(4):
                if dir:
                    d[self.size - j - 1][i] = self.c[i][j]
                else:
                    d[j][self.size - i - 1] = self.c[i][j]
        self.c = d

class Grid:
    def __init__(self):
        self.grid = [[None] * SCREEN_SIZE[0] for i in SCREEN_SIZE[1]]

    def add(self, block):
        pass

def main():
    pyg.init()
    pyg.mouse.set_visible(0)
    pyg.display.set_caption('asdftris')

    screen = pyg.display.set_mode((SCREEN_SIZE[0] * SQ_SIZE, SCREEN_SIZE[1] * SQ_SIZE))

    for color in BLOCK_COLORS:
        i = pyg.Surface((SQ_SIZE, SQ_SIZE))
        i.fill(color)
        pyg.draw.line(i, SQ_BORDER1, (0, 0), (0, SQ_SIZE-1))
        pyg.draw.line(i, SQ_BORDER1, (0, 0), (SQ_SIZE-1, 0))
        pyg.draw.line(i, SQ_BORDER2, (0, SQ_SIZE-1), (SQ_SIZE-1, SQ_SIZE-1))
        pyg.draw.line(i, SQ_BORDER2, (SQ_SIZE-1, 0), (SQ_SIZE-1, SQ_SIZE-1))
        SQUARES.append(i)

    b = Block()
    b.create(0)

    while True:
        for event in pyg.event.get():
            if event.type == QUIT: return
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE: return
                elif event.key == K_a: b.rotate(True)
                elif event.key == K_b: b.rotate(False)
                elif event.key == K_0: b.create(0)
                elif event.key == K_1: b.create(1)
                elif event.key == K_2: b.create(2)
                elif event.key == K_3: b.create(3)
                elif event.key == K_4: b.create(4)
                elif event.key == K_5: b.create(5)
                elif event.key == K_6: b.create(6)

        screen.fill(SCREEN_BG_COLOR)
        b.draw(screen)
        pyg.display.flip()

if __name__ == '__main__':
    main()
