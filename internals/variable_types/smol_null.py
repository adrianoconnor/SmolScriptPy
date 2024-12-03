from typing import Any
from internals.variable_types.smol_variable_type import SmolVariableType

class SmolNull(SmolVariableType):
    
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return f"(Null)"
    
    def getValue(self) -> Any:
        return None