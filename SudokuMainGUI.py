import sys
from functools import partial
import numpy as np
from PyQt5.Qt import QMainWindow, QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout
import PyQt5.QtWidgets
from PyQt5 import QtCore, QtWidgets

from Puzzles.Futoshiki import Futoshiki
from Puzzles.Kropki import Kropki
from Puzzles.Sudoku import Sudoku
from Puzzles.KillerSudoku import KillerSudoku
from Puzzles.KenKen import KenKen

from Widgets.FutoshikiWidget import FutoshikiWidget
from Widgets.KropkiWidget import KropkiWidget
from Widgets.RelationalSudokuWidget import PuzzleGridWidget

class SudokuMainWindow(QMainWindow):
    def __init__(self):
        super(SudokuMainWindow, self).__init__()
        self.puzzle_widget = FutoshikiWidget(parent=self)
        self.central_widget = self.puzzle_widget
        self.setCentralWidget(self.central_widget)

        self.show()
    
    def get_puzzle_type(self, puzzle_type):
        if puzzle_type == "Futoshiki":
            return Futoshiki( dimension=self.puzzle_widget.dim )
        if puzzle_type == "Kropki":
            return Kropki( dimension=self.puzzle_widget.dim )
    
    def solve(self, values):
        puzzle_type = values["type"]
        grid = values["grid"]
        relations = None
        if "relations" in values:
            relations = values["relations"]

        puzzle = self.get_puzzle_type(puzzle_type)
        puzzle.load_grid(grid)
        if not relations is None:
            puzzle.load_relations(relations)
        puzzle.solve()

        self.puzzle_widget.puzzle_widget.set_grid( puzzle.grid )

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SudokuMainWindow()
    w.setWindowTitle('Sudoku Main')
    w.show()
    sys.exit(app.exec_())