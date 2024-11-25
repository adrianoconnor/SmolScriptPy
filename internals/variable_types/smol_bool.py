from internals.variable_types.smol_variable_type import SmolVariable

class SmolBool(SmolVariable):

    value:bool

    def __init__(self, value:bool):
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return f"(Bool) {self.value}"
