from .AbstractSudokuWidget import AbstractSudokuWidget

class SudokuWidget(AbstractSudokuWidget):
    def __init__(self, dim=9, subgrid_shape=(3,3), parent=None):
        super(SudokuWidget, self).__init__( dim=dim, subgrid_shape=subgrid_shape, parent=parent)