from .expression import Expression
from ...token import Token

class IndexerGetExpression(Expression):

    obj:Expression
    indexerExpression:Expression
    
    def __init__(self, obj:Expression, indexerExpression:Expression):
        super().__init__()
        self.obj = obj
        self.indexerExpression = indexerExpression

    def accept(self, visitor):
        return visitor.visitIndexerGetExpression(self)