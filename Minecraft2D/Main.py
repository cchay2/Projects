import pygame, sys, random
import Constant as constant
import Player
import Block
import Chunk
import Skin
import time

# normal
# * Important
# ? hmm
# ! Uh Oh
# todo: Fix
# // Ded

pygame.init()

pygame.display.set_caption('Minecraft 2D')

item_count_font = pygame.font.SysFont( "Comic Sans MS", 15 )

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

SURFACE_HEIGHT = SCREEN_HEIGHT//2 ## Should be 300

WORLD_LIMIT_X = ( -100000, 100000 ) # Each block is 50x50, and for 2000 blocks left and right
WORLD_LIMIT_Y = ( SURFACE_HEIGHT, SURFACE_HEIGHT + 50*50 ) # 50 blocks down

SCREEN = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )

GRASS_TILE = pygame.image.load( "graphics/tiles/grass.png" )
DIRT_TILE = pygame.image.load( "graphics/tiles/dirt.png" )
STONE_TILE = pygame.image.load( "graphics/tiles/stone.png" )
WOOD_TILE = pygame.image.load( "graphics/tiles/oak-log.png" )
LEAF_TILE = pygame.image.load( "graphics/tiles/oak-leaf.png" )

GRASS_BLOCK = pygame.image.load( "graphics/blocks/grass.png" ).convert_alpha()
DIRT_BLOCK = pygame.image.load( "graphics/blocks/dirt.png" ).convert_alpha()
STONE_BLOCK = pygame.image.load( "graphics/blocks/stone.png" ).convert_alpha()
WOOD_BLOCK = pygame.image.load( "graphics/blocks/oak-log.png" ).convert_alpha()
LEAF_BLOCK = pygame.image.load( "graphics/blocks/leaves.png" ).convert_alpha()

ARROW = pygame.image.load( "graphics/other/crafting_arrow.png" ).convert_alpha()

head_right = pygame.transform.scale( pygame.image.load( "graphics/player/head_right.png" ), (30, 30) )
head_left = pygame.transform.scale( pygame.image.load( "graphics/player/head_left.png" ), (30, 30) )
body = pygame.transform.scale( pygame.image.load( "graphics/player/body.png" ), (16, 35) )
top_arm = pygame.transform.scale( pygame.image.load( "graphics/player/top_arm.png" ), (16, 35) )
bot_arm = pygame.transform.scale( pygame.image.load( "graphics/player/bot_arm.png" ), (16, 35) )
top_leg = pygame.transform.scale( pygame.image.load( "graphics/player/top_leg.png" ), (16, 40) )
bot_leg = pygame.transform.scale( pygame.image.load( "graphics/player/bot_leg.png" ), (16, 40) )



default_skin_dict = {
    "head_left" : { "img": head_left, 
                   "rect":  head_left.get_rect()},
    "head_right": { "img": head_right, 
                   "rect":  head_right.get_rect()},
    "body": { "img": body, 
            "rect":  body.get_rect()},
    "top_arm": { "img": top_arm, 
                "rect":  top_arm.get_rect()},
    "bot_arm": { "img": bot_arm, 
                "rect":  bot_arm.get_rect()},
    "top_leg": { "img": top_leg, 
                "rect":  top_leg.get_rect()},
    "bot_leg": { "img": bot_leg, 
                "rect":  bot_leg.get_rect()}
}
default_skin = Skin.Skin( default_skin_dict )

window = {
    "x": [ 0, SCREEN_WIDTH ],
    "y": [ 0, SCREEN_HEIGHT ]
}

BLOCK_LIST = []
CHUNK_LIST = []
CHUNK_SIZE = 10000 #10,000 in actuality it is 10,100? or 2000*50 or 100,000 blocks per chunk

    

