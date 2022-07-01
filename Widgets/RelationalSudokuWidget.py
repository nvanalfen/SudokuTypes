import numpy as np
from PyQt5.Qt import QWidget, QTextEdit, QSize, QComboBox, QFont
from PyQt5 import QtCore

class ComboBox(QComboBox):
    def __init__(self, width=50, height=30, options=[], parent=None):
        super(ComboBox, self).__init__(parent)

        self.setEditable(True)
        self.lineEdit().setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit().setFont( QFont('Times', 10) )
        self.addItems(options)
        self.lineEdit().setReadOnly(True)

        self.setMinimumSize(QSize(width, height))
        self.setMaximumSize(QSize(width, height))

class TextEdit(QTextEdit):
    def __init__(self, size=50, text="", parent=None):
        super(TextEdit, self).__init__(text, parent)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setFont( QFont('Times', 20) )

        self.setMinimumSize(QSize(size, size))
        self.setMaximumSize(QSize(size, size))

class RelationalSudokuWidget(QWidget):
    def __init__(self, dim=6, relations=[], vertical_relations=[], parent=None):
        super(RelationalSudokuWidget, self).__init__()

        self.relations_options = relations
        self.relations_options_vertical = vertical_relations

        self.dim = dim
        self.cell_size = 50
        self.combo_width = 50
        self.combo_height = 30
        self.spacing = 50
        self.start_x = 50
        self.start_y = 50

        self.boxes = np.repeat( None, self.dim*self.dim ).reshape( (self.dim, self.dim) )
        self.relation_selectors = np.repeat( None, (2*self.dim - 1)*self.dim ).reshape( (2*self.dim - 1, self.dim) )

        self.setup_UI()


    def setup_UI(self):
        for row in range(self.dim):
            for column in range(self.dim):

                # Create and place the box
                self.boxes[row,column] = TextEdit(size=self.cell_size, text="", parent=self)
                box_field = self.boxes[row,column]
                xi = ( column * self.cell_size ) + ( column * self.spacing ) + self.start_x
                yi = ( row * self.cell_size ) + ( row * self.spacing ) + self.start_y

                box_field.setGeometry(QtCore.QRect(xi, yi, self.cell_size, self.cell_size))

                # Create and place horizonal combo boxes
                if column > 0:
                    self.relation_selectors[2*row, column-1] = ComboBox(width=min( self.spacing, self.combo_width ), height=self.combo_height, options=self.relations_options, parent=self)
                    relation = self.relation_selectors[2*row, column-1]
                    xi = ( column * self.cell_size ) + ( (column-1) * self.spacing )  + int( (self.spacing-self.combo_width)/2 ) +  self.start_x
                    yi = ( row * self.cell_size ) + ( row * self.spacing ) + int( (self.cell_size-self.combo_height)/2 ) + self.start_y

                    relation.setGeometry(QtCore.QRect(xi, yi, min( self.spacing, self.combo_width ), self.combo_height))
                if row > 0:
                    self.relation_selectors[2*row-1, column] = ComboBox(width=self.cell_size, height=self.combo_height, options=self.relations_options_vertical, parent=self)
                    relation = self.relation_selectors[2*row-1, column]

                    xi = ( column * self.cell_size ) + ( column * self.spacing ) + self.start_x
                    yi = ( row * self.cell_size ) + ( (row-1) * self.spacing ) + int( (self.spacing-self.combo_height)/2 ) + self.start_y

                    relation.setGeometry(QtCore.QRect(xi, yi, self.cell_size, self.combo_height))