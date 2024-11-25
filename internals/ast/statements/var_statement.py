from internals.ast.expressions.expression import Expression
from .statement import Statement
from ...token import Token

class VarStatement(Statement):

    name:Token
    initializer:Expression

    firstTokenIndex:int
    lastTokenIndex:int

    def __init__(self, name:Token, initializer:Expression):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visitVarStatement(self)