## Generate the chunks
for chunk_width in range( WORLD_LIMIT_X[0], WORLD_LIMIT_X[1]-CHUNK_SIZE//2, CHUNK_SIZE//2 ): #Chunk Size = 10,000
    CHUNK_LIST.append( Chunk.Chunk( chunk_width, chunk_width+CHUNK_SIZE//2 ) )

## Generate all blocks
for yPos in range( WORLD_LIMIT_Y[0], WORLD_LIMIT_Y[1], 50  ):
    for xPos in range( WORLD_LIMIT_X[0], WORLD_LIMIT_X[1], 50 ):
        for chunk in CHUNK_LIST: # add blocks to the chunk
            if xPos >= chunk.getStart() and xPos < chunk.getEnd():
                if yPos >= SURFACE_HEIGHT and yPos < SURFACE_HEIGHT + 50:
                    chunk.blocks.append( Block.Block( 1, "Grass Block", constant.GRASS_GREEN, GRASS_BLOCK, GRASS_TILE, xPos, yPos ) )
                elif yPos >= SURFACE_HEIGHT+50 and yPos < SURFACE_HEIGHT + 50*4:
                    chunk.blocks.append( Block.Block( 2, "Dirt Block", constant.DIRT_BROWN, DIRT_BLOCK, DIRT_TILE, xPos, yPos ) )
                else:
                    chunk.blocks.append( Block.Block( 3, "Stone Block", constant.STONE_GREY, STONE_BLOCK, STONE_TILE, xPos, yPos ) )


floating_blocks = []   

clock = pygame.time.Clock()

player = Player.Player( SCREEN_WIDTH//2, SCREEN_HEIGHT//2-100 )
player.setSkin( default_skin )
place_cd = False


## Set Player Chunk
player.checkSetChunk( CHUNK_LIST )


def spawnTree( x, chunk ):
    tree_rect = pygame.Rect( x-100, SURFACE_HEIGHT-50, 250, 100 )
    
    if player.Rect.colliderect( tree_rect ):
        pass
    else:
        tree_height = random.randint( 3, 5 )
        for i in range( tree_height ):
            chunk.blocks.append( Block.Block( 4, "Wood Block", constant.WOOD_BROWN, WOOD_BLOCK, WOOD_TILE, x, SURFACE_HEIGHT-50*(i+1) ) )
        
        chunk.blocks.append( Block.Block( 5, "Leaf Block", constant.LEAF_GREEN, LEAF_BLOCK, LEAF_TILE, x, SURFACE_HEIGHT-50*(tree_height+1), True ) )
        
        for i in range( tree_height-1 ):
            chunk.blocks.append( Block.Block( 5, "Leaf Block", constant.LEAF_GREEN, LEAF_BLOCK, LEAF_TILE, x-50, SURFACE_HEIGHT-50*(i+2), True ) )
            chunk.blocks.append( Block.Block( 5, "Leaf Block", constant.LEAF_GREEN, LEAF_BLOCK, LEAF_TILE, x+50, SURFACE_HEIGHT-50*(i+2), True ) )
            chunk.blocks.append( Block.Block( 5, "Leaf Block", constant.LEAF_GREEN, LEAF_BLOCK, LEAF_TILE, x, SURFACE_HEIGHT-50*(i+2), True ) )
        
        double_leave = tree_height//2
        for i in range( double_leave ):
            chunk.blocks.append( Block.Block( 5, "Leaf Block", constant.LEAF_GREEN, LEAF_BLOCK, LEAF_TILE, x-100, SURFACE_HEIGHT-50*(i+2), True ) )
            chunk.blocks.append( Block.Block( 5, "Leaf Block", constant.LEAF_GREEN, LEAF_BLOCK, LEAF_TILE, x+100, SURFACE_HEIGHT-50*(i+2), True ) )
            chunk.blocks.append( Block.Block( 5, "Leaf Block", constant.LEAF_GREEN, LEAF_BLOCK, LEAF_TILE, x, SURFACE_HEIGHT-50*(i+2), True ) )
        
        
for chunk in CHUNK_LIST:
    for x in range( chunk.getStart(), chunk.getEnd(), 50 ):
        if random.randint( 1, 10 ) == 1:
            spawnTree( x, chunk )
    

while True:
    player.is_walking = False
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
                if event.button in (1, 3): ## Prevent Further Bugs created with scrolling by checking for left or right click
                    player.dragging = True
                    
                    slotIndex = player.findEmptyHotbarSlot( mouse_pos )
                    if slotIndex != -1: ## Handle False being thrown when player clcks on non-clickable 
                        if player.hotbar[ slotIndex ] != 0:
                            if event.button == 1: # left click  
                                #print("Click Index:", slotIndex)
                                player.hotbar[slotIndex]["drag"] = True
                            elif event.button == 3: # right click
                                #print("Click Index:", slotIndex)
                                player.hotbar[slotIndex]["drag"] = True
                                player.hotbar[slotIndex]["half"] = True
                                
                                
                                if player.hotbar[slotIndex]["count"] == 1:
                                    player.hotbar[slotIndex]["half count"] = 1
                                else:
                                    player.hotbar[slotIndex]["half count"] = player.hotbar[slotIndex]["count"]//2
                                
                            if slotIndex == 40 and player.hotbar[40] != 0: #player clicks on item in crafting bar
                                if event.button in (1, 3):
                                    player.crafting = True
                                    player.craftBlock()
                                    if player.hotbar[slotIndex]["half"] == True:
                                        player.hotbar[slotIndex]["half"] = False
                                        player.hotbar[slotIndex]["half count"] = 0
                                        
                            
                            
            
        if player.dragging and event.type == pygame.MOUSEBUTTONUP: ## DROPPING
            
            player.addToInventory( mouse_pos, player.hotbar )
            
            player.craft()

        
        
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
            if event.key == pygame.K_9:
                player.hotbar_index = 8
                
            
        elif event.type == pygame.MOUSEWHEEL:
            player.hotbar_index -= event.y
            if player.hotbar_index >= player.hotbar_size:
                player.hotbar_index = 0
            if player.hotbar_index <= -1:
                player.hotbar_index = player.hotbar_size-1
            
            #print( "mouse scroll" )
        
        
        elif event.type == pygame.MOUSEBUTTONDOWN: ## Moved placing down last to fix the place bug
            if event.button == 3: # right click is replace block
                player.place_block = True
                player.placeBlockAnimation()
                if player.show_inventory == True and not player.inventory_rect.collidepoint( mouse_pos ) and not player.hotbar_rect.collidepoint( mouse_pos ):
                    player.show_inventory = False
                elif player.show_inventory == True:
                    pass
                else:
                    if player.hotbar[player.hotbar_index] != 0: ## hot bar slot is actually a block
                        if player.hotbar[player.hotbar_index]["count"] > 0:
                            new_block = Block.Block( player.hotbar[player.hotbar_index]["id"], player.hotbar[player.hotbar_index]["name"], player.hotbar[player.hotbar_index]["color"], player.hotbar[player.hotbar_index]["img"], player.hotbar[player.hotbar_index]["tile"], mouse_pos[0]-player.scroll[0], mouse_pos[1]-player.scroll[1] )
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
                                        
            if event.button == 1:
                player.attack = True
                player.holding = True
                
        
        if event.type == pygame.MOUSEBUTTONUP:
            player.holding = False
            player.breaking = False
    
    
    #print( player.holding )
    
    ## Player movement
    
    if keys[pygame.K_d]:
        player.moveRight( CHUNK_LIST[player.getChunkIndex()] )
        #player.direction = "right"
        player.is_walking = True
    
    if keys[pygame.K_a]:
        player.moveLeft( CHUNK_LIST[player.getChunkIndex()] )
        #player.direction = "left"
        player.is_walking = True
        
    
    # Scrolling:
    player.scrollCheck()
        
    
    ## player gravity
    if player.is_jumping:
        player.jump( CHUNK_LIST[player.getChunkIndex()] )
    else:
        player.fall( CHUNK_LIST[player.getChunkIndex()] )
        
    #print( "Old y: {}; Current Y: {}" .format( player.oldy, player.y ) )
            
    SCREEN.fill( constant.SKY_BLUE )
    
    player.draw( SCREEN, mouse_pos )

    ## Log player action
    mouse_press = pygame.mouse.get_pressed()
    if player.holding and player.attack == False: #left click is destroy block
        #player.place_block = True
        #player.placeBlockAnimation()
        if not player.hotbar_rect.collidepoint( mouse_pos ) and not player.dragging:
            if player.show_inventory == True and not player.inventory_rect.collidepoint( mouse_pos ) and not player.hotbar_rect.collidepoint( mouse_pos ):
                player.show_inventory = False
            elif player.show_inventory == True:
                    pass
            else:
                ## Change this later so player can only destroy blocks in range
                for chunk in CHUNK_LIST:
                    if player.getCoords()[0] >= chunk.getStart() and player.getCoords()[0] <= chunk.getEnd(): ## Checking to see if player is in a chunk
                        for index in range( len(chunk.blocks)-1 , 0, -1):
                            block = chunk.blocks[index]
                            if block.Rect.collidepoint( mouse_pos[0]-player.scroll[0], mouse_pos[1]-player.scroll[1] ):
                                if player.holding == True:
                                    player.breaking = True
                                    #player.collectBlockHotBar( block ) #TODO: Change this later
                                    chunk.blocks.remove( block )
                                    floating_blocks.append( 
                                                           Block.FBlock( block.getID(), block.getName(), block.getColor(), block.getImage(), block.getTile(), block.x, block.y )
                                                           )
                                    print( block.y )
                                            
    
    # 20,200 blocks drawn
    player.checkSetChunk( CHUNK_LIST )
    chunk = CHUNK_LIST[player.getChunkIndex()]
    window["x"][0] = 0 - player.scroll[0] ## window is used to draw and display blocks
    window["x"][1] = SCREEN_WIDTH - player.scroll[0]
    window["y"][0] = 0 - player.scroll[1]
    window["y"][1] = SCREEN_HEIGHT - player.scroll[1]
    
    
    for block in chunk.blocks: #chunk that the player is in
        block.draw( SCREEN, window, player.scroll )
        #count += 1
        
    for fblock in floating_blocks[:]:
        fblock.animate( SCREEN, CHUNK_LIST[player.chunk_index], (player.x, player.y), window, player.scroll )
        if fblock.collected:
            print( fblock.getName() )
            player.collectBlockHotBar( Block.Block( fblock.getID(), fblock.getName(), fblock.getColor(), fblock.getImage(), fblock.getTile(), fblock.x, fblock.y ) )
            floating_blocks.remove( fblock )
    
    #print( floating_blocks )
    
    #print(  player.x - CHUNK_LIST[player.getChunkIndex()-1].getStart() )
    if player.x - chunk.getStart() <= 600: #Chunk Before the current Chunk player is in | range of 9 blocks
        for block in CHUNK_LIST[ player.getChunkIndex()-1 ].blocks: #chunk that the player is in
            block.draw( SCREEN, window, player.scroll )
    elif chunk.getEnd() - player.x <= 600: #Chunk Before the current Chunk player is in | range of 9 blocks
        for block in CHUNK_LIST[ player.getChunkIndex()+1 ].blocks: #chunk that the player is in
            block.draw( SCREEN, window, player.scroll )
    
    
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
    
    #player.drawInventory( SCREEN, mouse_pos )
    
    # Draw Hotbar
    player.drawInventory( SCREEN, 1, 9, 0, 180, 535, mouse_pos, player.hotbar )
    
    # Draw Inventory
    if player.show_inventory == True:
        player.drawInventory( SCREEN, 3, 9, 9, 180, 355, mouse_pos, player.hotbar )
    # Draw 2x2 Crafting table
        player.drawInventory( SCREEN, 2, 2, 36, 455, 165, mouse_pos, player.hotbar )
        player.drawInventory( SCREEN, 1, 1, 40, 615, 190, mouse_pos, player.hotbar )
        
        #print( player.hotbar[ 40 ] )
        
    
    pygame.display.update()
    clock.tick( 60 )
    #time.sleep(0.5)