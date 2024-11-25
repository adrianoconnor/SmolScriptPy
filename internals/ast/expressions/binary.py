from internals.token import Token
from .expression import Expression

class BinaryExpression(Expression):

    left:Expression
    op:Token
    right:Expression

    def __init__(self, left:Expression, op:Token, right:Expression):
        super().__init__()
        self.left = left
        self.op = op
        self.right = right

    def accept(self, visitor):
        return visitor.visitBinaryExpression(self)
