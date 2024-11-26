from typing import Any
from internals.variable_types.smol_variable_type import SmolVariable

class SmolNull(SmolVariable):
    
    def __init__(self):
        super().__init__()

    def __str__(self) -> str:
        return f"(Null)"
    
    def getValue(self) -> Any:
        return None