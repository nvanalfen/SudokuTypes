import sys
from functools import partial
import numpy as np
from PyQt5.Qt import QMainWindow, QApplication
import PyQt5.QtWidgets
from PyQt5 import QtCore

from Widgets.FutoshikiWidget import FutoshikiWidget
from Widgets.KropkiWidget import KropkiWidget

class SudokuMainWindow(QMainWindow):
    def __init__(self):
        super(SudokuMainWindow, self).__init__()
        centralWidget = KropkiWidget(parent=self)
        self.setCentralWidget(centralWidget)
        centralWidget.setGeometry( 50, 50, centralWidget.width(), centralWidget.height() )

        #self.setFixedWidth(centralWidget.width() + 100)
        #self.setFixedHeight(centralWidget.height() + 100)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SudokuMainWindow()
    w.setWindowTitle('Sudoku Main')
    w.show()
    sys.exit(app.exec_())