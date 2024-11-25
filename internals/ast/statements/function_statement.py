from .block_statement import BlockStatement
from .statement import Statement
from ...token import Token

class FunctionStatement(Statement):

    name:Token
    parameters:list[Token]
    functionBody:BlockStatement

    blockStartTokenIndex:int
    blockEndTokenIndex:int

    def __init__(self, name:Token, parameters:list[Token], functionBody:BlockStatement):
        self.name = name
        self.parameters = parameters
        self.functionBody = functionBody

    def accept(self, visitor):
        return visitor.visitFunctionStatement(self)