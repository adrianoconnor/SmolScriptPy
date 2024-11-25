from .function_statement import FunctionStatement
from .statement import Statement
from ...token import Token

class ClassStatement(Statement):

    className:Token
    superclassName:Token
    functions:list[FunctionStatement]

    blockStartTokenIndex:int
    blockEndTokenIndex:int

    def __init__(self, className:Token, superclassName:Token, functions:list[FunctionStatement]):
        self.className = className
        self.superclassName = superclassName
        self.functions = functions

    def accept(self, visitor):
        return visitor.visitClassStatement(self)
