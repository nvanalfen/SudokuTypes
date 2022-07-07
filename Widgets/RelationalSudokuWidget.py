import numpy as np
from PyQt5.Qt import QWidget, QTextEdit, QSize, QComboBox, QFont, QSpinBox, QPushButton, QGroupBox
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

class PuzzleGridWidget(QGroupBox):
    def __init__(self, dim, relations=[], vertical_relations=[], parent=None):
        super(PuzzleGridWidget, self).__init__()
        self.dim = dim

        self.relations_options = relations
        self.relations_options_vertical = vertical_relations

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
        self.relation_selectors = np.repeat( None, (2*self.dim - 1)*self.dim ).reshape( (2*self.dim - 1, self.dim) )

        for row in range(self.dim):
            for column in range(self.dim):

                # Create and place the box
                self.boxes[row,column] = TextEdit(size=self.cell_size, text="", parent=self)
                box_field = self.boxes[row,column]
                layout.addWidget( box_field, 2*row, 2*column )

                # Create and place horizonal combo boxes
                if column > 0:
                    self.relation_selectors[2*row, column-1] = ComboBox(width=min( self.spacing, self.combo_width ), height=self.combo_height, options=self.relations_options, parent=self)
                    relation = self.relation_selectors[2*row, column-1]
                    layout.addWidget( relation, 2*row, (2*column)-1 )

                if row > 0:
                    self.relation_selectors[2*row-1, column] = ComboBox(width=self.cell_size, height=self.combo_height, options=self.relations_options_vertical, parent=self)
                    relation = self.relation_selectors[2*row-1, column]
                    layout.addWidget( relation, (2*row)-1, 2*column )
        
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
    
    def get_relations(self):
        relations = np.repeat( '', len( self.relation_selectors.flatten() ) ).reshape( self.relation_selectors.shape )
        
        for row in range(len(self.relation_selectors)):
            for column in range(len(self.relation_selectors[row])):
                if not self.relation_selectors[row,column] is None:
                    val = self.relation_selectors[row,column].currentText().strip()
                    if val != '':
                        relations[row,column] = val
        
        return relations

    def set_grid(self, grid):

        for row in range(len(self.boxes)):
            for column in range(len(self.boxes[row])):
                if not self.boxes[row,column] is None and grid[row,column] != 0:
                    self.boxes[row,column].setPlainText( str(grid[row,column]) )

class RelationalSudokuWidget(QWidget):
    def __init__(self, dim=6, relations=[], vertical_relations=[], parent=None):
        super(RelationalSudokuWidget, self).__init__()
        self.parent = parent
        self.layout = QGridLayout()

        self.left_x = 0
        self.upper_y = 0

        self.relations_options = relations
        self.relations_options_vertical = vertical_relations

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
        self.layout.removeWidget( self.puzzle_widget )
        self.puzzle_widget.close()
        self.puzzle_widget = PuzzleGridWidget( self.dim, self.relations_options, self.relations_options_vertical, self )
        self.layout.addWidget( self.puzzle_widget, 1, 0, 10, 10 )

        self.update()
    
    def solve(self):
        values = {}
        values["grid"] = self.puzzle_widget.get_grid()
        values["relations"] = self.puzzle_widget.get_relations()
        self.parent.solve( values )

    def setup_UI(self):

        layout = QGridLayout()

        self.boxes = np.repeat( None, self.dim*self.dim ).reshape( (self.dim, self.dim) )
        self.relation_selectors = np.repeat( None, (2*self.dim - 1)*self.dim ).reshape( (2*self.dim - 1, self.dim) )

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

        self.puzzle_widget = PuzzleGridWidget(self.dim, self.relations_options, self.relations_options_vertical, self)
        layout.addWidget(self.puzzle_widget, 1, 0, 10, 10)
        self.layout = layout
        self.setLayout(self.layout)

        self.show()