import sys
from functools import partial
import numpy as np
from PyQt5.Qt import QMainWindow, QApplication, QWidget, QPushButton
import PyQt5.QtWidgets
from PyQt5 import QtCore, QtWidgets

from Widgets.FutoshikiWidget import FutoshikiWidget
from Widgets.KropkiWidget import KropkiWidget

class SudokuMainWindow(QMainWindow):
    def __init__(self):
        super(SudokuMainWindow, self).__init__()
        #self.central_widget = QWidget()
        #self.puzzle_widget = KropkiWidget(parent=self)
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.central_widget = KropkiWidget(parent=self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setGeometry( 50, 50, self.central_widget.width(), self.central_widget.height() )

        self.mainLayout.addWidget(self.central_widget)

        #self.setFixedWidth(centralWidget.width() + 100)
        #self.setFixedHeight(centralWidget.height() + 100)
    
    def refresh_view(self):
        self.temp = QPushButton(self,text="?")
        self.temp.setGeometry( QtCore.QRect( 200, 10, 80, 30 ) )
        print("?")
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = SudokuMainWindow()
    w.setWindowTitle('Sudoku Main')
    w.show()
    sys.exit(app.exec_())