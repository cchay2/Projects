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

class SpatialHash(object):
    def __init__( self, cell_size=10.0 ):
        self.cell_size = cell_size
        self.d = {}
    
    def add( self, cell_coord, obj ):
        """Add object obj to the cell at cell_coord"""
        try:
            self.d.setdefault( cell_coord, set() ).add(obj)
        except KeyError:
            self.d[cell_coord] = set( (obj,) )
    