from typing import Optional
from internals.token import Token
from internals.token_types import TokenType
from .expression import Expression

class VariableExpression(Expression):

    def __init__(self, name:Token, prepostfixOp:Optional[TokenType] = None):
        self.name:Token = name
        self.prepostfixOp:Optional[TokenType] = prepostfixOp

    def accept(self, visitor):
        return visitor.visitVariableExpression(self)