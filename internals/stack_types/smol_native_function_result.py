from .smol_stack_type import SmolStackType

class SmolNativeFunctionResult(SmolStackType):

    def __init__(self):
        super().__init__()

    def toString(self):
        return "(SmolNativeFunctionResult)"