from internals.ast.statements.block_statement import BlockStatement
from internals.token import Token
from .expression import Expression

class FunctionExpression(Expression):

    def __init__(self, parameters:list[Token], functionBody:BlockStatement):
        self.parameters:list[Token] = parameters
        self.functionBody:BlockStatement = functionBody

    def accept(self, visitor):
        return visitor.visitFunctionExpression(self)
    