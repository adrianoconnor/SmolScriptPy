from internals.token import Token
from .expression import Expression

class UnaryExpression(Expression):

    def __init__(self, op:Token, right:Expression):
        self.op:Token = op
        self.right:Expression = right

    def accept(self, visitor):
        return visitor.visitUnaryExpression(self)
