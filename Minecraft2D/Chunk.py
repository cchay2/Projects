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
    
    
        