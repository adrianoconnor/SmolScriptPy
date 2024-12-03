from .block_statement import BlockStatement
from .statement import Statement
from ...token import Token

class TryStatement(Statement):

    def __init__(self, tryBody:BlockStatement, exceptionVariableName:Token, catchBody:BlockStatement, finallyBody:BlockStatement):
        self.tryBody:BlockStatement = tryBody
        self.exceptionVariableName:Token = exceptionVariableName
        self.catchBody:BlockStatement = catchBody
        self.finallyBody:BlockStatement = finallyBody

    def accept(self, visitor):
        return visitor.visitTryStatement(self)