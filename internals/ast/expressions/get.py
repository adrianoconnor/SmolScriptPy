from .expression import Expression
from internals.token import Token

class GetExpression(Expression):

    def __init__(self, obj:Expression, name:Token):
        super().__init__()
        self.obj:Expression = obj
        self.name:Token = name

    def accept(self, visitor):
        return visitor.visitGetExpression(self)