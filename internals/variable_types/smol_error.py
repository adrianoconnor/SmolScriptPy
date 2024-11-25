from internals.variable_types.smol_variable_type import SmolVariable

class SmolError(SmolVariable):

    message:str

    def __init__(self, message:str):
        super().__init__()
        self.message = message

    def __str__(self) -> str:
        return f"(Error) {self.value}"
