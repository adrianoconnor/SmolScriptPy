from .expression import Expression
from internals.token import Token

class SetExpression(Expression):

    def __init__(self, obj:Expression, name:Token, value:Expression):
        self.obj:Expression = obj
        self.name:Token = name
        self.value:Expression = value

    def accept(self, visitor):
        return visitor.visitSetExpression(self)