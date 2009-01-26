#!/usr/bin/env python

import sys, random
import pygame as pyg
from pygame.locals import *

SCREEN_SIZE = (10, 15)
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
FALL_DELAY = 500

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
    def __init__(self, field):
        self.field = field

    def create(self, type):
        self.type = type
        self.c = [[False] * 4 for i in range(4)]
        for i in BLOCK_DEF[type][0]: self.c[i[0]][i[1]] = True
        self.size = BLOCK_DEF[type][1]
        self.sq = SQUARES[self.type]
        self.x, self.y = 0, 0

    def collides(self, dx, dy):
        for i in range(4):
            for j in range(4):
                a, b = self.y + dy + j, self.x + dx + i
                if self.c[i][j] and (a < 0 or b < 0 or a >= SCREEN_SIZE[1] or b >= SCREEN_SIZE[0] or self.field.f[a][b]):
                    return True
        return False

    def move(self, dx, dy):
        if self.collides(dx, dy):
            if dy >= 1:
                for i in range(4):
                    for j in range(4):
                        if self.c[i][j]:
                            self.field.f[self.y + dy + j - 1][self.x + i] = self.sq
            return True

        self.x += dx
        self.y += dy
        return False

    def rotate(self, dir):
        d = [[False] * 4 for i in range(4)]
        for i in range(4):
            for j in range(4):
                if dir:
                    d[self.size - j - 1][i] = self.c[i][j]
                else:
                    d[j][self.size - i - 1] = self.c[i][j]
        for i in range(4):
            for j in range(4):
                a, b = self.y + j, self.x + i
                if d[i][j] and (a < 0 or b < 0 or a >= SCREEN_SIZE[1] or b >= SCREEN_SIZE[0] or self.field.f[a][b]):
                    return
        self.c = d

    def draw(self, screen):
        for i in range(4):
            for j in range(4):
                if self.c[i][j]:
                    screen.blit(self.sq, ((self.x + i) * SQ_SIZE, (self.y + j) * SQ_SIZE))

class Field:
    def __init__(self):
        self.f = [[None] * SCREEN_SIZE[0] for i in range(SCREEN_SIZE[1])]

    def check_filled(self):
        for i in range(SCREEN_SIZE[1]):
            while all(self.f[i]):
                del self.f[i]
                self.f.insert(0, [None] * SCREEN_SIZE[0])

    def draw(self, screen):
        for i in range(SCREEN_SIZE[1]):
            for j in range(SCREEN_SIZE[0]):
                if self.f[i][j]:
                    screen.blit(self.f[i][j], (j * SQ_SIZE, i * SQ_SIZE))

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

    field = Field()

    block = Block(field)
    block.create(random.randint(0, 6))

    last_fall = 0
    while True:
        for event in pyg.event.get():
            if event.type == QUIT: return
            elif event.type == KEYDOWN:
                k = event.key
                if k == K_ESCAPE: return
                elif k == K_UP: block.rotate(True)
                elif k == K_LEFT: block.move(-1, 0)
                elif k == K_RIGHT: block.move(1, 0)
                elif k == K_DOWN:
                    while not block.move(0, 1): pass

        time = pyg.time.get_ticks()
        if time - last_fall >= FALL_DELAY:
            if block.move(0, 1):
                field.check_filled()
                block.create(random.randint(0, 6))
            last_fall = time

        screen.fill(SCREEN_BG_COLOR)
        block.draw(screen)
        field.draw(screen)
        pyg.display.flip()

if __name__ == '__main__':
    main()
