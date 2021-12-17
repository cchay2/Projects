import pygame, sys, random
import Constant as constant
import Player
import Block
import Chunk

pygame.init()

pygame.display.set_caption('Minecraft 2D')

item_count_font = pygame.font.SysFont( "Comic Sans MS", 15 )

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SURFACE_HEIGHT = SCREEN_HEIGHT//2 ## Should be 300

WORLD_LIMIT_X = ( -100000, 100000 ) # Each block is 50x50, and for 2000 blocks left and right
WORLD_LIMIT_Y = ( SURFACE_HEIGHT, SURFACE_HEIGHT + 50*50 ) # 50 blocks down

SCREEN = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )


GRASS_BLOCK = pygame.image.load( "graphics/blocks/grass.png" ).convert_alpha()
DIRT_BLOCK = pygame.image.load( "graphics/blocks/dirt.png" ).convert_alpha()
STONE_BLOCK = pygame.image.load( "graphics/blocks/stone.png" ).convert_alpha()
WOOD_BLOCK = pygame.image.load( "graphics/blocks/wood.png" ).convert_alpha()
LEAF_BLOCK = pygame.image.load( "graphics/blocks/leaves.png" ).convert_alpha()

ARROW = pygame.image.load( "graphics/other/crafting_arrow.png" ).convert_alpha()

window = {
    "x": [ 0, SCREEN_WIDTH ],
    "y": [ 0, SCREEN_HEIGHT ]
}

BLOCK_LIST = []
CHUNK_LIST = []
CHUNK_SIZE = 20000 #20,000 in actuality it is 20,200 

    

