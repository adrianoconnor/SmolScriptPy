from typing import Optional
from .statement import Statement
from ..expressions.expression import Expression

class ReturnStatement(Statement):

    expression:Optional[Expression]

    tokenIndex:int
    exprFirstTokenIndex:int
    exprLastTokenIndex:int

    def __init__(self, expression:Optional[Expression] = None):
        self.expression = expression

    def accept(self, visitor):
        return visitor.visitReturnStatement(self)