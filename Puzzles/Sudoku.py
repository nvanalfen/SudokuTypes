from setuptools import setup
from AbstractSudoku import AbstractSudoku
import numpy as np

class Sudoku(AbstractSudoku):
    def __init__(self, dimension=9, setup_groups=True, subgrid_shape=(3,3)):
        super().__init__(dimension, setup_groups=False, subgrid_shape=subgrid_shape)
        self.initialize_sudoku(dimension, setup_groups=setup_groups, subgrid_shape=subgrid_shape)
    
    def initialize_sudoku(self, dimension, setup_groups=True, subgrid_shape=(3,3)):
        super().initialize_sudoku(dimension, setup_groups=False, subgrid_shape=None)
        self.subgrid_rows = None
        self.subgrid_columns = None

        if not subgrid_shape is None:
            self.subgrid_rows, self.subgrid_columns = subgrid_shape            
        
        if setup_groups:
            self.set_groups()

    def set_groups(self):
        super().set_groups()

        if self.subgrid_rows is None or self.subgrid_columns is None:
            return

        grids_y, grids_x = ( int(self.dim/self.subgrid_rows), int(self.dim/self.subgrid_columns) )
        self.groups["subgrid"] = np.repeat( None, grids_x*grids_y ).reshape( (grids_y, grids_x) )
        for row in range(grids_y):
            for col in range(grids_x):
                group = {}
                group["coords"] = set()
                group["functions"] = [ self.N_of_N_counts, self.N_of_N_possibilities ]
                group["properties"] = {}
                self.groups["subgrid"][row,col] = group
        
        for row in range(self.dim):
            for col in range(self.dim):
                x = int( col / grids_x )
                y = int( row / grids_y )
                self.groups["subgrid"][y,x]["coords"].add( (col,row) )
