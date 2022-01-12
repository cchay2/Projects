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

class Chunk:
    def __init__( self, start, end ):
        """Each chunk is 10,000 pixels wide, or 200 blocks"""
        self.start = start # tuple
        self.end = end
    
        self.blocks = []
    
    
    def getStart( self ):
        return self.start
    
    def getEnd( self ):
        return self.end
    
    def addBlock( self, block ):
        #self.blocks.append(block)
        for b in self.blocks:
            if block.isColliding( b ):
                return
        else:
            self.blocks.append(block)
    
    
        