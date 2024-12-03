
from typing import Any, Optional
from internals.opcodes import OpCode

class ByteCodeInstruction:
     
    def __init__(self, opcode:OpCode, operand1:Optional[Any] = None, operand2:Optional[Any] = None):
        self.opcode:OpCode = opcode
        self.operand1:Optional[Any] = operand1
        self.operand2:Optional[Any] = operand2
 
        # This flag tells the debugger that this instruction starts a new statement,
        # which is how it steps through the program
        self.isStatementStartpoint:bool = False

        # These attributes are used for mapping back to the original source code
        self.token_map_start_index:Optional[int]
        self.token_map_end_index:Optional[int]

    def __str__(self) -> str:
        return self.opcode.__str__()