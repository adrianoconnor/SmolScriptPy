from internals.scope_environment import ScopeEnvironment
from .smol_stack_type import SmolStackType

class SmolTryRegionSaveState(SmolStackType):

    def __init__(self, code_section:int, pc:int, this_env:ScopeEnvironment, jump_exception:int):
        self.code_section:int = code_section
        self.pc:int = pc
        self.this_env:ScopeEnvironment = this_env
        self.jump_exception:int = jump_exception

    def toString(self):
        return "(SmolTryRegionSaveState)"