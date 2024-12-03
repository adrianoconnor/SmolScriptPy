from typing import Optional
from .statement import Statement

class BlockStatement(Statement):

    def __init__(self, statements:list[Statement], isVirtual:Optional[bool] = False):
        self.statements:list[Statement] = statements
        self.insertedByParser:Optional[bool] = isVirtual

        self.blockStartTokenIndex:int
        self.blockEndTokenIndex:int

    def accept(self, visitor):
        return visitor.visitBlockStatement(self)