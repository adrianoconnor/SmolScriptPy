from .expression import Expression
from ...token import Token

class NewInstanceExpression(Expression):

    className:Token
    ctorArgs:list[Expression]
    
    def __init__(self, className:Token, ctorArgs:list[Expression]):
        super().__init__()
        self.className = className
        self.ctorArgs = ctorArgs

    def accept(self, visitor):
        return visitor.visitNewInstanceExpression(self)