from internals.scope_environment import ScopeEnvironment
from .smol_stack_type import SmolStackType

class SmolLoopMarker(SmolStackType):

    def __init__(self, current_env:ScopeEnvironment):
        self.current_env:ScopeEnvironment = current_env

    def toString(self):
        return "(SmolLoopMarker)"
