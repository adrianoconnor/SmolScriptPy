from .expression import Expression
from internals.token import Token

class IndexerSetExpression(Expression):
    
    def __init__(self, obj:Expression, indexerExpression:Expression, value:Expression):
        self.obj:Expression = obj
        self.indexerExpression:Expression = indexerExpression
        self.value:Expression= value

    def accept(self, visitor):
        return visitor.visitIndexerSetExpression(self)