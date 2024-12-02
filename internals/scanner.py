from typing import Any, Dict
from compiler_error import SmolCompilerError
from .token_types import TokenType
from .token import Token

class Scanner:

    tokens:list[Token] = []
    
    keywords:Dict[str,TokenType] = {
        "break": TokenType.BREAK,
        "class": TokenType.CLASS,
        "case": TokenType.CASE,
        "const": TokenType.CONST,
        "continue": TokenType.CONTINUE,
        "debugger": TokenType.DEBUGGER,
        "do": TokenType.DO,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "function": TokenType.FUNC,
        "if": TokenType.IF,
        "null": TokenType.NULL,
        "new": TokenType.NEW,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "switch": TokenType.SWITCH,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "let": TokenType.VAR,
        "while": TokenType.WHILE,
        "undefined": TokenType.UNDEFINED,
        "try": TokenType.TRY,
        "catch": TokenType.CATCH,
        "finally": TokenType.FINALLY,
        "throw": TokenType.THROW
    }

    startOfToken:int = 0
    currentPos:int = 0
    currentLine:int = 1
    currentLineStartIndex:int = 0
    previous:int = 0
    source:str = ""

    def __init__(self, source:str):
        self.tokens = []
        self.startOfToken = 0
        self.currentPos = 0
        self.currentLine = 0
        self.currentLineStartIndex = 0
        self.previous = 0

        self.source = source

    @staticmethod
    def tokenize(source:str) -> list[Token]:
        return Scanner(source).scan()
    
    def scan(self):
        while(self.reachedEnd() == False):
            self.startOfToken = self.currentPos
            self.scanToken()        
        self.tokens.append(Token(TokenType.EOF, "", None, self.currentLine, self.currentPos - self.currentLineStartIndex + 1, self.currentPos, self.currentPos))

    def reachedEnd(self):
        return self.currentPos >= self.source.__len__()

    def nextChar(self):
        c = self.source[self.currentPos]
        self.currentPos += 1
        return c
    
    def peek(self, peekAheadChars:int = 0):
        if (self.reachedEnd()):
            return '\0'

        return self.source[self.currentPos + peekAheadChars]
    
    def matchNext(self, charToMatch:str):
        if (self.peek() == charToMatch):
            self.nextChar()
            return True
        else:
            return False

    def addToken(self, tokenType:TokenType, literal:Any = None):
        lexeme = self.source[self.startOfToken:self.currentPos]
        self.tokens.append(Token(tokenType, lexeme, literal, self.currentLine, self.startOfToken - self.currentLineStartIndex + 1, self.previous, self.currentPos))
        self.previous = self.currentPos

    def charIsDigit(self, char):
        return char >= "0" and char <= "9"
    
    def charIsAlpha(self, char):
        return (char >= "a" and char <= "z") or (char >= "A" and char <= "Z") or char == "_"

    def charIsAlphaNumeric(self, char):
        return self.charIsAlpha(char) or self.charIsDigit(char)
    
    def scanToken(self):
        c = self.nextChar()

        match c:
            case "(":
                self.addToken(TokenType.LEFT_BRACKET)
            case ")":
                self.addToken(TokenType.RIGHT_BRACKET)
            case "{":
                self.addToken(TokenType.LEFT_BRACE)
            case "}":
                self.addToken(TokenType.RIGHT_BRACE)
            case "[":
                self.addToken(TokenType.LEFT_SQUARE_BRACKET)
            case "]":
                self.addToken(TokenType.RIGHT_SQUARE_BRACKET)
            case ",":
                self.addToken(TokenType.COMMA)
            case ".":
                self.addToken(TokenType.DOT)
            case "?":
                self.addToken(TokenType.QUESTION_MARK)
            case ":":
                self.addToken(TokenType.COLON)
            case ";":
                self.addToken(TokenType.SEMICOLON)

            case "-":
                if (self.matchNext('-')):
                    if (self.tokens.__len__() > 0 and self.tokens[self.tokens.__len__() - 1].type == TokenType.IDENTIFIER
                        and self.tokens[self.tokens.__len__() - 1].isFollowedByLineBreak == False):
                        self.addToken(TokenType.POSTFIX_DECREMENT)
                    else:
                        self.addToken(TokenType.PREFIX_DECREMENT)
                elif (self.matchNext("=")):
                    self.addToken(TokenType.MINUS_EQUALS)
                else:
                    self.addToken(TokenType.MINUS)

            case "+":
                if (self.matchNext('+')):
                    if (self.tokens.__len__() > 0 and self.tokens[self.tokens.__len__() - 1].type == TokenType.IDENTIFIER
                        and self.tokens[self.tokens.__len__() - 1].isFollowedByLineBreak == False):
                        self.addToken(TokenType.POSTFIX_INCREMENT)
                    else:
                        self.addToken(TokenType.PREFIX_INCREMENT)
                elif (self.matchNext("=")):
                    self.addToken(TokenType.PLUS_EQUALS)
                else:
                    self.addToken(TokenType.PLUS)
                    
            case "*":
                if (self.matchNext("*")):
                    if (self.matchNext("=")):
                        self.addToken(TokenType.POW_EQUALS)
                    else:
                       self.addToken(TokenType.POW)
                elif (self.matchNext("=")):
                    self.addToken(TokenType.MULTIPLY_EQUALS)
                else:
                    self.addToken(TokenType.MULTIPLY)

            case "/":
                if (self.matchNext("/")):
                    while(self.peek() != "\n" and not(self.reachedEnd())):
                        self.nextChar()
                elif (self.matchNext("*")):
                    while (self.peek() != "*" or self.peek(1) != "/"):
                        if (self.reachedEnd()):
                            raise SmolCompilerError("Expected end of a comment block but reached the end of the file")
                        else:
                            tc = self.nextChar()

                            if (tc == '\n'):
                                self.currentLine += 1
                                self.currentLineStartIndex = self.currentPos

                    self.matchNext("*")
                    self.matchNext("/")

                elif (self.matchNext("=")):
                    self.addToken(TokenType.DIVIDE_EQUALS)
                else:
                    self.addToken(TokenType.DIVIDE)

            case "!":
                if (self.matchNext("=")):
                    self.addToken(TokenType.NOT_EQUAL)
                else:
                    self.addToken(TokenType.NOT)

            case "=":
                if (self.matchNext("=")):
                    self.addToken(TokenType.EQUAL)
                elif (self.matchNext(">")):
                    self.addToken(TokenType.FAT_ARROW)
                else:
                    self.addToken(TokenType.EQUAL)

            case "<":
                if (self.matchNext("=")):
                    self.addToken(TokenType.LESS_EQUAL)
                else:
                    self.addToken(TokenType.LESS)

            case ">":
                if (self.matchNext("=")):
                    self.addToken(TokenType.GREATER_EQUAL)
                else:
                    self.addToken(TokenType.GREATER)

            case "%":
                if (self.matchNext("=")):
                    self.addToken(TokenType.REMAINDER_EQUALS)
                else:
                    self.addToken(TokenType.REMAINDER)

            case "&":
                if (self.matchNext("&")):
                    self.addToken(TokenType.LOGICAL_AND)
                else:
                    self.addToken(TokenType.BITWISE_AND)

            case "|":
                if (self.matchNext("|")):
                    self.addToken(TokenType.LOGICAL_OR)
                else:
                    self.addToken(TokenType.BITWISE_OR)

            case " ":
                self.previous = self.currentPos
            
            case '\r':
                return
            
            case '\t':
                return

            case '\n':
                self.currentLine += 1
                self.currentLineStartIndex = self.currentPos

                if (self.tokens.__len__() > 0):
                    self.tokens[self.tokens.__len__() - 1].isFollowedByLineBreak = True

            case "'":
                self.processString("'")

            case _:
                if (self.charIsDigit(c)):
                    self.processNumber()
                elif (self.charIsAlpha(c)):
                    self.processIdenitifier()
                else:
                    raise SmolCompilerError("error scanning, unexpected character: ", c)
        return
    
    def processNumber(self):
        
        while (self.charIsDigit(self.peek())):
            self.nextChar()

        if (self.peek() == "." and self.charIsDigit(self.peek(1))):
            self.nextChar()
            while (self.charIsDigit(self.peek())):
                self.nextChar()

        stringValue = self.source[self.startOfToken:self.currentPos]

        self.addToken(TokenType.NUMBER, float(stringValue))

    def processIdenitifier(self):
        
        while (self.charIsAlphaNumeric(self.peek())):
            self.nextChar()

        stringValue = self.source[self.startOfToken:self.currentPos]

        if (self.keywords.__contains__(stringValue)):
            self.addToken(self.keywords[stringValue])
        else:
            self.addToken(TokenType.IDENTIFIER)

    def processString(self, quoteChar):

        string = ""

        while(self.peek() != quoteChar and not(self.reachedEnd())):
            if (self.matchNext("\n")):
                raise SmolCompilerError("Unexpected newline in string")
            string += self.nextChar()
        
        if (self.reachedEnd()):
            raise SmolCompilerError("Unterminated string")
        
        self.nextChar()

        self.addToken(TokenType.STRING, string)
    