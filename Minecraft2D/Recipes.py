""" Copyright (C) 2022  Christopher Chay

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>. """

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