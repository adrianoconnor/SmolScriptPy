from .expression import Expression
from internals.token import Token

class NewInstanceExpression(Expression):
    
    def __init__(self, className:Token, ctorArgs:list[Expression]):
        self.className:Token = className
        self.ctorArgs:list[Expression] = ctorArgs

    def accept(self, visitor):
        return visitor.visitNewInstanceExpression(self)