import pygame, sys
import Constant as constant
import Player
import Block
import Chunk

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SURFACE_HEIGHT = SCREEN_HEIGHT//2 ## Should be 300


SCREEN = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
    
    pygame.display.update()
