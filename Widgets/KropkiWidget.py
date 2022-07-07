from .RelationalSudokuWidget import RelationalSudokuWidget

class KropkiWidget(RelationalSudokuWidget):
    def __init__(self, dim=6, parent=None):
        super(KropkiWidget, self).__init__(dim=dim, relations=[".", "B", "W"], vertical_relations=[".", "B", "W"], parent=parent)
