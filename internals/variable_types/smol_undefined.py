from internals.variable_types.smol_variable_type import SmolVariable

class SmolUndefined(SmolVariable):
    
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return f"(Undefined)"