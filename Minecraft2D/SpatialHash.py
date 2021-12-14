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
    