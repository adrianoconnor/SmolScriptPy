from internals.scope_environment import ScopeEnvironment
from .smol_stack_type import SmolStackType

class SmolTryRegionSaveState(SmolStackType):

    code_section:int
    pc:int
    this_env:ScopeEnvironment
    jump_exception:int

    def __init__(self, code_section:int, pc:int, this_env:ScopeEnvironment, jump_exception:int):
        super().__init__()
        self.code_section = code_section
        self.pc = pc
        self.this_env = this_env
        self.jump_exception = jump_exception

    def toString(self):
        return "(SmolTryRegionSaveState)"