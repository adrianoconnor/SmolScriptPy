from internals.ast.expressions.expression import Expression
from .statement import Statement
from ...token import Token

class VarStatement(Statement):
    
    def __init__(self, name:Token, initializer:Expression):
        self.name:Token = name
        self.initializer:Expression = initializer

        self.firstTokenIndex:int
        self.lastTokenIndex:int

    def accept(self, visitor):
        return visitor.visitVarStatement(self)