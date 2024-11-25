from internals.token import Token
from .expression import Expression

class UnaryExpression(Expression):

    op:Token
    right:Expression

    def __init__(self, op:Token, right:Expression):
        super().__init__()
        self.op = op
        self.right = right

    def accept(self, visitor):
        return visitor.visitUnaryExpression(self)
