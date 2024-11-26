
from typing import Any, Optional
from internals.opcodes import OpCode

class ByteCodeInstruction:
 
    opcode:OpCode
    operand1:Optional[Any]
    operand2:Optional[Any]

    # This flag tells the debugger that this instruction starts a new statement,
    # which is how it steps through the program
    isStatementStartpoint:bool

    # These attributes are used for mapping back to the original source code
    token_map_start_index:Optional[int]
    token_map_end_index:Optional[int]
    
    def __init__(self, opcode:OpCode, operand1:Optional[Any] = None, operand2:Optional[Any] = None):
        self.opcode = opcode
        self.operand1 = operand1
        self.operand2 = operand2
        self.isStatementStartpoint = False

    def __str__(self) -> str:
        return self.opcode.__str__()