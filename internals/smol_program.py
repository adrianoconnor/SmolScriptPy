from typing import Optional
from internals.bytecode_instruction import ByteCodeInstruction
from internals.opcodes import OpCode
from internals.variable_types.smol_function import SmolFunction
from internals.variable_types.smol_variable_type import SmolVariableType
from internals.token import Token

class SmolProgram:

    def __init__(self):
        self.constants:list[SmolVariableType] = []
        self.code_sections:list[list[ByteCodeInstruction]] = []
        self.function_table:list[SmolFunction] = []
        self.tokens:list[Token] = []
        self.source:Optional[str] = None

    def decompile(self, html:bool = False) -> str:
        p = ''

        p += f'.constants\n'
        n = -1
        for c in self.constants:
            n += 1

            p += f'{n}: {c.getValue()}\n'

        p += f'\n'

        n = -1
        for s in self.code_sections:
            n += 1

            p += f'.code_section_{n}\n'
            # idx:int = 1
            for i in s:
                if (i.isStatementStartpoint and i.opcode != OpCode.START):
                    p += '* '
                else:
                    p += '  '
                
                op1 = f' {i.operand1}' if i.operand1 != None else ''
                op2 = f' {i.operand1}' if i.operand2 != None else ''

                if (i.opcode == OpCode.CONST):
                    p += f'{i.opcode} [{i.operand1}] {self.constants[int(str(i.operand1))]}'
                elif (i.opcode == OpCode.START):
                    p += f'PROGRAM START'
                elif (i.opcode == OpCode.EOF):
                    p += f'PROGRAM END' 
                else:
                    p += f'{i.opcode}{op1}{op2}'
                
                p += '\n'
            
            p += f'\n'

        p += f'.function_table:\n'

        n = -1
        for fn in self.function_table: 
            n += 1
            p += f'{n}: name: {fn.global_function_name}, code_section: {fn.code_section}, arity: {fn.arity}, parameter names: {fn.param_variable_names}\n'
    
        p += f''

        return p