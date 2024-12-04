from internals.scope_environment import ScopeEnvironment
from internals.variable_types.smol_variable_type import SmolVariableType

class SmolObject(SmolVariableType):

    def __init__(self, object_env:ScopeEnvironment, class_name:str):
        self.object_env:ScopeEnvironment = object_env
        self.class_name:str = class_name

    def getValue(self):
        return self

    def toString(self):
        if (self.class_name != ''):
            return f"(SmolInstance, class_name = {self.class_name})"
        else:
            return "(SmolObject)"

    def getProp(self, propName:str) -> SmolVariableType:
        match (propName):
            case default:
                raise RuntimeError(f"{self} cannot handle native property ${propName}");

    def setProp(self, propName:str, value:SmolVariableType):    
        raise RuntimeError("Not a valid target")
    
    def nativeCall(self, funcName:str, parameters:list[SmolVariableType]) -> SmolVariableType:
        match (funcName):
            case default:
                raise RuntimeError(f"Object cannot handle native function ${funcName}")

    @staticmethod
    def staticCall(funcName:str , parameters:list[SmolVariableType]) -> SmolVariableType:
        match (funcName):
 
            case "constructor":
                return SmolObject(ScopeEnvironment(), "Object")

            case default:
                raise RuntimeError(f"Object class cannot handle static function {funcName}")