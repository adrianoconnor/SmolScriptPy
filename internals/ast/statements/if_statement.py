from internals.ast.expressions.expression import Expression
from .statement import Statement

class IfStatement(Statement):

    expression:Expression
    thenStatement:Statement
    elseStatement:Statement

    exprFirstTokenIndex:int
    exprLastTokenIndex:int
    thenFirstTokenIndex:int
    thenLastTokenIndex:int
    elseFirstTokenIndex:int
    elseLastTokenIndex:int

    def __init__(self, expression:Expression, thenStatement:Statement, elseStatement:Statement):
        self.expression = expression
        self.thenStatement = thenStatement
        self.elseStatement = elseStatement

    def accept(self, visitor):
        return visitor.visitIfStatement(self)