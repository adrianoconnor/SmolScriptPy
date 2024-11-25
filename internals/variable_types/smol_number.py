from internals.variable_types.smol_variable_type import SmolVariable

class SmolNumber(SmolVariable):

    value:float

    def __init__(self, value:float):
        super().__init__()
        self.value = value

    def __str__(self) -> str:
        return f"(Number) {self.value}"
