from .KenKen import KenKen
import numpy as np
import pandas as pd

class KillerSudoku(KenKen):
    def __init__(self, dimension=6, setup_groups=True, subgrid_shape=(2,3)):
        super().__init__(dimension, setup_groups=False, subgrid_shape=subgrid_shape)
        self.blobs = {}
        self.initialize_sudoku(dimension, setup_groups=setup_groups, subgrid_shape=subgrid_shape)
    
    def initialize_sudoku(self, dimension=6, setup_groups=True, subgrid_shape=(2,3)):
        super().initialize_sudoku(dimension, setup_groups=False, subgrid_shape=subgrid_shape)

        if setup_groups:
            self.set_groups()
    
    def set_groups(self):
        super().set_groups()

    def read_blobs_from_csv(self, f_name):
        blobs = np.array( pd.read_csv( f_name, header=None, index_col=None ) )
        for row in range(len(blobs)):
            for col in range(len(blobs[row])):
                key, val = blobs[row,col].split(":")
                if not key in self.blobs:
                    pass