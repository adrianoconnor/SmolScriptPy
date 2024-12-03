from typing import Optional
from .statement import Statement
from ..expressions.expression import Expression

class ReturnStatement(Statement):
    
    def __init__(self, expression:Optional[Expression] = None):
        self.expression:Optional[Expression] = expression
    
        self.tokenIndex:int
        self.exprFirstTokenIndex:int
        self.exprLastTokenIndex:int
    
    def accept(self, visitor):
        return visitor.visitReturnStatement(self)