## Generate the chunks
for chunk_width in range( WORLD_LIMIT_X[0], WORLD_LIMIT_X[1]-CHUNK_SIZE//2, CHUNK_SIZE//2 ): #Chunk Size = 10,000
    CHUNK_LIST.append( Chunk.Chunk( chunk_width, chunk_width+CHUNK_SIZE//2 ) )


# Old Slow way of generating world
for yPos in range( WORLD_LIMIT_Y[0], WORLD_LIMIT_Y[1], 50  ):
    for xPos in range( WORLD_LIMIT_X[0], WORLD_LIMIT_X[1], 50 ):
        BLOCK_LIST.append( Block.Block( 0, "Grass Block", constant.GRASS_GREEN, GRASS_BLOCK, xPos, yPos ) )
        

## Generate all blocks
for yPos in range( WORLD_LIMIT_Y[0], WORLD_LIMIT_Y[1], 50  ):
    for xPos in range( WORLD_LIMIT_X[0], WORLD_LIMIT_X[1], 50 ):
        for chunk in CHUNK_LIST: # add blocks to the chunk
            if xPos >= chunk.getStart() and xPos < chunk.getEnd():
                if yPos >= SURFACE_HEIGHT and yPos < SURFACE_HEIGHT + 50:
                    chunk.blocks.append( Block.Block( 1, "Grass Block", constant.GRASS_GREEN, GRASS_BLOCK, xPos, yPos ) )
                elif yPos >= SURFACE_HEIGHT+50 and yPos < SURFACE_HEIGHT + 50*4:
                    chunk.blocks.append( Block.Block( 2, "Dirt Block", constant.DIRT_BROWN, DIRT_BLOCK, xPos, yPos ) )
                else:
                    chunk.blocks.append( Block.Block( 3, "Stone Block", constant.STONE_GREY, STONE_BLOCK, xPos, yPos ) )


    

clock = pygame.time.Clock()

player = Player.Player( SCREEN_WIDTH//2, SCREEN_HEIGHT//2-100 )
place_cd = False


## Set Player Chunk
player.checkSetChunk( CHUNK_LIST )


def spawnTree( x, chunk ):
    tree_height = random.randint( 3, 5 )
    for i in range( tree_height ):
        chunk.blocks.append( Block.Block( 4, "Wood Block", constant.WOOD_BROWN, WOOD_BLOCK, x, SURFACE_HEIGHT-50*(i+1) ) )
    
    chunk.blocks.append( Block.Block( 5, "Leaf Block", constant.LEAF_GREEN, LEAF_BLOCK, x, SURFACE_HEIGHT-50*(tree_height+1), True ) )
    
    for i in range( tree_height-1 ):
        chunk.blocks.append( Block.Block( 5, "Leaf Block", constant.LEAF_GREEN, LEAF_BLOCK, x-50, SURFACE_HEIGHT-50*(i+2), True ) )
        chunk.blocks.append( Block.Block( 5, "Leaf Block", constant.LEAF_GREEN, LEAF_BLOCK, x+50, SURFACE_HEIGHT-50*(i+2), True ) )
    
    double_leave = tree_height//2
    for i in range( double_leave ):
        chunk.blocks.append( Block.Block( 5, "Leaf Block", constant.LEAF_GREEN, LEAF_BLOCK, x-100, SURFACE_HEIGHT-50*(i+2), True ) )
        chunk.blocks.append( Block.Block( 5, "Leaf Block", constant.LEAF_GREEN, LEAF_BLOCK, x+100, SURFACE_HEIGHT-50*(i+2), True ) )
        
        
for xPos in range( WORLD_LIMIT_X[0], WORLD_LIMIT_X[1], 50 ):
    for chunk in CHUNK_LIST:
        if random.randint( 1, 15 ) == 1:
            spawnTree( xPos, chunk )
    

while True:
    mouse_pos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    
    count = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            pygame.quit()
            sys.exit()
            
        ## DRAG AND DROP EVENT         
                    
        if player.hotbar_rect.collidepoint( mouse_pos ) or (player.inventory_rect.collidepoint( mouse_pos ) and player.show_inventory == True):
            
            if player.dragging == False and event.type == pygame.MOUSEBUTTONDOWN: ## DRAGGING
                player.dragging = True
                
                slotIndex = player.findEmptyHotbarSlot( mouse_pos )
                
                if player.hotbar[ slotIndex ] != 0:
                    if event.button == 1: # left click
                        #print("Left Click")
                        player.hotbar[slotIndex]["drag"] = True
                    elif event.button == 3: # right click
                        #print("Right Click")
                        player.hotbar[slotIndex]["drag"] = True
                        player.hotbar[slotIndex]["half"] = True
                        if player.hotbar[slotIndex]["count"] == 1:
                            player.hotbar[slotIndex]["half count"] = 1
                        else:
                            player.hotbar[slotIndex]["half count"] = player.hotbar[slotIndex]["count"]//2
                            
            
        if player.dragging and event.type == pygame.MOUSEBUTTONUP: ## DROPPING
            #print( "drop" )
            player.dragging = False
            
            for i in range( len( player.hotbar ) ):
                if player.hotbar[i] != 0:
                    if player.hotbar[i]["drag"] == True: # We found the block
                        player.hotbar[i]["drag"] = False
                        player.hotbar[i]["half"] = False
                        break
            
            
            #if player.hotbar[i] != 0:
            if player.hotbar_rect.collidepoint( mouse_pos ) or player.inventory_rect.collidepoint( mouse_pos ):
                
                slotIndex = player.findEmptyHotbarSlot( mouse_pos )
                
                if player.hotbar[slotIndex] != 0: # Existing block at position slotIndex
                    if slotIndex != i: #Make sure the id's are different
                        if player.hotbar[slotIndex]["id"] == player.hotbar[i]["id"]: #combine the stack
                            if player.hotbar[i]["half count"] > 0:
                                if player.hotbar[slotIndex]["count"] + player.hotbar[i]["half count"] > 64:
                                    remainder = player.hotbar[i]["half count"] + player.hotbar[slotIndex]["count"] - 64
                                    player.hotbar[slotIndex]["count"] = 64
                                    player.hotbar[i]["count"] += ( remainder - player.hotbar[i]["half count"] )
                                    player.hotbar[i]["half count"] = 0
                                else: # adding blocks to a stack less than full
                                    player.hotbar[slotIndex]["count"] += player.hotbar[i]["half count"]
                                    player.hotbar[i]["count"] -= player.hotbar[i]["half count"]
                                    player.hotbar[i]["half count"] = 0
                            else:
                                if player.hotbar[slotIndex]["count"] + player.hotbar[i]["count"] >= 64:
                                    remainder = player.hotbar[i]["count"] + player.hotbar[slotIndex]["count"] - 64
                                    player.hotbar[slotIndex]["count"] = 64
                                    player.hotbar[i]["count"] = remainder
                                    
                                else:
                                    player.hotbar[slotIndex]["count"] += player.hotbar[i]["count"]
                                    player.hotbar[i] = 0
                        else:
                            target_block = player.hotbar[slotIndex]
                            player.hotbar[slotIndex] = player.hotbar[i] # Move the dragged block to the new position
                            player.hotbar[i] = target_block # Finish swapping the blocks
                else:
                    if player.hotbar[i] != 0:
                        if player.hotbar[i]["half count"] > 0:
                            player.hotbar[slotIndex] = player.hotbar[i].copy() # Drag the block to the new spot
                            
                            player.hotbar[slotIndex]["count"] = player.hotbar[slotIndex]["half count"]
                            player.hotbar[slotIndex]["half count"] = 0
                            
                            player.hotbar[i]["count"] = player.hotbar[i]["count"] - player.hotbar[i]["half count"]
                            player.hotbar[i]["half count"] = 0 # Vacate the old spot
                        else:
                            player.hotbar[slotIndex] = player.hotbar[i] # Drag the block to the new spot
                            player.hotbar[i] = 0 # Vacate the old spot
        
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                if player.show_inventory == False:
                    player.show_inventory = True
                else:
                    player.show_inventory = False
            
            if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                player.broadcastJump( CHUNK_LIST[player.getChunkIndex()] )
            
            
            if event.key == pygame.K_1:
                player.hotbar_index = 0
            if event.key == pygame.K_2:
                player.hotbar_index = 1
            if event.key == pygame.K_3:
                player.hotbar_index = 2
            if event.key == pygame.K_4:
                player.hotbar_index = 3
            if event.key == pygame.K_5:
                player.hotbar_index = 4
            if event.key == pygame.K_6:
                player.hotbar_index = 5
            if event.key == pygame.K_7:
                player.hotbar_index = 6
            if event.key == pygame.K_8:
                player.hotbar_index = 7
                
            
        elif event.type == pygame.MOUSEWHEEL:
            player.hotbar_index -= event.y
            if player.hotbar_index >= player.hotbar_size:
                player.hotbar_index = 0
            if player.hotbar_index <= -1:
                player.hotbar_index = player.hotbar_size-1
        
        
        elif event.type == pygame.MOUSEBUTTONDOWN: ## Moved placing down last to fix the place bug
            if event.button == 3: # right click is replace block
                if player.show_inventory == True and not player.inventory_rect.collidepoint( mouse_pos ) and not player.hotbar_rect.collidepoint( mouse_pos ):
                    player.show_inventory = False
                elif player.show_inventory == True:
                    pass
                else:
                    if player.hotbar[player.hotbar_index] != 0: ## hot bar slot is actually a block
                        if player.hotbar[player.hotbar_index]["count"] > 0:
                            new_block = Block.Block( player.hotbar[player.hotbar_index]["id"], player.hotbar[player.hotbar_index]["name"], player.hotbar[player.hotbar_index]["color"], player.hotbar[player.hotbar_index]["img"], mouse_pos[0]-player.scroll[0], mouse_pos[1]-player.scroll[1] )
                            new_block.adjustPosition()
                            player.updateRect()
                            if player.dragging == False:
                                if not new_block.Rect.colliderect( player.Rect ):
                                    for i in CHUNK_LIST[player.getChunkIndex()].blocks:
                                        if new_block.Rect.colliderect( i.Rect ):
                                            break
                                    else:
                                        CHUNK_LIST[player.getChunkIndex()].addBlock( new_block )
                                        player.hotbar[player.hotbar_index]["count"] -= 1
    
    ## Player movement
    
    if keys[pygame.K_d]:
        player.moveRight( CHUNK_LIST[player.getChunkIndex()] )
    
    if keys[pygame.K_a]:
        player.moveLeft( CHUNK_LIST[player.getChunkIndex()] )
        
    
    # Scrolling:
    player.scrollCheck()
        
    
    ## player gravity
    if player.is_jumping:
        player.jump( CHUNK_LIST[player.getChunkIndex()] )
    else:
        player.fall( CHUNK_LIST[player.getChunkIndex()] )
        
    #print( "Old y: {}; Current Y: {}" .format( player.oldy, player.y ) )
            
    SCREEN.fill( constant.SKY_BLUE )
    
    player.draw( SCREEN )

    ## Log player action
    mouse_press = pygame.mouse.get_pressed()
    if mouse_press[0]: #left click is destroy block
        if not player.hotbar_rect.collidepoint( mouse_pos ) and not player.dragging:
            if player.show_inventory == True and not player.inventory_rect.collidepoint( mouse_pos ) and not player.hotbar_rect.collidepoint( mouse_pos ):
                player.show_inventory = False
            elif player.show_inventory == True:
                    pass
            else:
                ## Change this later so player can only destroy blocks in range
                for chunk in CHUNK_LIST:
                    if player.getCoords()[0] >= chunk.getStart() and player.getCoords()[0] <= chunk.getEnd(): ## Checking to see if player is in a chunk
                        for block in chunk.blocks:
                            if block.Rect.collidepoint( mouse_pos[0]-player.scroll[0], mouse_pos[1]-player.scroll[1] ):
                                player.collectBlockHotBar( block )
                                chunk.blocks.remove( block )
                                            
    
    # 20,200 blocks drawn
    player.checkSetChunk( CHUNK_LIST )
    chunk = CHUNK_LIST[player.getChunkIndex()]
    window["x"][0] = 0 - player.scroll[0] ## window is used to draw and display blocks
    window["x"][1] = SCREEN_WIDTH - player.scroll[0]
    window["y"][0] = 0 - player.scroll[1]
    window["y"][1] = SCREEN_HEIGHT - player.scroll[1]
    
    
    for block in chunk.blocks: #chunk that the player is in
        block.draw( SCREEN, window, player.scroll )
        count += 1
    
    
    ## Player Inventory
    if player.show_inventory:
        inventory = pygame.draw.rect( SCREEN, constant.STEEL_GREY, ( 125, 100, 550, 400 ) )
        
        for row in range( 3 ): ## Inventory
            for column in range( player.hotbar_size ):
                pygame.draw.rect( SCREEN, constant.WHITE, ( 175+50*(column), 350+50*(row), 50, 50 ), 5 )
        
        for i in range(4): ## Armor Slots
            for column in range( player.hotbar_size ):
                pygame.draw.rect( SCREEN, constant.WHITE, ( 175, 125+50*(i), 50, 50 ), 5 )
        
        pygame.draw.rect( SCREEN, constant.WHITE, ( 400, 125+50*(i), 50, 50 ), 5 ) # Off hand
        
        pygame.draw.rect( SCREEN, constant.BLACK, ( 225+15, 125, 150, 200 ) ) # Player Image
        
        ## Draw player crafting table
        for i in range( 0, 2 ):
            pygame.draw.rect( SCREEN, constant.WHITE, ( 150+50*(6+i), 160, 50, 50 ), 5 )
        
        for i in range( 3, 5 ):
            pygame.draw.rect( SCREEN, constant.WHITE, ( 150+50*(6+i-3), 210, 50, 50 ), 5 )
            
        # Crafting arrow
        SCREEN.blit( ARROW, ( 560, 190 ) )
        
        pygame.draw.rect( SCREEN, constant.WHITE, ( 610, 185, 50, 50 ), 5 )
        
    
    ## Player Hotbar
    hotbar = pygame.draw.rect( SCREEN, constant.BLACK, ( 175, 530, 450, 50 ) )
    
    for i in range( player.hotbar_size ):
        pygame.draw.rect( SCREEN, constant.STEEL_GREY, ( 175+50*(i), 530, 50, 50 ), 5 )
    
    
    # Draw Highlighted Cube
    pygame.draw.rect( SCREEN, constant.WHITE, ( 175+50*( player.hotbar_index ), 530, 50, 50 ), 5 )
    
    player.drawInventory( SCREEN, mouse_pos )
    
    
    pygame.display.update()
    clock.tick( 60 )