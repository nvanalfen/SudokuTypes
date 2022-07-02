from AbstractSudoku import AbstractSudoku
import numpy as np
import pandas as pd
from copy import deepcopy

class RelationalSudoku(AbstractSudoku):
    def __init__(self, dimension=9):
        self.initialize_sudoku(dimension)

    # In addition to parent class functions, add relations
    def initialize_sudoku(self, dimension):
        super().initialize_sudoku(dimension)
        self.relations = []
    
    def read_relations_from_csv(self, f_name):
        # Does not need to have the full (2*dim-1, dim) size
        # Will read up to as many relations as there are
        symbols = np.array( pd.read_csv( f_name, header=None, index_col=None, keep_default_na=False ) )
        return symbols
    
    # A symbol between two cells represents a relation (function) between the cells
    def map_symbol_to_function(self, symbol):
        return lambda : print("Abstract Method")

    # A symbol between a cell on the left and right (or up and down)
    # may have opposite relations when going right to left (down to up)
    def invert_symbol(self, symbol):
        return symbol

    # The relation grid is of shape ( 2*dim-1, dim )
    # Even rows (including 0) can have up to dim-1 elements and represent relations between left and right
    # Odd rows can have dim elements and represent relations between up and down
    def load_relations(self, relation_grid):
        self.relations = []

        rows, columns = relation_grid.shape
        for j in range(rows):
            for i in range(columns):
                symbol = relation_grid[j,i].strip()
                if symbol == '':
                    continue

                if j % 2 == 0:
                    # Even rows indicates and left -> right relation
                    x1 = i
                    y1 = int( j/2 )
                    x2 = i + 1
                    y2 = int( j/2 )
                else:
                    x1 = i
                    y1 = int( j/2 )
                    x2 = i
                    y2 = int( j/2 ) + 1
                
                # Set the relations both ways
                self.relations.append( [ (x1, y1), self.map_symbol_to_function(symbol), (x2, y2) ] )
                self.relations.append( [ (x2, y2), self.map_symbol_to_function( self.invert_symbol(symbol) ), (x1, y1) ] )

    # The specific relation functions will be tailored to the implemented classes
    # They will all take the two sets of possible values for coord1 and coord2
    # And will return the subset of coord1 that remains possible after applying the relation
    # Remove the complement of coord1's before and after from the possibilities of coord1
    def apply_relations(self):
        for coord1, func, coord2 in self.relations:
            x, y = coord1

            if self.solved[y,x]:
                continue

            prior = self.possible[y,x]
            remainder = func( coord1, coord2 )

            for value in prior - remainder:
                self.remove_possibility( coord1, value )

    def basic_loop(self):
        self.apply_group_functions()
        self.apply_relations()
    