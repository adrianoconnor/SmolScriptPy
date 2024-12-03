from .statement import Statement
from ..expressions.expression import Expression

class ExpressionStatement(Statement):

    def __init__(self, expression:Expression):
        self.expression:Expression = expression
        
        self.firstTokenIndex:int
        self.lastTokenIndex:int

    def accept(self, visitor):
        return visitor.visitExpressionStatement(self)