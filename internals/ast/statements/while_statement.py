from internals.ast.expressions.expression import Expression
from .statement import Statement

class WhileStatement(Statement):

    whileCondition:Expression
    executeStatement:Statement

    exprFirstTokenIndex:int
    exprLastTokenIndex:int
    stmtFirstTokenIndex:int
    stmtLastTokenIndex:int

    def __init__(self, whileCondition:Expression, executeStatement:Statement):
        self.whileCondition = whileCondition
        self.executeStatement = executeStatement

    def accept(self, visitor):
        return visitor.visitWhileStatement(self)