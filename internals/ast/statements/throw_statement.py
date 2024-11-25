from .statement import Statement
from ..expressions.expression import Expression

class ThrowStatement(Statement):

    expression:Expression
    
    def __init__(self, expression:Expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitThrowStatement(self)