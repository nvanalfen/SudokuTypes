from .RelationalSudoku import RelationalSudoku

class Futoshiki(RelationalSudoku):
    def __init__(self, dimension=9):
        self.initialize_sudoku(dimension)
    
    ##### RELATION FUNCTIONS #######################################

    # A symbol between two cells represents a relation (function) between the cells
    def map_symbol_to_function(self, symbol):
        if symbol == ">":
            return self.greater_than
        elif symbol == "<":
            return self.less_than

    # A symbol between a cell on the left and right (or up and down)
    # may have opposite relations when going right to left (down to up)
    def invert_symbol(self, symbol):
        if symbol == ">":
            return "<"
        elif symbol == "<":
            return ">"

    def greater_than(self, coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        values1 = self.possible[y1,x1]
        values2 = self.possible[y2,x2]

        remaining = set( [ el for el in values1 if el > min(values2) ] )
        return remaining
    
    def less_than(self, coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        values1 = self.possible[y1,x1]
        values2 = self.possible[y2,x2]

        remaining = set( [ el for el in values1 if el < max(values2) ] )
        return remaining