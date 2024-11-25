from .expression import Expression

class TernaryExpression(Expression):

    evaluationExpression:Expression
    expresisonIfTrue:Expression
    expresisonIfFalse:Expression

    def __init__(self, evaluationExpression:Expression, expresisonIfTrue:Expression, expresisonIfFalse:Expression):
        super().__init__()
        self.evaluationExpression = evaluationExpression
        self.expresisonIfTrue = expresisonIfTrue
        self.expresisonIfFalse = expresisonIfFalse

    def accept(self, visitor):
        return visitor.visitTernaryExpression(self)