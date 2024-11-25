from .expression import Expression
from ...token import Token

class IndexerSetExpression(Expression):

    obj:Expression
    indexerExpression:Expression
    value:Expression
    
    def __init__(self, obj:Expression, indexerExpression:Expression, value:Expression):
        super().__init__()
        self.obj = obj
        self.indexerExpression = indexerExpression
        self.value = value

    def accept(self, visitor):
        return visitor.visitIndexerSetExpression(self)