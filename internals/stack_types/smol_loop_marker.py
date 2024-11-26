from internals.scope_environment import ScopeEnvironment
from .smol_stack_type import SmolStackType

class SmolLoopMarker(SmolStackType):

    current_env:ScopeEnvironment

    def __init__(self, current_env:ScopeEnvironment):
        super().__init__()
        self.current_env = current_env

    def toString(self):
        return "(SmolLoopMarker)"
