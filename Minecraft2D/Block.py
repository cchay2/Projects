import pygame, Constant

class Block():
    def __init__( self, id, name, color, image, tile, x, y, transparent=False ):
        self.id = id
        self.name = name
        self.color = color
        self.image = image
        self.tile = tile
        self.x = x
        self.y = y
        
        self.width = 50
        self.height = 50
        
        self.drawn = False
        self.transparent = transparent
        
        self.Rect = pygame.Rect( self.x, self.y, self.width, self.height )
    
    
    def getObject( self, block_dict ):
        return Block( block_dict["id"], block_dict["name"], block_dict["color"], block_dict["img"], block_dict["tile"], block_dict["x"], block_dict["y"] )
    
    
    def __str__( self ):
        return "X : " + str(self.x) + "; Y: " + str(self.y)
    
    def getName( self ):
        return self.name
    
    def getID( self ):
        return self.id
    
    def getImage( self ):
        return self.image
    
    def getTile( self ):
        return self.tile

    def getColor( self ):
        return self.color
        
    def isOnScreen( self, window ):
        if self.x > window["x"][0]-self.width and self.x < window["x"][1]: # Block is present on screen even if it's just 1 pixel
            if self.y > window["y"][0]-self.height and self.y < window["y"][1]:
                return True
    
    def draw( self, surface, window, scroll ):
        rect = pygame.Rect( self.x + scroll[0], self.y+scroll[1], self.width, self.height )
        if self.isOnScreen( window ):
            self.drawn = True
            if self.tile == None:
                pygame.draw.rect( surface, self.color, rect, 5 )
            else:
                surface.blit( self.tile, (self.x+scroll[0], self.y+scroll[1]) )
        else:
            self.drawn = False
    
    
    def updateRect( self ):
        """Updates Rectangle"""
        self.Rect = pygame.Rect( self.x, self.y, self.width, self.height )
    
    
    def adjustPosition( self ):
        """Adjusts the block so it snaps to a grid and updates rect accordingly"""
        self.x = ( self.x//50 )*50
        self.y = ( self.y//50 )*50
            
        self.updateRect()
        
        #print( "x: {}; y: {}" .format( self.x, self.y ) )
    

    def isColliding( self, block ):
        """Checking to see if self.block is colliding with block arg"""
        if self.x+self.width > block.x and self.x < block.x+block.width and self.y+self.height > block.y and self.y < block.y+block.height:
            return True
        
        return False
        