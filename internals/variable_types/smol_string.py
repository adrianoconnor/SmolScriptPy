from internals.variable_types.smol_variable_type import SmolVariable

class SmolString(SmolVariable):

    value:str

    def __init__(self, value:str):
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return f"(String) {self.value}"
