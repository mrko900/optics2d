import sys

import pygame
from typing import List
from optics import *
from dataclasses import dataclass


pygame.init()

WINDOW_SIZE = (800, 600)
BACKGROUND_COLOR = (255, 255, 255)
MIRROR_COLOR = (0, 0, 0)  # Black
RAY_COLOR = (255, 0, 0)  # Red
INF = 1e5

# Create the window
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Optics")


def render(snapshot: Snapshot):
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill(BACKGROUND_COLOR)
    for mirror in snapshot.mirrors:
        a = mirror.center + mirror.normal.rotate_ccw() * mirror.length * 0.5
        b = mirror.center + mirror.normal.rotate_cw() * mirror.length * 0.5
        pygame.draw.line(screen, MIRROR_COLOR, (a.x, a.y), (b.x, b.y), 2)
        c = mirror.center + mirror.normal * 50
        pygame.draw.line(screen, (0, 0, 255), (mirror.center.x, mirror.center.y),
                         (c.x, c.y), 3)
    for path in snapshot.ray_paths:
        # print(path)
        if len(path) < 2:
            continue
        prev = path[0]
        path[-1] = path[-2] + (path[-1] - path[-2]) * INF
        for cur in path[1:]:
            pygame.draw.line(screen, RAY_COLOR, (prev.x, prev.y), (cur.x, cur.y), 1)
            prev = cur
    pygame.display.flip()
