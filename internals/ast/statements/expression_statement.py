from .statement import Statement
from ..expressions.expression import Expression

class ExpressionStatement(Statement):

    expression:Expression

    firstTokenIndex:int
    lastTokenIndex:int

    def __init__(self, expression:Expression):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitExpressionStatement(self)