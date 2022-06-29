import numpy as np
import pandas as pd
import itertools

class AbstractSudoku:
    def __init__(self, dimension=9):
        self.dim = dimension
        self.values = [ i+1 for i in range(self.dim) ]
        
        # Grids for the puzzle itself
        self.grid = np.zeros( (self.dim, self.dim) )
        self.solved = np.zeros( (self.dim, self.dim) ).astype(bool)
        self.possible = np.repeat( None, self.dim*self.dim ).reshape( (self.dim, self.dim) )
        self.set_possibilities()
        
        # Groups for things like rows, columns, subgrids, etc
        self.groups = {}
        self.set_groups()
        
    ##### SETUP FUNCTIONS ######################################
        
    def set_possibilities(self):
        for i in range(self.dim):
            for j in range(self.dim):
                self.possible[j,i] = set( self.values )
        
    # Make groups for simplicity when applying the various rules of sudoku
    # e.g. each number in self. values can only appear once in a group
    def set_groups(self):
        
        # Create the row groups
        self.groups["row"] = []
        for i in range(self.dim):
            group = {}
            group["coords"] = set( [ (x,i) for x in range(self.dim) ] )
            group["functions"] = [ self.N_of_N_counts, self.N_of_N_possibilities ]
            group["properties"] = {}
            
            self.groups["row"].append( group )
        
        self.groups["column"] = []
        for i in range(self.dim):
            group = {}
            group["coords"] = set( [ (i,y) for y in range(self.dim) ] )
            group["functions"] = [ self.N_of_N_counts, self.N_of_N_possibilities ]
            group["properties"] = {}
            
            self.groups["column"].append( group )
        
    ##### SOLVE FUNCTIONS ######################################
        
    def solve_cell(self, coord, value):
        x,y = coord
        
        # Set the value in the proper place and let solved show that
        self.grid[y,x] = value
        self.solved[y,x] = True
        self.possible[y,x] = set()
        
        # Remove value from the possibilities of all other cells in a group containing
        # the cell being set
        for key in self.groups:
            groups = self.groups[key]
            for group in groups:
                if not coord in group["coords"]:
                    continue
                
                # Remove value from all unsolved cells
                for coord2 in group["coords"]:
                    self.remove_possibility( coord2, value )
    
    def remove_possibility(self, coord, value):
        x, y = coord
        if not self.solved[y, x] and value in self.possible[y, x]:
            # Only remove if the cell isn't already solved and if the value
            # can be removed
            self.possible[y, x].remove(value)
        if len(self.possible[y, x]) == 1:
            # Solve cells with only one possibility remaining
            self.solve_cell( coord, self.possible[y, x].pop() )
    
    def N_of_N_counts(self, group):
        unsolved = self.solved_in_group( group )
        coord_sets, frequencies = self.get_frequencies( group )

        for freq in frequencies:
            if freq >= ( len(group["coords"]) - unsolved ):
                continue

            for values in itertools.combinations( frequencies[freq], freq ):
                primary = values[0]
                seed = coord_sets[primary]
                matching = True

                for secondary in values[1:]:
                    remaining = coord_sets[secondary]
                    matching = matching and ( seed == remaining )

                if matching:
                    # Remove other possibilities from these cells
                    for coord in seed:
                        x,y = coord
                        # Remove the other possibilities one by one
                        # do it this way to trigger the "if only one remains" possibility of remove_possibility
                        outcast = self.possible[y,x] - set(values)
                        for val in outcast:
                            self.remove_possibility( coord, val )

                    # Remove these possibilities from other coords
                    for coord in group["coords"]:
                        if not coord in seed:
                            for val in values:
                                self.remove_possibility( coord, val )

        
    def N_of_N_possibilities(self, group):
        pass
    
    ##### AUXILIARY FUNCTIONS ##################################
    
    # Given a group and value, return the set of all coordinates in group
    # containing that value as a possibility
    def get_possibility_coords(self, group, value):
        all_coords = set()
        
        for coord in group["coords"]:
            x,y = coord
            if ( not self.solved[y,x] ) and  ( value in self.possible[y,x] ):
                all_coords.add( coord )
        
        return all_coords

    def solved_in_group(self, group):
        total = 0
        for x,y in group["coords"]:
            total += int( self.solved[y,x] )
    
        return total

    # Given a group, return how often and where each possibility occurs
    # Params:
    #   group               -> Group of cells
    # Returns:
    #   coord_sets          -> dict from value to coords that have that value in its possibilities
    #   frequencies         -> dict from frequency (len of coord set for that value) to list of all values with that frequency
    def get_frequencies(self, group):
        coord_sets = {}
        frequencies = {}
        for i in self.values:
            possibilities = self.get_possibility_coords( group, i )
            coord_sets[i] = possibilities

            if not len(possibilities) in frequencies:
                frequencies[ len(possibilities) ] = []
            
            frequencies[ len(possibilities) ].append( i )
        
        return coord_sets, frequencies