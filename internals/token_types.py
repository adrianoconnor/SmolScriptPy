from enum import Enum

class TokenType(Enum):
    LEFT_BRACKET = 1
    RIGHT_BRACKET = 2
    LEFT_BRACE = 3,
    RIGHT_BRACE = 4,
    LEFT_SQUARE_BRACKET = 5,
    RIGHT_SQUARE_BRACKET = 6,
    COMMA = 7,
    DOT = 8,
    MINUS = 9,
    PLUS = 10,
    POW = 11,
    SEMICOLON = 12,
    DIVIDE = 13,
    REMAINDER = 14,

    MULTIPLY = 15,
    LOGICAL_AND = 16,
    LOGICAL_OR = 17,

    BITWISE_AND = 18,
    BITWISE_OR = 19,
    BITWISE_XOR = 20,
    BITWISE_NOT = 21,

    QUESTION_MARK = 22,
    COLON = 23,

    NOT = 24,
    NOT_EQUAL = 25,
    EQUAL = 26,
    EQUAL_EQUAL = 27,
    GREATER = 28,
    GREATER_EQUAL = 29,
    LESS = 30,
    LESS_EQUAL = 31,

    PLUS_EQUALS = 32,
    MINUS_EQUALS = 33,
    MULTIPLY_EQUALS = 34,
    POW_EQUALS = 35,
    DIVIDE_EQUALS = 36,
    REMAINDER_EQUALS = 37,

    POSTFIX_INCREMENT = 38,
    PREFIX_INCREMENT = 39,
    POSTFIX_DECREMENT = 40,
    PREFIX_DECREMENT = 41,
    
    FAT_ARROW = 42,

    # Literals

    IDENTIFIER = 43,
    STRING = 44,
    NUMBER = 45,
    
    START_OF_EMBEDDED_STRING_EXPRESSION = 46,
    END_OF_EMBEDDED_STRING_EXPRESSION = 47,

    # Keywords

    BREAK = 48,
    CASE = 49,
    CLASS = 50,
    CONST = 51,
    CONTINUE = 52,
    DEBUGGER = 53,
    DO = 54,
    ELSE = 55,
    FALSE = 56,
    FUNC = 57,
    FOR = 58,
    IF = 59,
    NEW = 60,
    NULL = 61,
    RETURN = 62,
    SUPER = 63,
    SWITCH = 64,
    TRUE = 65,
    VAR = 66,
    WHILE = 67,
    UNDEFINED = 68,
    TRY = 69,
    CATCH = 70,
    FINALLY = 71,
    THROW = 72,

    EOF = 0