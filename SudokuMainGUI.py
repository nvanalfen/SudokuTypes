import sys
from functools import partial
import numpy as np
from PyQt5.Qt import QMainWindow, QApplication, QWidget, QPushButton, QAction
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout

from Puzzles.Futoshiki import Futoshiki
from Puzzles.Kropki import Kropki
from Puzzles.Sudoku import Sudoku
from Puzzles.KillerSudoku import KillerSudoku
from Puzzles.KenKen import KenKen

from Widgets.FutoshikiWidget import FutoshikiWidget
from Widgets.KropkiWidget import KropkiWidget
from Widgets.RelationalSudokuWidget import PuzzleGridWidget
from Widgets.AbstractSudokuWidget import AbstractSudokuWidget
from Widgets.SudokuWidget import SudokuWidget

class ManagerWidget(QWidget):
    def __init__(self, central):
        super(ManagerWidget, self).__init__()

        self.central = central
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.central)
        self.setLayout(self.layout)
    
    def swap_widget(self, central):
        if not self.central is None:
            self.layout.removeWidget( self.central )
            self.central.close()
        self.central = central
        self.layout.addWidget( self.central )

        self.update()

class SudokuMainWindow(QMainWindow):
    def __init__(self):
        super(SudokuMainWindow, self).__init__()

        self.puzzle_type = "Kropki"
        self.puzzle_widget = KropkiWidget(parent=self)
        #self.puzzle_widget = AbstractSudokuWidget(dim=6, subgrid_shape=(2,3), parent=self)
        self.manager = ManagerWidget( self.puzzle_widget )


        #self.central_widget = self.puzzle_widget
        self.central_widget = self.manager
        self.setCentralWidget(self.central_widget)

        self._createMenuBar()
        self.connect_actions()

        self.show()
    
    def _createMenuBar(self):
        menuBar = self.menuBar()
        self.puzzle_menu = menuBar.addMenu("&Puzzles")

        self.sudoku_action = QAction("Classic Sudoku", self)
        self.killer_sudoku_action = QAction("Killer Sudoku", self)
        self.kenken_action = QAction("Kenken", self)
        self.futoshiki_action = QAction("Futoshiki", self)
        self.kropki_action = QAction("Kropki", self)

        self.puzzle_menu.addAction(self.sudoku_action)
        self.puzzle_menu.addAction(self.killer_sudoku_action)
        self.puzzle_menu.addAction(self.kenken_action)
        self.puzzle_menu.addAction(self.futoshiki_action)
        self.puzzle_menu.addAction(self.kropki_action)
        

    def connect_actions(self):
        self.sudoku_action.triggered.connect( lambda : self.set_puzzle_type( "Sudoku" ) )
        self.killer_sudoku_action.triggered.connect( lambda : self.set_puzzle_type( "Killer Sudoku" ) )
        self.kenken_action.triggered.connect( lambda : self.set_puzzle_type( "Kenken" ) )
        self.futoshiki_action.triggered.connect( lambda : self.set_puzzle_type( "Futoshiki" ) )
        self.kropki_action.triggered.connect( lambda : self.set_puzzle_type( "Kropki" ) )
    
    def set_puzzle_type(self, puzzle_type):
        if puzzle_type == self.puzzle_type:
            return
        
        self.puzzle_type = puzzle_type
        self.puzzle_widget = self.get_widget_type()
        self.manager.swap_widget( self.puzzle_widget )
        self.update()
    
    def get_puzzle_type(self, puzzle_type=None):
        if puzzle_type is None:
            puzzle_type = self.puzzle_type

        if puzzle_type == "Sudoku":
            subgrid = self.puzzle_widget.subgrid_shape
            return Sudoku( dimension=self.puzzle_widget.dim, subgrid_shape=subgrid )
        if puzzle_type == "Killer Sudoku":
            return KillerSudoku( dimension=self.puzzle_widget.dim )
        if puzzle_type == "KenKen":
            return KenKen( dimension=self.puzzle_widget.dim )
        if puzzle_type == "Futoshiki":
            return Futoshiki( dimension=self.puzzle_widget.dim )
        if puzzle_type == "Kropki":
            return Kropki( dimension=self.puzzle_widget.dim )
        
        print( "{} not supported".format(puzzle_type) )
        
    def get_widget_type(self, puzzle_type=None):
        if puzzle_type is None:
            puzzle_type = self.puzzle_type
            
        if puzzle_type == "Sudoku":
            return SudokuWidget(parent=self)
            pass
        if puzzle_type == "Killer Sudoku":
            #return KillerSudokuWidget()
            pass
        if puzzle_type == "KenKen":
            #return KenKenWidget()
            pass
        if puzzle_type == "Futoshiki":
            return FutoshikiWidget(dim=self.puzzle_widget.dim, parent=self)
        if puzzle_type == "Kropki":
            return KropkiWidget(dim=self.puzzle_widget.dim, parent=self)
        
        print( "{} Widget not supported".format(puzzle_type) )
    
    def solve(self, values):
        grid = values["grid"]
        relations = None
        if "relations" in values:
            relations = values["relations"]

        puzzle = self.get_puzzle_type()
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