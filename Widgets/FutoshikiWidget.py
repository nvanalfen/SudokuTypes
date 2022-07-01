from .RelationalSudokuWidget import RelationalSudokuWidget

class FutoshikiWidget(RelationalSudokuWidget):
    def __init__(self, dim=6, parent=None):
        super(FutoshikiWidget, self).__init__(dim=dim, relations=["", "<", ">"], vertical_relations=["", "^", "v"], parent=parent)