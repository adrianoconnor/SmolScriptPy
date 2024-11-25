from .expression import Expression
from ...token import Token

class AssignExpression(Expression):

    name:Token
    value:Expression

    def __init__(self, name:Token, value:Expression):
        super().__init__()
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visitAssignExpression(self)
    