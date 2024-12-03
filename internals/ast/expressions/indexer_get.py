from .expression import Expression
from internals.token import Token

class IndexerGetExpression(Expression):
    
    def __init__(self, obj:Expression, indexerExpression:Expression):
        self.obj:Expression = obj
        self.indexerExpression:Expression = indexerExpression

    def accept(self, visitor):
        return visitor.visitIndexerGetExpression(self)