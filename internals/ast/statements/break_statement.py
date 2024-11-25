from .statement import Statement

class BreakStatement(Statement):

    tokenIndex:int

    def __init__(self):
        return

    def accept(self, visitor):
        return visitor.visitBreakStatement(self)