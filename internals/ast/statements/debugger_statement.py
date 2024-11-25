from .statement import Statement

class DebuggerStatement(Statement):

    tokenIndex:int

    def __init__(self):
        return

    def accept(self, visitor):
        return visitor.visitDebuggerStatement(self)