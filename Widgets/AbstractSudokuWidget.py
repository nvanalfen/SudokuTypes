import numpy as np
from PyQt5.Qt import QWidget, QTextEdit, QSize, QComboBox, QFont, QSpinBox, QPushButton, QGroupBox, QLabel
from PyQt5 import QtCore
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout

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

class BackgroundBox(QLabel):
    def __init__(self, size=70, color=None, border=None, parent=None):
        super(BackgroundBox, self).__init__(parent)

        self.parent = parent

        self.color = color
        self.border = border

        self.set_colors()

        self.setMinimumSize(QSize(size, size))
        self.setMaximumSize(QSize(size, size))
    
    def set_colors(self):
        if self.border is None:
            self.border = self.color
        
        self.setStyleSheet( """background-color : {};
                                border : 3px solid {};""".format( self.color, self.border ) )

class Box(QWidget):
    def __init__(self, textbox_size=50, label_size=70, color=None, border=None, parent=None):
        super(Box, self).__init__()

        self.layout = QGridLayout()
        self.background = BackgroundBox(label_size, color, border, self)
        self.textbox = TextEdit(textbox_size, "", self)

        self.setLayout(self.layout)

        self.layout.addWidget( self.background, 0, 0, 3, 3 )
        self.layout.addWidget( self.textbox, 1, 1 )

        self.background.setAlignment(QtCore.Qt.AlignCenter)
        self.textbox.setAlignment(QtCore.Qt.AlignCenter)

        self.setMinimumSize(QSize(label_size+13, label_size+13))
        self.setMaximumSize(QSize(label_size+13, label_size+13))
    
    def toPlainText(self):
        return self.textbox.toPlainText()
    
    def setPlainText(self, text):
        self.textbox.setPlainText(text)

class SubgridSpinner(QGroupBox):
    def __init__(self, subgrid_shape=(3,3), dim=9, parent=None):
        super(SubgridSpinner, self).__init__()
        self.setTitle("Subgrid Dimension (row,col)")
        self.parent = parent
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        rows, columns = subgrid_shape

        self.row_spinner = QSpinBox(self)
        self.row_spinner.setRange(1, dim)
        self.row_spinner.setValue( rows )
        self.layout.addWidget( self.row_spinner )

        self.column_spinner = QSpinBox(self)
        self.column_spinner.setRange(1, dim)
        self.column_spinner.setValue( columns )
        self.layout.addWidget( self.column_spinner )
    
    def get_subgrid(self):
        return self.row_spinner.value(), self.column_spinner.value()

class PuzzleGridWidget(QGroupBox):
    def __init__(self, dim, subgrid_shape, parent=None):
        super(PuzzleGridWidget, self).__init__()
        self.dim = dim
        self.subgrid_shape = subgrid_shape

        self.cell_size = 50
        self.combo_width = 50
        self.combo_height = 30
        self.spinner_size = 40
        self.button_width = 80
        self.button_height = 30
        self.spacing = 50

        self.setup_boxes()

    def setup_boxes(self):
        layout = QGridLayout()
        self.boxes = np.repeat( None, self.dim*self.dim ).reshape( (self.dim, self.dim) )
        colors = [ "rgb(0,200,225)", "rgb(150,150,150)" ]

        for row in range(self.dim):
            for column in range(self.dim):

                ind = ( ( int(row / self.subgrid_shape[0] ) ) + ( int( column / self.subgrid_shape[1] ) ) ) % 2
                color = colors[ind]

                # Create and place the box
                #self.boxes[row,column] = TextEdit(size=self.cell_size, text="", parent=self)
                self.boxes[row,column] = Box(textbox_size=self.cell_size, label_size=70, color=color, border=None, parent=self)
                box_field = self.boxes[row,column]
                layout.addWidget( box_field, row, column )

        self.layout = layout
        self.setLayout(self.layout)

    def get_grid(self):
        grid = np.zeros( self.boxes.shape )

        for row in range(len(self.boxes)):
            for column in range(len(self.boxes[row])):
                if not self.boxes[row,column] is None:
                    val = self.boxes[row,column].toPlainText().strip()
                    if val != '' and int(val) != 0:
                        grid[row,column] = int(val)
        
        return grid

    def set_grid(self, grid):

        for row in range(len(self.boxes)):
            for column in range(len(self.boxes[row])):
                if not self.boxes[row,column] is None and grid[row,column] != 0:
                    self.boxes[row,column].setPlainText( str(grid[row,column]) )

class AbstractSudokuWidget(QWidget):
    def __init__(self, dim=9, subgrid_shape=(3,3), parent=None):
        super(AbstractSudokuWidget, self).__init__()
        self.parent = parent
        self.layout = QGridLayout()
        self.subgrid_shape = subgrid_shape

        self.left_x = 0
        self.upper_y = 0

        self.dim = dim

        # Set Widget sizes
        self.cell_size = 50
        self.combo_width = 50
        self.combo_height = 30
        self.spinner_size = 40
        self.button_width = 80
        self.button_height = 30
        self.spacing = 50

        self.start_x = self.left_x + 50
        self.start_y = self.upper_y + 50

        self.administrative_widget = QWidget()
        self.puzzle_widget = QWidget()

        self.setup_UI()
    
    def generate(self):
        self.dim = self.dim_spinner.value()
        self.subgrid_shape = self.subgrid_spinners.get_subgrid()
        self.layout.removeWidget( self.puzzle_widget )
        self.puzzle_widget.close()
        self.puzzle_widget = PuzzleGridWidget( self.dim, self.subgrid_shape, self )
        self.layout.addWidget( self.puzzle_widget, 1, 0, 10, 10 )

        self.update()
    
    def solve(self):
        values = {}
        values["grid"] = self.puzzle_widget.get_grid()
        self.parent.solve( values )

    def setup_UI(self):

        layout = QGridLayout()

        self.boxes = np.repeat( None, self.dim*self.dim ).reshape( (self.dim, self.dim) )

        # Create a spinner to change the dimension of the puzzle
        self.dim_spinner = QSpinBox(self)
        self.dim_spinner.setValue( self.dim )
        self.dim_spinner.setRange(4, 9)
        layout.addWidget( self.dim_spinner, 0, 0 )

        # Create a button to regerate a puzzle of the right dimension
        self.generate_button = QPushButton( self, text="Generate" )
        self.generate_button.clicked.connect( self.generate )
        layout.addWidget( self.generate_button, 0, 1 )

        # Create button to access the solved function
        self.solve_button = QPushButton( self, text="Solve" )
        self.solve_button.clicked.connect( self.solve )
        layout.addWidget( self.solve_button, 0, 2 )

        # Create Spinners to change subgrid rows
        self.subgrid_spinners = SubgridSpinner( self.subgrid_shape, self.dim, self )
        layout.addWidget( self.subgrid_spinners, 0, 3 )

        self.puzzle_widget = PuzzleGridWidget(self.dim, self.subgrid_shape, self)
        layout.addWidget(self.puzzle_widget, 1, 0, 10, 10)
        self.layout = layout
        self.setLayout(self.layout)

        self.show()