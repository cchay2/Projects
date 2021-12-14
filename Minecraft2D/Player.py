import pygame
import Constant as constant

class Player():
    def __init__( self, x, y ):
        self.count = 0
        self.scroll = [ 0, 0 ] ## How much to scroll left/right and up/down
        
        self.x = x
        self.y = y
        
        self.width = 30
        self.height = 100
        
        self.chunk_index = 0
        
        self.velocity = 4
        
        self.oldy = self.y
        self.gravity = 6
        self.jump_increment = 10
        self.jump_height = 80
        
        self.is_jumping = False
        self.is_falling = True
    
        self.color = constant.WHITE
        
        self.dRect = pygame.Rect( self.x, self.y, self.width, self.height ) #Draw
        self.Rect = pygame.Rect( self.x, self.y, self.width, self.height ) #x, y, width, height
        
        self.scrolling_right = False
        self.scrolling_left = False
        self.scrolling_up = False
        self.scrolling_down = False
        
        self.hotbar_index = 0
        self.hotbar = [0, 0, 0, 0, 0, 0, 0, 0] # 8 slots
        
        self.dragging = False
        
        for i in range( 24 ):
            self.hotbar.append( 0 )
        
    
    def adjustPos( self ):
        """ Snap the player to the nearest y Coord multiple of 50 when landing """
        
        if self.y % 50 != 0:
            yUp = (self.y//50)*50
            yDown = (self.y//50+1)*50
            
            if yDown - self.y < self.y-yUp:
                self.y = yDown
            else:
                self.y = yUp
            
            self.updateRect()
    
    
    def checkSetChunk( self, CHUNK_LIST ):
        for chunk_index in range( len(CHUNK_LIST) ):
            chunk = CHUNK_LIST[chunk_index]
            if self.x > chunk.start and self.x < chunk.end:
                self.chunk_index = chunk_index
                
    
    def getChunkIndex( self ):
        return self.chunk_index

    def setChunkIndex( self, new_chunkID ):
        self.chunk_index  = new_chunkID
    
    def getCoords( self ):
        return ( self.x, self.y )
        
    def moveRight( self, chunk ):
        if self.checkRight( chunk ) == False:
            self.x += self.velocity
            if self.x+self.scroll[0] > 600:
                self.scrolling_right = True
                self.scroll[0] -= self.velocity
        
    def moveLeft( self, chunk ):
        if self.checkLeft( chunk ) == False:
            self.x -= self.velocity
            if self.x+self.scroll[0] < 200:
                self.scrolling_left = True
                self.scroll[0] += self.velocity
                
        #print( "X: {}; Scroll: {}" .format( self.x, self.scroll[0] ) )
            
    def broadcastJump( self, chunk ):
        if self.is_jumping == False and self.checkFloor( chunk ):
            self.oldy = self.y
        
            self.is_jumping = True

    def jump( self, chunk ):
        """Jump method"""
        if self.is_jumping:
            if self.checkCeiling( chunk ) == False:
                self.y -= self.jump_increment
                if self.y+self.scroll[1] < 150:
                    self.scrolling_up = True
                    self.scroll[1] += self.gravity
            else:
                self.is_jumping = False
        
        if self.y <= self.oldy-self.jump_height:
            self.is_jumping = False
        
    
    def fall( self, chunk ):
        if self.checkFloor( chunk ) == False:
            self.y += self.gravity
            self.updateRect()
            if self.y+self.scroll[1] > 450-self.height:
                self.scrolling_down = True
                self.scroll[1] -= self.gravity
                
                
    ## SCROLLING
    
    def scrollCheck( self ):
        self.scrollRight()
        self.scrollLeft()
        self.scrollUp()
        self.scrollDown()
    
    def scrollRight( self ):
        if self.scrolling_right:
            if self.x+self.scroll[0] > 500:
                self.scroll[0] -= self.velocity
            else:
                self.scrolling_right = False     

    def scrollLeft( self ):
        if self.scrolling_left:
            if self.x+self.scroll[0] < 300:
                self.scroll[0] += self.velocity
            else:
                self.scrolling_left = False        
    
    def scrollUp( self ):
        if self.scrolling_up:
            if self.y+self.scroll[1] < 200:
                self.scroll[1] += self.velocity
            else:
                self.scrolling_up = False
    
    def scrollDown( self ):
        if self.scrolling_down:
            if self.y+self.scroll[1] > 600-self.height:
                self.scroll[1] -= self.velocity
            else:
                self.scrolling_down = False
                
    
    def updateRect( self ):
        """Update Player Location to Rect for accurate drawing"""
        #print( "x scroll:", self.x+self.scroll[0] )
        self.dRect = pygame.Rect( self.x+self.scroll[0], self.y+self.scroll[1], self.width, self.height ) #x, y, width, height
        self.Rect = pygame.Rect( self.x, self.y, self.width, self.height )
        
    def draw( self, surface ):
        """Update Player Rect then Draw"""
        self.updateRect()
        pygame.draw.rect( surface, self.color, self.dRect )
    
    
    def checkCeiling( self, chunk ):
        rect = pygame.Rect( self.x, self.y-self.jump_increment, self.width, self.height )
        
        for block in chunk.blocks:
            if rect.colliderect( block.Rect ):
                self.adjustPos()
                return True
        
        return False
    
    
    def checkFloor( self, chunk ):
        rect = pygame.Rect( self.x, self.y, self.width, self.height+self.velocity )
        
        for block in chunk.blocks:
            if rect.colliderect( block.Rect ):
                self.adjustPos()
                return True
        
        return False
    
    
    def checkRight( self, chunk ):
        rect = pygame.Rect( self.x, self.y, self.width+self.velocity, self.height )
        
        for block in chunk.blocks:
            if rect.colliderect( block.Rect ):
                return True
        
        return False

    def checkLeft( self, chunk ):
        rect = pygame.Rect( self.x-self.velocity, self.y, self.width, self.height )
        
        for block in chunk.blocks:
            if rect.colliderect( block.Rect ):
                return True
        
        return False

    
    def collectBlockHotBar( self, block ):
        for i in range( len(self.hotbar) ): 
            ## First check to see if a block already exists in hotbar
            if self.hotbar[i] != 0:
                if self.hotbar[i]["id"] == block.getID(): # Block exists
                    if self.hotbar[i]["count"] < 64:
                        self.hotbar[i]["count"] += 1
                        return
        
        for i in range( len(self.hotbar) ): # look for a new slot
            if self.hotbar[i] == 0: ## Empty slot to place a block
                self.hotbar[i] = {
                    "id": block.getID(),
                    "name": block.getName(),
                    "img": block.getImage(),
                    "color": block.getColor(),
                    "rect": pygame.Rect( 205+50*i, 535, 40, 40 ),
                    "x" : 205+50*i,
                    "y": 535,
                    "drag": False,
                    "half": False,
                    "count": 1,
                    "half count": 0
                }
                break
    
    
    def findEmptyHotbarSlot( self, mouse_pos ):
        """ Will return int of range 8 to indicate which position to swap the block to """
        for i in range(8):
            if mouse_pos[0] >= 200+50*i and mouse_pos[0] <= 200+50*(i+1) and mouse_pos[1] >= 530 and mouse_pos[1] <= 580:
                return i
        
        print("break")
        return False
        
            
                
            
                
    