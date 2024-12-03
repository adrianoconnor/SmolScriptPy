from internals.ast.expressions.expression import Expression
from .statement import Statement

class WhileStatement(Statement):

    def __init__(self, whileCondition:Expression, executeStatement:Statement):
        self.whileCondition:Expression = whileCondition
        self.executeStatement:Statement = executeStatement

        self.exprFirstTokenIndex:int
        self.exprLastTokenIndex:int
        self.stmtFirstTokenIndex:int
        self.stmtLastTokenIndex:int

    def accept(self, visitor):
        return visitor.visitWhileStatement(self)