from internals.ast.expressions.expression import Expression
from .statement import Statement

class IfStatement(Statement):

    def __init__(self, expression:Expression, thenStatement:Statement, elseStatement:Statement):
        self.expression:Expression = expression
        self.thenStatement:Statement = thenStatement
        self.elseStatement:Statement = elseStatement
        
        self.exprFirstTokenIndex:int
        self.exprLastTokenIndex:int
        self.thenFirstTokenIndex:int
        self.thenLastTokenIndex:int
        self.elseFirstTokenIndex:int
        self.elseLastTokenIndex:int

    def accept(self, visitor):
        return visitor.visitIfStatement(self)