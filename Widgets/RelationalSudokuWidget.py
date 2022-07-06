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

class PuzzleWidget(QWidget):
    def __init__(self, dim, relations=[], vertical_relations=[], parent=None):
        super(PuzzleGridWidget, self).__init__(parent)
        self.dim = dim


        self.left_x = 0
        self.upper_y = 0

        self.relations_options = relations
        self.relations_options_vertical = vertical_relations

        # Set Widget sizes
        self.cell_size = 50
        self.combo_width = 50
        self.combo_height = 30
        self.spinner_size = 40
        self.button_width = 80
        self.button_height = 30
        self.spacing = 50

        self.width = ( self.cell_size * self.dim ) + ( self.spacing * (self.dim - 1) )
        self.height = ( self.cell_size * self.dim ) + ( self.spacing * (self.dim - 1) )
    
    def setup_boxes(self):
        self.boxes = np.repeat( None, self.dim*self.dim ).reshape( (self.dim, self.dim) )
        self.relation_selectors = np.repeat( None, (2*self.dim - 1)*self.dim ).reshape( (2*self.dim - 1, self.dim) )

        for row in range(self.dim):
            for column in range(self.dim):

                # Create and place the box
                self.boxes[row,column] = TextEdit(size=self.cell_size, text="", parent=self.parent)
                box_field = self.boxes[row,column]
                xi = ( column * self.cell_size ) + ( column * self.spacing ) + self.start_x
                yi = ( row * self.cell_size ) + ( row * self.spacing ) + self.start_y

                box_field.setGeometry(QtCore.QRect(xi, yi, self.cell_size, self.cell_size))

                # Create and place horizonal combo boxes
                if column > 0:
                    self.relation_selectors[2*row, column-1] = ComboBox(width=min( self.spacing, self.combo_width ), height=self.combo_height, options=self.relations_options, parent=self.parent)
                    relation = self.relation_selectors[2*row, column-1]
                    xi = ( column * self.cell_size ) + ( (column-1) * self.spacing )  + int( (self.spacing-self.combo_width)/2 ) +  self.start_x
                    yi = ( row * self.cell_size ) + ( row * self.spacing ) + int( (self.cell_size-self.combo_height)/2 ) + self.start_y

                    relation.setGeometry(QtCore.QRect(xi, yi, min( self.spacing, self.combo_width ), self.combo_height))
                if row > 0:
                    self.relation_selectors[2*row-1, column] = ComboBox(width=self.cell_size, height=self.combo_height, options=self.relations_options_vertical, parent=self.parent)
                    relation = self.relation_selectors[2*row-1, column]

                    xi = ( column * self.cell_size ) + ( column * self.spacing ) + self.start_x
                    yi = ( row * self.cell_size ) + ( (row-1) * self.spacing ) + int( (self.spacing-self.combo_height)/2 ) + self.start_y

                    relation.setGeometry(QtCore.QRect(xi, yi, self.cell_size, self.combo_height))



class RelationalSudokuWidget(QWidget):
    def __init__(self, dim=6, relations=[], vertical_relations=[], parent=None):
        super(RelationalSudokuWidget, self).__init__()
        self.parent = parent
        self.layout = QVBoxLayout()

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
        
        self.clear_widgets()
        self.dim = self.dim_spinner.value()
        #self.layout.removeWidget( self.puzzle_widget )
        #self.puzzle_widget.close()
        #self.puzzle_widget = PuzzleGridWidget( self.dim, self.relations_options, self.relations_options_vertical, self )
        #self.layout.addWidget( self.puzzle_widget )
        #self.layout.update()

        self.setup_boxes()
        self.update()
        #self.parent.refresh_view()
        print(self.boxes.shape)

    def setup_UI(self):

        layout = QVBoxLayout()

        self.boxes = np.repeat( None, self.dim*self.dim ).reshape( (self.dim, self.dim) )
        self.relation_selectors = np.repeat( None, (2*self.dim - 1)*self.dim ).reshape( (2*self.dim - 1, self.dim) )

        # Create a spinner to change the dimension of the puzzle
        self.dim_spinner = QSpinBox(self)
        self.dim_spinner.setValue( self.dim )
        self.dim_spinner.setRange(4, 9)
        #x = self.start_x
        #y = self.upper_y
        #self.dim_spinner.setGeometry(QtCore.QRect(x, y, self.spinner_size, self.spinner_size))
        layout.addWidget( self.dim_spinner )

        # Create a button to regerate a puzzle of the right dimension
        self.generate_button = QPushButton( self, text="Generate" )
        self.generate_button.clicked.connect( self.generate )
        #x += self.spinner_size + self.spacing
        #y = self.upper_y
        #self.generate_button.setGeometry( QtCore.QRect( x, y, self.button_width, self.button_height ) )
        layout.addWidget( self.generate_button )

        # Create button to access the solved function
        self.solve_button = QPushButton( self, text="Solve" )
        self.solve_button.clicked.connect( self.solve )
        #x += self.button_width + self.spacing
        #y = self.upper_y
        #self.solve_button.setGeometry( QtCore.QRect( x, y, self.button_width, self.button_height ) )
        layout.addWidget( self.solve_button )

        #self.puzzle_widget = PuzzleGridWidget( self.dim, self.relations_options, self.relations_options_vertical, self )
        #self.puzzle_widget.setGeometry( QtCore.QRect( self.spacing, y+self.spacing, self.puzzle_widget.width, self.puzzle_widget.height ) )
        #self.setup_boxes()
        self.puzzle_widget = PuzzleGridWidget(self.dim, self.relations_options, self.relations_options_vertical, self)
        layout.addWidget(self.puzzle_widget)

        self.show()

        #self.setup_boxes()

    def setup_boxes(self):

        self.boxes = np.repeat( None, self.dim*self.dim ).reshape( (self.dim, self.dim) )
        self.relation_selectors = np.repeat( None, (2*self.dim - 1)*self.dim ).reshape( (2*self.dim - 1, self.dim) )

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

    def clear_widgets(self):
        for i in range(len(self.boxes)):
            for j in range(len(self.boxes[i])):
                if self.boxes[i,j] is None:
                    continue 
                
                self.boxes[i,j].close()
        
        for i in range(len(self.relation_selectors)):
            for j in range(len(self.relation_selectors[i])):
                if self.relation_selectors[i,j] is None:
                    continue 
                
                self.relation_selectors[i,j].close()

    def solve(self):
        pass