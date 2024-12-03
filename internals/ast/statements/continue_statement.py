from .statement import Statement

class ContinueStatement(Statement):

    def __init__(self):
        self.tokenIndex:int

    def accept(self, visitor):
        return visitor.visitContinueStatement(self)