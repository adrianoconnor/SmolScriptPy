from internals.ast.statements.block_statement import BlockStatement
from internals.token import Token
from .expression import Expression

class FunctionExpression(Expression):

    parameters:list[Token]
    functionBody:BlockStatement

    def __init__(self, parameters:list[Token], functionBody:BlockStatement):
        super().__init__()
        self.parameters = parameters
        self.functionBody = functionBody

    def accept(self, visitor):
        return visitor.visitFunctionExpression(self)
    