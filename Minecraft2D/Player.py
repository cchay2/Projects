import pygame
import Constant as constant
import Recipes as recipes
import Block as block
import Skin as skin
import math

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
        
        self.direction = "left"
        
        self.oldy = self.y
        self.gravity = 6
        self.jump_increment = 10
        self.jump_height = 80
        
        self.is_walking = False
        self.is_jumping = False
        self.is_falling = True
    
        self.color = constant.WHITE
        
        self.skin = None
        
        self.dRect = pygame.Rect( self.x, self.y, self.width, self.height ) #Draw
        self.Rect = pygame.Rect( self.x, self.y, self.width, self.height ) #x, y, width, height
        
        self.hotbar_rect = pygame.Rect( 175, 530, 450, 50 )
        self.inventory_rect = pygame.Rect( 125, 100, 550, 400 )
        
        self.scrolling_right = False
        self.scrolling_left = False
        self.scrolling_up = False
        self.scrolling_down = False
        
        self.hotbar_size = 9
        self.hotbar_index = 0
        self.hotbar = [] # 9 slots
        self.inventory_slots = []
        
        self.dragging = False
        
        for i in range( self.hotbar_size*4 ):
            self.hotbar.append( 0 )
        
        for row in range( 3 ):
            for column in range( 9 ):
                self.inventory_slots.append( ( 175+50*(column), 350+50*(row) ) )
            
        
        
        self.show_inventory = False
        self.craft_table = [ 0, 0, 0, 0 ]
        self.craft_slots = []
        
        for i in range( 4 ):
            self.hotbar.append( 0 )
        
        for row in range( 2 ):
            for column in range( 2 ):
                self.craft_slots.append( ( 450+50*(column), 160+50*(row) ) )

        self.hotbar.append(0) ## for final crafting slot
        
        self.crafting = False
    
    def setSkin( self, skin ):
        """Initiate all the rectangle positions"""
        self.skin = skin
        
        self.skin.bot_arm_rect.x = self.x+7
        self.skin.bot_arm_rect.y = self.y+30
        
        self.skin.bot_leg_rect.x = self.x+7
        self.skin.bot_leg_rect.y = self.y+30+35
        
        self.skin.body_rect.x = self.x+7
        self.skin.body_rect.y = self.y+30
        
        self.skin.head_left_rect.x = self.x
        self.skin.head_left_rect.y = self.y
        
        self.skin.head_right_rect.x = self.x
        self.skin.head_right_rect.y = self.y
            
        self.skin.top_leg_rect.x = self.x+7
        self.skin.top_leg_rect.y = self.y+30+35
        
        self.skin.top_arm_rect.x = self.x+7
        self.skin.top_arm_rect.y = self.y+30
        
    
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
    
    
    def headAnimation( self, mouse_pos ):
        center_point = (self.skin.getHeadRightRect().centerx, self.skin.getHeadRightRect().centery)
        adj = mouse_pos[1] - center_point[1]
        opp = mouse_pos[0] - center_point[0]
        try:
            angle = round( math.atan(adj/opp)*100 )
        except:
            angle = 0
            
        if -60 < angle < 60:
            if angle < 0:
                self.skin.head_margin = -(-angle//5)
            else:
                self.skin.head_margin = angle//5
            
            
            self.skin.setHeadAngle( -angle )
            
        
        if mouse_pos[0] - center_point[0] >= 0:
            self.skin.head_right = pygame.transform.rotate( self.skin.head_right_r, self.skin.getHeadAngle() )
            self.direction = "right"
        else:
            self.skin.head_left = pygame.transform.rotate( self.skin.head_left_r, self.skin.getHeadAngle() )
            self.direction = "left"
    
    
    def walkAnimation( self ):
        self.topArmWalkAnimation()
        self.botArmWalkAnimation()
        self.topLegWalkAnimation()
        self.botLegWalkAnimation()
    
    def topArmWalkAnimation( self ):
        if self.skin.swing_arm == "up":
            if self.skin.getTopArmAngle() <= 50:
                self.skin.changeTopArmAngle( 10 )
                self.skin.top_arm_margin += 2
                self.skin.top_arm = pygame.transform.rotate( self.skin.top_arm_r, self.skin.getTopArmAngle() )
            else:
                self.skin.swing_arm = "down"
                self.skin.top_arm_margin = 4
        else:
            if self.skin.getTopArmAngle() >= -50:
                self.skin.changeTopArmAngle( -10 )
                self.skin.top_arm_margin -= 2
                self.skin.top_arm = pygame.transform.rotate( self.skin.top_arm_r, self.skin.getTopArmAngle() )
            else:
                self.skin.swing_arm = "up"
                self.skin.top_arm_margin = -16
                
    
    def botArmWalkAnimation( self ):
        if self.skin.swing_arm == "down":
            if self.skin.getBotArmAngle() <= 50:
                self.skin.changeBotArmAngle( 10 )
                self.skin.bot_arm_margin += 2
                self.skin.bot_arm = pygame.transform.rotate( self.skin.bot_arm_r, self.skin.getBotArmAngle() )
            else:
                self.skin.bot_arm_margin = 4
        else:
            if self.skin.getBotArmAngle() >= -50:
                self.skin.changeBotArmAngle( -10 )
                self.skin.bot_arm_margin -= 2
                self.skin.bot_arm = pygame.transform.rotate( self.skin.bot_arm_r, self.skin.getBotArmAngle() )
            else:
                self.skin.bot_arm_margin = -16
                
    
    def botLegWalkAnimation( self ):
        if self.skin.swing_arm == "up":
            if self.skin.getBotLegAngle() <= 50:
                self.skin.changeBotLegAngle( 10 )
                self.skin.bot_leg_margin += 2
                self.skin.bot_leg = pygame.transform.rotate( self.skin.bot_leg_r, self.skin.getBotLegAngle() )
            else:
                self.skin.bot_leg_margin = 4
        else:
            if self.skin.getBotLegAngle() >= -50:
                self.skin.changeBotLegAngle( -10 )
                self.skin.bot_leg_margin -= 2
                self.skin.bot_leg = pygame.transform.rotate( self.skin.bot_leg_r, self.skin.getBotLegAngle() )
            else:
                self.skin.bot_leg_margin = -16
                
    
    def topLegWalkAnimation( self ):
        if self.skin.swing_arm == "down":
            if self.skin.getTopLegAngle() <= 50:
                self.skin.changeTopLegAngle( 10 )
                self.skin.top_leg_margin += 2
                self.skin.top_leg = pygame.transform.rotate( self.skin.top_leg_r, self.skin.getTopLegAngle() )
            else:
                self.skin.top_leg_margin = 4
        else:
            if self.skin.getTopArmAngle() >= -50:
                self.skin.changeTopLegAngle( -10 )
                self.skin.top_leg_margin -= 2
                self.skin.top_leg = pygame.transform.rotate( self.skin.top_leg_r, self.skin.getTopLegAngle() )
            else:
                self.skin.top_leg_margin = 0
    
    
    def resetAnimation( self ):
        self.skin.top_arm_margin = 0
        self.skin.bot_arm_margin = 0
        self.skin.top_leg_margin = 0
        self.skin.bot_leg_margin = 0
        
        self.skin.top_arm = self.skin.top_arm_r
        self.skin.bot_arm = self.skin.bot_arm_r
        self.skin.top_leg = self.skin.top_leg_r
        self.skin.bot_leg = self.skin.bot_leg_r
        
        self.skin.resetTopArmAngle()
        self.skin.resetBotArmAngle()
        self.skin.resetTopLegAngle()
        self.skin.resetBotLegAngle()

    
    
    def updateSkinRects( self, x, y ):
        self.skin.head_right_rect.x = x+self.skin.head_margin
        self.skin.head_left_rect.x = x+self.skin.head_margin
        self.skin.body_rect.x = x+8
        self.skin.top_arm_rect.x = x+8+self.skin.top_arm_margin
        self.skin.bot_arm_rect.x = x+8+self.skin.bot_arm_margin
        self.skin.top_leg_rect.x = x+8+self.skin.top_leg_margin
        self.skin.bot_leg_rect.x = x+8+self.skin.bot_leg_margin
        
        self.skin.head_right_rect.y = y
        self.skin.head_left_rect.y = y
        self.skin.body_rect.y = y+30
        self.skin.top_arm_rect.y = y+30
        self.skin.bot_arm_rect.y = y+30
        self.skin.top_leg_rect.y = y+60
        self.skin.bot_leg_rect.y = y+60
    
        
    def draw( self, surface, mouse_pos ):
        """Update Player Rect then Draw"""
        self.updateRect()
        #pygame.draw.rect( surface, self.color, self.dRect )
        
        x = self.x+self.scroll[0]
        y = self.y+self.scroll[1]
        
        self.updateSkinRects( x, y )
        
        
        if self.is_walking:
            self.walkAnimation()
        else:
            self.resetAnimation()
            
            
        self.headAnimation( mouse_pos )    
        
        surface.blit( self.skin.getBotArm(), self.skin.getBotArmRect() )
        surface.blit( self.skin.getBotLeg(), self.skin.getBotLegRect() )
        surface.blit( self.skin.getBody(), self.skin.getBodyRect() )
        
        if self.direction == "left":
            surface.blit( self.skin.getHeadLeft(), self.skin.getHeadLeftRect() )
        else:
            surface.blit( self.skin.getHeadRight(), self.skin.getHeadRightRect() )
            
        surface.blit( self.skin.getTopLeg(), self.skin.getTopLegRect() )
        surface.blit( self.skin.getTopArm(), self.skin.getTopArmRect() )
    
    
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

    
    def collectBlockHotBar( self, block, amount=1 ):
        for i in range( 36 ): 
            ## First check to see if a block already exists in hotbar
            if self.hotbar[i] != 0:
                if self.hotbar[i]["id"] == block.getID(): # Block exists
                    if self.hotbar[i]["count"] < 64:
                        self.hotbar[i]["count"] += amount
                        return
        
        for i in range( len(self.hotbar) ): # look for a new slot
            if self.hotbar[i] == 0: ## Empty slot to place a block
                self.hotbar[i] = {
                    "id": block.getID(),
                    "name": block.getName(),
                    "img": block.getImage(),
                    "tile": block.getTile(),
                    "color": block.getColor(),
                    "rect": pygame.Rect( 180+50*i, 535, 40, 40 ),
                    "x" : 180+50*i,
                    "y": 535,
                    "drag": False,
                    "half": False,
                    "count": amount,
                    "half count": 0
                }
                break
    
    def printHotbar( self ):
        for i in self.hotbar:
            print(i)
        print()
    
    
    def findEmptyHotbarSlot( self, mouse_pos ):
        """ Will return int of range 8 to indicate which position to swap the block to """
        for i in range( self.hotbar_size ):
            if mouse_pos[0] >= 175+50*i and mouse_pos[0] <= 175+50*(i+1) and mouse_pos[1] >= 530 and mouse_pos[1] <= 580:
                return i
            
        for i in self.inventory_slots:
            if mouse_pos[0] >= i[0] and mouse_pos[0] <= i[0]+50 and mouse_pos[1] >= i[1] and mouse_pos[1] <= i[1]+50:
                return self.inventory_slots.index( i )+9
        
        for i in self.craft_slots:
            if mouse_pos[0] >= i[0] and mouse_pos[0] <= i[0]+50 and mouse_pos[1] >= i[1] and mouse_pos[1] <= i[1]+50:
                return self.craft_slots.index( i )+36
        
        if mouse_pos[0] >= 610 and mouse_pos[0] <= 610+50 and mouse_pos[1] >= 185 and mouse_pos[1] <= 185+50:
            return 40
            
            
        #print("break")
        return -1
    
    def drawInventory( self, surface, rows, columns, slot, x, y, mouse_pos, inventory ):
        for row in range( rows ): ## DRAW INVENTORY BLOCKS
            for column in range( columns ):
                #print("slot:", slot)
                if inventory[slot] != 0:
                    if inventory[slot]["count"] == 0: ## Player has no more blocks left, set to 0 since last block was used
                        inventory[slot] = 0
                    else: ## DRAW HOTBAR BLOCKS
                        if inventory[slot]["half"] == True: # Player is dragging with right mouse:
                            if inventory[slot]["count"] > 1:
                                surface.blit( inventory[slot]["img"], ( x+50*column, y+50*row ) )
                                surface.blit( constant.FONT.render( str(inventory[slot]["count"]-inventory[slot]["half count"]), False, constant.WHITE ), ( x+50*column+25, y+50*row+25 ) )

                                surface.blit( inventory[slot]["img"], ( mouse_pos[0]-25, mouse_pos[1]-25 ) )
                                surface.blit( constant.FONT.render( str(inventory[slot]["half count"]), False, constant.WHITE ), ( mouse_pos[0], mouse_pos[1] ) )
                            
                            else:
                                surface.blit( inventory[slot]["img"], ( mouse_pos[0]-25, mouse_pos[1]-25 ) )
                                surface.blit( constant.FONT.render( str(inventory[slot]["half count"]), False, constant.WHITE ), ( mouse_pos[0], mouse_pos[1] ) )
                        
                        elif inventory[slot]["drag"] == False: # Block is not being dragged so draw underfirst so it is underneath                  
                            surface.blit( inventory[slot]["img"], ( x+50*column, y+50*row ) )
                            surface.blit( constant.FONT.render( str(inventory[slot]["count"]), False, constant.WHITE ), ( x+50*column+25, y+50*row+25 ) )
                        else:
                            surface.blit( inventory[slot]["img"], ( mouse_pos[0]-25, mouse_pos[1]-25 ) )
                            surface.blit( constant.FONT.render( str(inventory[slot]["count"]), False, constant.WHITE ), ( mouse_pos[0], mouse_pos[1] ) )
                slot += 1
    
    
    def addToInventory( self, mouse_pos, inventory ):
            self.dragging = False
            
            for i in range( len( inventory ) ):
                if inventory[i] != 0:
                    if inventory[i]["drag"] == True: # We found the block
                        inventory[i]["drag"] = False
                        inventory[i]["half"] = False
                        break
            
            
            #if inventory[i] != 0:
            if self.hotbar_rect.collidepoint( mouse_pos ) or self.inventory_rect.collidepoint( mouse_pos ):
                
                slotIndex = self.findEmptyHotbarSlot( mouse_pos )
                
                if self.crafting == True:
                    #print("Adding block to inventory")
                    self.crafting = False
                    new_block = block.Block.getObject( block.Block, self.hotbar[40] )
                    self.collectBlockHotBar( new_block, self.hotbar[40]["count"] )
                    
                
                if slotIndex == 40:
                    pass
                elif slotIndex != -1: ## Handle False being thrown when player clcks on non-clickable :
        
                    if inventory[slotIndex] != 0 and inventory[i] != 0: # Existing block at position slotIndex
                        if slotIndex != i: #Make sure the id's are different
                            if inventory[slotIndex]["id"] == inventory[i]["id"]: #combine the stack
                                if inventory[i]["half count"] > 0:
                                    if inventory[slotIndex]["count"] + inventory[i]["half count"] > 64:
                                        remainder = inventory[i]["half count"] + inventory[slotIndex]["count"] - 64
                                        inventory[slotIndex]["count"] = 64
                                        inventory[i]["count"] += ( remainder - inventory[i]["half count"] )
                                        inventory[i]["half count"] = 0
                                    else: # adding blocks to a stack less than full 
                                        inventory[slotIndex]["count"] += inventory[i]["half count"]
                                        inventory[i]["count"] -= inventory[i]["half count"]
                                        inventory[i]["half count"] = 0
                                else:
                                    if inventory[slotIndex]["count"] + inventory[i]["count"] >= 64:
                                        remainder = inventory[i]["count"] + inventory[slotIndex]["count"] - 64
                                        inventory[slotIndex]["count"] = 64
                                        inventory[i]["count"] = remainder
                                        
                                    else:
                                        inventory[slotIndex]["count"] += inventory[i]["count"]
                                        inventory[i] = 0
                            else:
                                target_block = inventory[slotIndex]
                                inventory[slotIndex] = inventory[i] # Move the dragged block to the new position
                                inventory[i] = target_block # Finish swapping the blocks
                    else:
                        if inventory[i] != 0:
                            if inventory[i]["half count"] > 0:
                                inventory[slotIndex] = inventory[i].copy() # Drag the block to the new spot
                                
                                inventory[slotIndex]["count"] = inventory[slotIndex]["half count"]
                                inventory[slotIndex]["half count"] = 0
                                
                                inventory[i]["count"] = inventory[i]["count"] - inventory[i]["half count"]
                                inventory[i]["half count"] = 0 # Vacate the old spot
                            else:
                                inventory[slotIndex] = inventory[i] # Drag the block to the new spot
                                inventory[i] = 0 # Vacate the old spot
    
    
    def craft( self ):
        block_id = 0
        for i in range( 36, 40 ):
            if self.hotbar[i] != 0:
                self.craft_table[ i-36 ] = self.hotbar[i]["id"]
                block_id = self.hotbar[i]["id"]
            else:
                self.craft_table[ i-36 ] = 0
        
        table_copy = self.craft_table[:]
        for i in range(5):
            table_copy.append(0)
        
        #print("RECIPES")
        for recipe in recipes.RECIPES:
            if recipe[ "id" ] == block_id:
                for i in recipe[ "position" ]:
                    #print( "Table :", self.craft_table )
                    #print( "Copy  : ", table_copy )
                    #print( "Recipe: ", i )
                    if table_copy == i:
                        self.hotbar[40] = {
                                            "id": recipe["r id"],
                                            "name": "Wood Plank",
                                            "img": recipe["img"],
                                            "tile": recipe["tile"],
                                            "color": recipe["color"],
                                            "rect": pygame.Rect( 615, 190, 40, 40 ),
                                            "x" : 615,
                                            "y": 190,
                                            "drag": False,
                                            "half": False,
                                            "count": recipe["amount"],
                                            "half count": 0
                                        }
                        return
                else:
                    self.hotbar[40] = 0
            else:
                self.hotbar[40] = 0
    
    
    def craftBlock( self ):
        for block in self.hotbar[ 36:40 ]:
            #print( block )
            if block != 0:
                block["count"] -= 1
                if block["count"] == 0:
                    block = 0
                        
