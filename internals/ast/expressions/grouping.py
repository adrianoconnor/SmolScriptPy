from .expression import Expression
from internals.token import Token

class GroupingExpression(Expression):

    def __init__(self, expr:Expression, castToStringForEmbeddedStringExpression:bool = False):
        self.expr:Expression = expr
        self.castToStringForEmbeddedStringExpression:bool = castToStringForEmbeddedStringExpression

    def accept(self, visitor):
        return visitor.visitGroupingExpression(self)