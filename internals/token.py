from typing import Optional
from internals.token_types import TokenType


class Token():
    
    def __init__(self, tokenType:TokenType, lexeme:str, literal:Optional[str], line:int, col:int, startPos:int, endPos:int):
        self.type:TokenType = tokenType
        self.lexeme:str = lexeme
        self.literal:Optional[str] = literal
        self.line:int = line
        self.col:int = col
        self.startPos:int = startPos
        self.endPos:int = endPos
        self.isFollowedByLineBreak:bool = False
    
    def __str__(self):
        return str(self.type) + ", " + self.lexeme + " [literal = " + str(self.literal) + "], line: " + str(self.line) + ", col: " + str(self.col) # + str(self.isFollowedByLineBreak)
    