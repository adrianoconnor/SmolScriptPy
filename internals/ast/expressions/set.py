from .expression import Expression
from ...token import Token

class SetExpression(Expression):

    obj:Expression
    name:Token
    value:Expression
    
    def __init__(self, object:Expression, name:Token, value:Expression):
        super().__init__()
        self.object = object
        self.name = name
        self.value = value

    def accept(self, visitor):
        return visitor.visitSetExpression(self)