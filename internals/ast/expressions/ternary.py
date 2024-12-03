from .expression import Expression

class TernaryExpression(Expression):

    def __init__(self, evaluationExpression:Expression, expresisonIfTrue:Expression, expresisonIfFalse:Expression):
        self.evaluationExpression:Expression = evaluationExpression
        self.expresisonIfTrue:Expression = expresisonIfTrue
        self.expresisonIfFalse:Expression = expresisonIfFalse

    def accept(self, visitor):
        return visitor.visitTernaryExpression(self)