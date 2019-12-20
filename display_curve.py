import pygame
from pygame import *
import sys, random, math, fractions

pygame.init()
Screen_Width = 800
Screen_Height = 600

Total_Display = pygame.display.set_mode((Screen_Width, Screen_Height))

clock = pygame.time.Clock()

pxarray = pygame.PixelArray(Total_Display)

for x in range(0, Screen_Width):
    y = int(math.sin(math.radians(x)) * Screen_Height/2)
    print(math.sin(x), end=' ')
    pxarray[x][y] = 200

running = True

pressed_state = False
while running:
    clock.tick(60)

    for e in pygame.event.get():
        if e == pygame.QUIT:
            Running = False
        if e.type == pygame.KEYDOWN and e.type == pygame.K_ESCAPE:
            running = False

    Mouse_x, Mouse_y = pygame.mouse.get_pos()
    Is_pressed = pygame.mouse.get_pressed()
    Left_key_pressed = Is_pressed[0]
    
    if pressed_state != Left_key_pressed and Left_key_pressed == True:
        print("Mouse is pressed")
            
    if pressed_state != Left_key_pressed and Left_key_pressed == False:
        print("Mouse is not pressed")
		
    # print(Mouse_x, Mouse_y)
    Total_Display.set_at((Mouse_x, Mouse_y), (255, 105, 180))

    pygame.display.flip()
