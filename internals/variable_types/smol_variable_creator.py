from typing import Any

from .smol_bool import SmolBool
from .smol_number import SmolNumber
from .smol_string import SmolString
from .smol_variable_type import SmolVariableType
from .smol_null import SmolNull

def SmolVariableCreator(value:Any) -> SmolVariableType:
   
    if (value == None):
        return SmolNull()
    elif (isinstance(value, SmolVariableType)):
        return value
    elif (isinstance(value, str)):
        return SmolString(value)
    elif (isinstance(value, float)):
        return SmolNumber(value)
    elif (isinstance(value, int)):
        return SmolNumber(float(value))
    elif (isinstance(value, bool)):
        return SmolBool(value)
    
    raise RuntimeError()