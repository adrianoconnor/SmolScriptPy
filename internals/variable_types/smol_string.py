from internals.variable_types.smol_variable_type import SmolVariableType

class SmolString(SmolVariableType):

    def __init__(self, value:str):
        self.value:str = value

    def __str__(self) -> str:
        return f"(String) {self.value}"

    def getValue(self) -> str:
        return self.value
    
    def toString(self) -> str:
        return self.value