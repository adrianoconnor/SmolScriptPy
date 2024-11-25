from .expression import Expression
from ...token import Token

class GetExpression(Expression):

    obj:Expression
    name:Token
    
    def __init__(self, object:Expression, name:Token):
        super().__init__()
        self.object = object
        self.name = name

    def accept(self, visitor):
        return visitor.visitGetExpression(self)