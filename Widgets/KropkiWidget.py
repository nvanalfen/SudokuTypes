from .RelationalSudokuWidget import RelationalSudokuWidget

class KropkiWidget(RelationalSudokuWidget):
    def __init__(self, dim=6, parent=None):
        super(KropkiWidget, self).__init__(dim=dim, relations=[".", "B", "W"], vertical_relations=[".", "B", "W"], parent=parent)

    def solve(self):
        values = {}
        values["type"] = "Kropki"
        values["grid"] = self.puzzle_widget.get_grid()
        values["relations"] = self.puzzle_widget.get_relations()
        self.parent.solve( values )