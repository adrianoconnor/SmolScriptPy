from internals.scope_environment import ScopeEnvironment
from .smol_stack_type import SmolStackType

class SmolCallSiteSaveState(SmolStackType):

    def __init__(self, code_section:int, pc:int, previous_env:ScopeEnvironment, call_is_extern:bool):

        self.code_section:int = code_section
        self.pc:int = pc
        self.previous_env:ScopeEnvironment = previous_env
        self.call_is_extern:bool = call_is_extern

    def toString(self):
        return "(SmolCallSiteSaveState)"