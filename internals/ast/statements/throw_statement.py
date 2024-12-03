from .statement import Statement
from ..expressions.expression import Expression

class ThrowStatement(Statement):
    
    def __init__(self, expression:Expression):
        self.expression:Expression = expression

    def accept(self, visitor):
        return visitor.visitThrowStatement(self)