from typing import Optional
from .statement import Statement

class BlockStatement(Statement):

    statements:list[Statement]
    insertedByParser:Optional[bool]

    blockStartTokenIndex:int
    blockEndTokenIndex:int

    def __init__(self, statements:list[Statement], isVirtual:Optional[bool] = False):
        self.statements = statements
        self.insertedByParser = isVirtual

    def accept(self, visitor):
        return visitor.visitBlockStatement(self)