from .statement import Statement

class BreakStatement(Statement):

    def __init__(self):
        self.tokenIndex:int

    def accept(self, visitor):
        return visitor.visitBreakStatement(self)