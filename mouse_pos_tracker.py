import pygame
from pygame import *
import sys, random, math, fractions

pygame.init()
Screen_Width = 800
Screen_Height = 600

Total_Display = pygame.display.set_mode((Screen_Width, Screen_Height))

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(60)

    for e in pygame.event.get():
        if e == pygame.QUIT:
            Running = False
        if e.type == pygame.KEYDOWN and e.type == pygame.K_ESCAPE:
            running = False

    Mouse_x, Mouse_y = pygame.mouse.get_pos()
    print(Mouse_x, Mouse_y)
    Total_Display.set_at((Mouse_x, Mouse_y), (255, 105, 180))

    pygame.display.flip()
