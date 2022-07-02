from Sudoku import Sudoku
import numpy as np
import pandas as pd

class KenKen(Sudoku):
    def __init__(self, dimension=6, setup_groups=True, subgrid_shape=None):
        super().__init__(dimension, setup_groups=False, subgrid_shape=subgrid_shape)
        self.blobs = {}
        self.initialize_sudoku(dimension, setup_groups=setup_groups, subgrid_shape=subgrid_shape)
    
    def initialize_sudoku(self, dimension=6, setup_groups=True, subgrid_shape=(2,3)):
        super().initialize_sudoku(dimension, setup_groups=False, subgrid_shape=subgrid_shape)

        if setup_groups:
            self.set_groups()
    
    def set_groups(self):
        super().set_groups()

        self.load_blobs()

    def load_blobs(self, blobs=None):
        if not blobs is None:
            self.blobs = blobs

        self.groups["arithmetic"] = np.repeat( None, len(self.blobs) )
        ind = 0
        for key in self.blobs:
            self.groups["arithmetic"][ind] = self.blobs[key]
            self.groups["arithmetic"][ind]["functions"] = []
            ind += 1

    def read_blobs_from_csv(self, f_name):
        blobs = np.array( pd.read_csv( f_name, header=None, index_col=None ) )
        for row in range(len(blobs)):
            for col in range(len(blobs[row])):
                element = [el.strip() for el in blobs[row,col].split(":") ]
                if len( element ) == 3:
                    key, val, operation = element
                elif len( element ) == 2:
                    key, val = element
                    val = int(val)
                    operation = None
                else:
                    key = element[0]
                    val = None
                    operation = None

                if not key in self.blobs:
                    self.blobs[key] = {}
                    self.blobs[key]["coords"] = []
                    self.blobs[key]["functions"] = []
                    self.blobs[key]["properties"] = {}
                
                self.blobs[key]["coords"].append( (col, row) )
                if not val is None:
                    self.blobs[key]["properties"]["total"] = val
                if not operation is None:
                    self.blobs[key]["properties"]["operation"] = self.map_symbol_to_operation(operation)
    
    def get_permutations(self, group, ind, current, all_results):
        if ind >= len( group["coords"] ):
            all_results.append( current )
            return
        
        x,y = list( group["coords"] )[ind]
        possible = self.possible[y,x]

        # If a cell is already solved, make sure that value is taken into account
        if self.solved[y,x]:
            possible = set( [ self.grid[y,x] ] )

        for val in possible:
            self.get_permutations( group, ind+1, current+[val], all_results )

    def add_all(self, values):
        if len(values) == 0:
            return None
        
        total = values[0]
        for val in values[1:]:
            total += val
        
        return total

    def subtract_all(self, values):
        if len(values) == 0:
            return None
        
        total = values[0]
        for val in values[1:]:
            total -= val
        
        return total

    def multiply_all(self, values):
        if len(values) == 0:
            return None
        
        total = values[0]
        for val in values[1:]:
            total *= val
        
        return total

    def divide_all(self, values):
        if len(values) == 0:
            return None
        
        total = values[0]
        for val in values[1:]:
            total /= val
        
        return total

    # For all possible permutations of possibilities in a group, return only those
    # That are possible with the total and arithmetic operation needed
    def cull_combos(self, group):
        operation = group["properties"]["operation"]
        total = group["properties"]["total"]

        combos = []
        possible_combos = []
        self.get_permutations( group, 0, [], possible_combos )
        for combo in possible_combos:
            value = operation( combo )
            if value == total and len( set(combo) ) == len(combo):
                combos.append( combo )
        
        return combos

    def map_symbol_to_operation(self, symbol):
        if symbol == "+":
            return self.add_all
        elif symbol == "-":
            return self.subtract_all
        elif symbol == "*" or symbol.lower() == "x":
            return self.multiply_all
        elif symbol == "/":
            return self.divide_all
