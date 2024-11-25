from .block_statement import BlockStatement
from .statement import Statement
from ...token import Token

class TryStatement(Statement):

    tryBody:BlockStatement
    exceptionVariableName:Token
    catchBody:BlockStatement
    finallyBody:BlockStatement

    def __init__(self, tryBody:BlockStatement, exceptionVariableName:Token, catchBody:BlockStatement, finallyBody:BlockStatement):
        self.tryBody = tryBody
        self.exceptionVariableName = exceptionVariableName
        self.catchBody = catchBody
        self.finallyBody = finallyBody

    def accept(self, visitor):
        return visitor.visitTryStatement(self)