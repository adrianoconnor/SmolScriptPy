from internals.variable_types.smol_variable_type import SmolVariableType
from .expression import Expression

class LiteralExpression(Expression):

    def __init__(self, value:SmolVariableType):
        self.value:SmolVariableType = value

    def accept(self, visitor):
        return visitor.visitLiteralExpression(self)
    
    def getExpressionType(self):
        return "Literal"