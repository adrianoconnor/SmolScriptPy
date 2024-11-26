from internals.scope_environment import ScopeEnvironment
from .smol_stack_type import SmolStackType

class SmolCallSiteSaveState(SmolStackType):

    code_section:int
    pc:int
    previous_env:ScopeEnvironment
    call_is_extern:bool

    def __init__(self, code_section:int, pc:int, previous_env:ScopeEnvironment, call_is_extern:bool):
        super().__init__()
        self.code_section = code_section
        self.pc = pc
        self.previous_env = previous_env
        self.call_is_extern = call_is_extern

    def toString(self):
        return "(SmolCallSiteSaveState)"