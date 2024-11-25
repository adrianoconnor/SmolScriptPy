from typing import Any
from compiler_error import SmolCompilerError

class Expression():
    def __init__(self):
        return
    
    def accept(self, visitor:Any) -> Any:
        raise SmolCompilerError("Not supposed to call this on the base class...")