import numpy as np
import pandas as pd
import itertools
from copy import deepcopy

class AbstractSudoku:
    def __init__(self, dimension=9, subgrid_shape=None):
        self.initialize_sudoku(dimension)
        
    ##### SETUP FUNCTIONS ######################################
        
    def initialize_sudoku(self, dimension, setup_groups=True, subgrid_shape=None):
        self.dim = dimension
        self.values = set([ i+1 for i in range(self.dim) ])
        
        # Grids for the puzzle itself
        self.grid = np.zeros( (self.dim, self.dim) ).astype(int)
        self.solved = np.zeros( (self.dim, self.dim) ).astype(bool)
        self.possible = np.repeat( None, self.dim*self.dim ).reshape( (self.dim, self.dim) )
        self.set_possibilities()
        
        # Groups for things like rows, columns, subgrids, etc
        self.groups = {}

        if setup_groups:
            self.set_groups()

    def set_possibilities(self):
        for i in range(self.dim):
            for j in range(self.dim):
                self.possible[j,i] = set( self.values )
        
    # Make groups for simplicity when applying the various rules of sudoku
    # e.g. each number in self. values can only appear once in a group
    def set_groups(self):
        
        # Create the row groups
        self.groups["row"] = np.repeat(None, self.dim)
        for i in range(self.dim):
            group = {}
            group["coords"] = set( [ (x,i) for x in range(self.dim) ] )
            group["functions"] = [ self.N_of_N_counts, self.N_of_N_possibilities ]
            group["properties"] = {}
            
            self.groups["row"][i] = group
        
        self.groups["column"] = np.repeat(None, self.dim)
        for i in range(self.dim):
            group = {}
            group["coords"] = set( [ (i,y) for y in range(self.dim) ] )
            group["functions"] = [ self.N_of_N_counts, self.N_of_N_possibilities ]
            group["properties"] = {}
            
            self.groups["column"][i] = group

    # Load grid with pre-solved cells
    # This function does not read a grid from a file, but turns a read grid into a puzzle
    def load_grid(self, grid):
        self.initialize_sudoku( len(grid) )

        for i in range(self.dim):
            for j in range(self.dim):
                if grid[j,i] in self.values:
                    self.solve_cell( (i,j), grid[j,i] )
    
    # Reads a CSV sudoku puzzle where blank spots are 0
    # Reads it and turns it into a numerical grid
    def read_grid_from_csv(self, f_name):
        grid = np.array( pd.read_csv( f_name, header=None, index_col=None ) )
        return grid

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
            groups = self.groups[key].flatten()
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
    
    # Given a group, if N values appear only in the same N sets as possibilities,
    # Remove other values from those possibilities
    # Params:
    #   group               -> Group of cells
    # Returns:
    #   None                -> This function alters the cells in the group
    def N_of_N_counts(self, group):
        unsolved = len(group["coords"]) - self.solved_in_group( group )
        coord_sets, frequencies = self.get_frequencies( group )

        for freq in frequencies:
            if freq >= unsolved or freq == 0:
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

    # Similar to N_of_N_counts, but distinct
    # If N of the cells in the group only have the same N possibilities,
    # Remove those possibilities from other cells
    # Different from N_of_N_counts because the possibilities in these cells may appear elsewhere in the group
    # e.g. if two cells only have set([1,2]) as possibilities, but 1 appears in all other cells and 2 appears in three more,
    # they have different frequencies and will not be handled by N_of_N_counts but will be handled here
    # Params:
    #   group               -> Group of cells
    # Returns:
    #   None                -> This function alters the cells in the group
    def N_of_N_possibilities(self, group):
        
        unsolved = len(group) - self.solved_in_group(group)

        # make a dict linking each coord with each set of possibilities
        coord_possibilities = { coord : self.possible[ coord[1], coord[0] ] for coord in group["coords"] }

        # Now link each distinct set of possibilities to the coords that hold them
        distinct_possibilities = {}
        for coord in coord_possibilities:
            possible_values = tuple( coord_possibilities[coord] )
            if not possible_values in distinct_possibilities:
                distinct_possibilities[possible_values] = []
            distinct_possibilities[possible_values].append( coord )

        # Now loop through distinct possibilities and if any set of possibilities has the same length
        # as the number of coords it maps to, and that number is less than the total remaining unsolved cells,
        # eliminate those possibilities from other cells in the group
        for values in distinct_possibilities:
            if ( len(values) == len( distinct_possibilities[values] ) ) and ( len(values) < unsolved ):
                self.remove_from_complement( group, distinct_possibilities[values], values )
    
    def apply_group_functions(self):
        for group_type in self.groups:
            for group in self.groups[group_type].flatten():
                for func in group["functions"]:
                    func(group)

    # If a value appears N times (1-3 in this case) in group1 (row, column, subgrid) as possibilities,
    # and all N of those occurances also exist in group2, remove all other
    # instances of these values grom group2 (other than those also in group1)
    # e.g. if 2 appears three times in a subgrid, and all three of those exist in row 2,
    # then remove all other instances of 2 from row2 (force the row)
    def force_group(self, group, group_type):
        # Get the set of coordinates where each value exists as a possibility
        possible_coords = { value : self.get_possibility_coords(group, value) for value in self.values }

        for other_group_type in self.groups:
            if other_group_type == group_type:
                continue

            for group2 in self.groups[other_group_type]:
                # For each other group, get the set of coordinates where each value exists as a possibility
                possible_coords2 = { value : self.get_possibility_coords(group2, value) for value in self.values }

                # For each value, if the coords in group1 are a subset of those in group2, remove the complement from group2
                for val in possible_coords:
                    coords1 = possible_coords[val]
                    coords2 = possible_coords2[val]

                    if coords1 == coords1 & coords2:
                        self.remove_from_complement(group2, coords1, [val])


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

    # Remove values from all coords in group not included in coords
    # Params:
    #   group                       -> Group of cells
    #   coords                      -> Coordinated that will keep the given values
    #   values                      -> Values to be removed from all coordinates in group not included in coords
    # Returns:
    #   None                        -> This function alters the cells in the group
    def remove_from_complement(self, group, coords, values):
        for coord in group["coords"]:
            if not coord in coords:
                for val in values:
                    self.remove_possibility(coord, val)
    
    def basic_loop(self):
        self.apply_group_functions()

    def solve(self, debug=False):
        changed = True

        while changed:
            changed = False

            pre_grid = deepcopy( self.grid )
            pre_possible = deepcopy( self.possible )

            if debug:
                self.write_log("Pre")

            self.basic_loop()

            if debug:
                self.write_log("Post")

            changed = changed or ( not ( np.all( self.grid == pre_grid ) ) )
            changed = changed or ( not ( np.all( self.possible == pre_possible ) ) )

        if self.is_solved():
            print("Success!")
        else:
            print("Not yet...")

    def is_solved(self):
        return np.all( self.solved )

    def write_log(self, pre_f_name, grid=None, possible=None):
        if grid is None:
            grid = self.grid
        if possible is None:
            possible = self.possible

        f = open( "{}_values.txt".format(pre_f_name), "w" )
        for i in range(self.dim):
            for j in range(self.dim):
                f.write(str(grid[i,j]))
                f.write("\t")
            f.write("\n")
        f.close()

        f = open( "{}_possible.txt".format(pre_f_name), "w" )
        for i in range(self.dim):
            for j in range(self.dim):
                f.write(str(possible[i,j]))
                f.write("\n")
            f.write("\n>>>>>\n")
        f.close()