from .expression import Expression
from ...token import Token

class GroupingExpression(Expression):

    expr:Expression
    castToStringForEmbeddedStringExpression:bool = False

    def __init__(self, expr:Expression, castToStringForEmbeddedStringExpression:bool = False):
        super().__init__()
        self.expr = expr
        self.castToStringForEmbeddedStringExpression = castToStringForEmbeddedStringExpression

    def accept(self, visitor):
        return visitor.visitGroupingExpression(self)