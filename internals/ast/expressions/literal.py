from internals.variable_types.smol_variable_type import SmolVariable
from .expression import Expression

class LiteralExpression(Expression):

    value:SmolVariable

    def __init__(self, value:SmolVariable):
        super().__init__()
        self.value = value

    def accept(self, visitor):
        return visitor.visitLiteralExpression(self)
    
    def getExpressionType(self):
        return "Literal"