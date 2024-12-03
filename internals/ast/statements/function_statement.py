from .block_statement import BlockStatement
from .statement import Statement
from ...token import Token

class FunctionStatement(Statement):
    
    def __init__(self, name:Token, parameters:list[Token], functionBody:BlockStatement):
        self.name:Token = name
        self.parameters:list[Token] = parameters
        self.functionBody:BlockStatement = functionBody

        self.blockStartTokenIndex:int
        self.blockEndTokenIndex:int


    def accept(self, visitor):
        return visitor.visitFunctionStatement(self)