from internals.token_types import TokenType


class Token():

    type:TokenType
    lexeme:str
    literal:str
    line:int
    col:int
    startPos:int
    endPos:int
    isFollowedByLineBreak:bool = False

    def __init__(self, tokenType, lexeme, literal, line, col, startPos, endPos):
        self.type = tokenType
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        self.col = col
        self.startPos = startPos
        self.endPos = endPos
    
    def __str__(self):
        return str(self.type) + ", " + self.lexeme + " [literal = " + str(self.literal) + "], line: " + str(self.line) + ", col: " + str(self.col) # + str(self.isFollowedByLineBreak)
    