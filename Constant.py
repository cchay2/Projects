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

##COLORS

WHITE =         ( 255, 255, 255 )
BLACK =         (   0,   0,   0 )

SKY_BLUE =      ( 135, 206, 235 )

GRASS_GREEN =   (   0, 154,  23 )
LEAF_GREEN =    (  48, 183,   0 )

STEEL_GREY =    ( 136, 139, 141 )
STONE_GREY =    ( 145, 142, 133 )

DIRT_BROWN =    ( 116, 102,  59 )
WOOD_BROWN =    ( 164, 116,  73 )



## font
pygame.init()
FONT = pygame.font.SysFont( "Comic Sans MS", 15 )