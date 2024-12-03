from internals.variable_types.smol_variable_type import SmolVariableType

class SmolError(SmolVariableType):

    def __init__(self, message:str):
        self.message:str = message

    def __str__(self) -> str:
        return f"(Error) {self.value}"
