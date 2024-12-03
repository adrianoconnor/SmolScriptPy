from internals.variable_types.smol_variable_type import SmolVariableType

class SmolBool(SmolVariableType):

    def __init__(self, value:bool):
        self.value:bool = value

    def __str__(self) -> str:
        return f"(Bool) {self.value}"

    def getValue(self) -> bool:
        return self.value