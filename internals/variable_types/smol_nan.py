from internals.variable_types.smol_variable_type import SmolVariableType

class SmolNaN(SmolVariableType):

    def __init__(self):
        pass

    def __str__(self) -> str:
        return f"(NaN)"

    def getValue(self) -> 'SmolNaN':
        return self

    def toString(self) -> str:
        return 'NaN'