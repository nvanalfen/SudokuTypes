from .RelationalSudokuWidget import RelationalSudokuWidget

class FutoshikiWidget(RelationalSudokuWidget):
    def __init__(self, dim=6, parent=None):
        super(FutoshikiWidget, self).__init__(dim=dim, relations=["", "<", ">"], vertical_relations=["", "^", "v"], parent=parent)

    def solve(self):
        values = {}
        values["type"] = "Futoshiki"
        values["grid"] = self.puzzle_widget.get_grid()
        values["relations"] = self.puzzle_widget.get_relations()
        self.parent.solve( values )