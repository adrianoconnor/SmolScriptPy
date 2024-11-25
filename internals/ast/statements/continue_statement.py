from .statement import Statement

class ContinueStatement(Statement):

    tokenIndex:int

    def __init__(self):
        return

    def accept(self, visitor):
        return visitor.visitContinueStatement(self)