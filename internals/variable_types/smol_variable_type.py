from typing import Any
from internals.stack_types.smol_stack_type import SmolStackType

class SmolVariable(SmolStackType):
    def __init__(self):
        return
    
    def getValue(self) -> Any:
        raise RuntimeError()

    def equals(self, compareTo) -> bool:
        return (self.getValue() == compareTo.getValue())
