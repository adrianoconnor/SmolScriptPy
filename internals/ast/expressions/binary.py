from internals.token import Token
from .expression import Expression

class BinaryExpression(Expression):

    def __init__(self, left:Expression, op:Token, right:Expression):
        self.left:Expression = left
        self.op:Token = op
        self.right:Expression = right

    def accept(self, visitor):
        return visitor.visitBinaryExpression(self)
