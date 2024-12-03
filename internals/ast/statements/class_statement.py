from .function_statement import FunctionStatement
from .statement import Statement
from ...token import Token

class ClassStatement(Statement):

    def __init__(self, className:Token, superclassName:Token, functions:list[FunctionStatement]):
        self.className:Token = className
        self.superclassName:Token = superclassName
        self.functions:list[FunctionStatement] = functions

    def accept(self, visitor):
        return visitor.visitClassStatement(self)
