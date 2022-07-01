from RelationalSudoku import RelationalSudoku

class Kropki(RelationalSudoku):
    def __init__(self, dimension=9):
        self.initialize_sudoku(dimension)
    
    ##### RELATION FUNCTIONS #######################################

    # A symbol between two cells represents a relation (function) between the cells
    def map_symbol_to_function(self, symbol):
        if symbol == "B":
            return self.black_dot
        elif symbol == "W":
            return self.white_dot
        elif symbol == ".":
            return self.blank_relation

    # A symbol between a cell on the left and right (or up and down)
    # may have opposite relations when going right to left (down to up)
    def invert_symbol(self, symbol):
        # In Kropki, each symbol is its own inverse
        return symbol

    # Black dot indicates a factor of 2 relation
    def black_dot(self, coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2

        if self.solved[y1,x1]:
            return

        values1 = self.possible[y1,x1]
        values2 = self.possible[y2,x2]

        if self.solved[y2,x2]:
            values2 = set()
            values2.add( self.grid[y2,x2] )

        remaining = set()
        # Everything in values1 must be a factor of two of something in values2
        for val in values2:
            remaining |= self.factor_two( val )
        # Of the factors of 2 of the values in values2,
        # only the results already present in values1 can work
        remaining &= values1

        return remaining
    
    def white_dot(self, coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        
        if self.solved[y1,x1]:
            return

        values1 = self.possible[y1,x1]
        values2 = self.possible[y2,x2]

        if self.solved[y2,x2]:
            values2 = set()
            values2.add( self.grid[y2,x2] )

        remaining = set()
        # Everything in values1 must be one off of something in values2
        for val in values2:
            remaining |= self.difference_one( val )
        # Of the factors of 2 of the values in values2,
        # only the results already present in values1 can work
        remaining &= values1

        return remaining
    
    def blank_relation(self, coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        
        if self.solved[y1,x1]:
            return

        values1 = self.possible[y1,x1]
        values2 = self.possible[y2,x2]

        if self.solved[y2,x2]:
            values2 = set()
            values2.add( self.grid[y2,x2] )

        remaining = set()
        # The final result in values1 can neither be off by one nor a factor of two
        # different from the final result in values2
        for val in values2:
            seed = set([val])       # For each value we look at, that value could not be included
            seed |= self.difference_one( val )
            seed |= self.factor_two( val )
            # Only values that don't satisfy either of the above are possible
            remaining |= self.values - seed
    
        remaining &= values1

        return remaining

    def factor_two(self, value):
        results = set( [ value*2, value/2 ] )
        final = set()
        for num in results:
            if ( num == int(num) ) and ( num >= min(self.values) ) and ( num <= max(self.values) ):
                final.add( int(num) )
        return final
    
    def difference_one(self, value):
        results = set( [ int(value - 1), int(value + 1) ] )
        final = set()
        for num in results:
            if isinstance(num, int) and num >= min(self.values) and num <= max(self.values):
                final.add(num)
        return final