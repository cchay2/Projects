import pygame
import Constant as constant

pygame.init()


## Minecraft Recipes

WOOD_PLANKS = {
    "id": 4, # WOOD_BLOCK ID
    "name": "Wood Planks",
    "img": pygame.image.load( "graphics/blocks/oak-plank.png" ),
    "tile": pygame.image.load( "graphics/tiles/oak-plank.png" ),
    "color": constant.WOOD_BROWN,
    "cost": 1,
    "r id": 6,
    "amount": 4,
    "position": [
        [ 4, 0, 0, 0, 0, 0, 0, 0, 0 ], 
        [ 0, 4, 0, 0, 0, 0, 0, 0, 0 ], 
        [ 0, 0, 4, 0, 0, 0, 0, 0, 0 ], 
        [ 0, 0, 0, 4, 0, 0, 0, 0, 0 ], 
        [ 0, 0, 0, 0, 4, 0, 0, 0, 0 ], 
        [ 0, 0, 0, 0, 0, 4, 0, 0, 0 ], 
        [ 0, 0, 0, 0, 0, 0, 4, 0, 0 ], 
        [ 0, 0, 0, 0, 0, 0, 0, 4, 0 ], 
        [ 0, 0, 0, 0, 0, 0, 0, 0, 4 ] 
    ]
}

RECIPES = [ WOOD_PLANKS ]