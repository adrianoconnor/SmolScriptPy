from .statement import Statement

class DebuggerStatement(Statement):
    
    def __init__(self):
        self.tokenIndex:int

    def accept(self, visitor):
        return visitor.visitDebuggerStatement(self)