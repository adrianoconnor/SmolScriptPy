from internals.variable_types.smol_variable_type import SmolVariableType

class SmolNumber(SmolVariableType):

    def __init__(self, value:float):
        self.value:float = value

    def __str__(self) -> str:
        return f"(Number) {self.value}"

    def getValue(self) -> float:
        return self.value

    def toString(self) -> str:
        return f'{self.value:g}'