from internals.scope_environment import ScopeEnvironment
from internals.variable_types.smol_variable_type import SmolVariable


class SmolObject(SmolVariable):
    
    object_env:ScopeEnvironment
    class_name:str

    def __init__(self, object_env:ScopeEnvironment, class_name:str):
        super().__init__()
        self.object_env = object_env
        self.class_name = class_name

    def getValue(self):
        return self

    def toString(self):
        if (self.class_name != ''):
            return f"(SmolInstance, class_name = {self.class_name})"
        else:
            return "(SmolObject)"

    def getProp(self, propName:str) -> SmolVariable:
        match (propName):
            case default:
                raise RuntimeError(f"{self} cannot handle native property ${propName}");

    def setProp(self, propName:str, value:SmolVariable):    
        raise RuntimeError("Not a valid target")
    
    def nativeCall(funcName:str, parameters:list[SmolVariable]) -> SmolVariable:
        match (funcName):
            case default:
                raise RuntimeError(f"Object cannot handle native function ${funcName}")

    @staticmethod
    def staticCall(funcName:str , parameters:list[SmolVariable]) -> SmolVariable:
        match (funcName):
 
            case "constructor":
                return SmolObject(ScopeEnvironment(), "Object")

            case default:
                raise RuntimeError(f"Object class cannot handle static function {funcName}")