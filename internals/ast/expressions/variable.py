from typing import Optional
from internals.token import Token
from internals.token_types import TokenType
from .expression import Expression

class VariableExpression(Expression):

    name:Token
    prepostfixOp:Optional[TokenType]

    def __init__(self, name:Token, prepostfixOp:Optional[TokenType] = None):
        super().__init__()
        self.name = name
        self.prepostfixOp = prepostfixOp

    def accept(self, visitor):
        return visitor.visitVariableExpression(self)