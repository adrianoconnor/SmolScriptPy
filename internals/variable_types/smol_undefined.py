from typing import Any
from internals.variable_types.smol_variable_type import SmolVariableType

class SmolUndefined(SmolVariableType):
    
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return f"(Undefined)"
    
    def getValue(self) -> Any:
        return self