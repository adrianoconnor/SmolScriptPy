from enum import Enum

class OpCode(Enum):
    
    NOP = 0,

    LABEL = 1,
    CALL = 2,
    RETURN = 3,

    ADD = 4,
    SUB = 5,
    DIV = 6,
    MUL = 7,
    POW = 8,
    REM = 9,

    EQL = 10,
    NEQ = 11,
    LT = 12,
    LTE = 13,
    GT = 14,
    GTE = 15,

    BITWISE_AND = 16,
    BITWISE_OR = 17,

    JMPTRUE = 18,
    JMPFALSE = 19,
    JMP = 20,

    DECLARE = 21,

    CONST = 22, # op1: Const index (number), op2: NA
    FETCH = 23,

    STORE = 24,

    ENTER_SCOPE = 25,
    LEAVE_SCOPE = 26,

    TRY = 27,
    CATCH = 28,
    THROW = 29,

    NEW = 30,

    POP_AND_DISCARD = 31,
    DUPLICATE_VALUE = 32,

    LOOP_EXIT = 33,
    LOOP_START = 34,
    LOOP_END = 35,

    CREATE_OBJECT = 36,


    PRINT = 37, # op1: NA, op2: NA
    DEBUGGER = 38,

    START = 39,
    EOF = 40
