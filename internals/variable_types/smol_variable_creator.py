from typing import Any

from .smol_bool import SmolBool
from .smol_number import SmolNumber
from .smol_string import SmolString
from .smol_variable_type import SmolVariable
from .smol_null import SmolNull

def SmolVariableCreator(value:Any) -> SmolVariable:
   
    if (value == None):
        return SmolNull()
    elif (isinstance(value, SmolVariable)):
        return value
    elif (isinstance(value, str)):
        return SmolString(value)
    elif (isinstance(value, float)):
        return SmolNumber(value)
    elif (isinstance(value, bool)):
        return SmolBool(value)
    
    raise RuntimeError()