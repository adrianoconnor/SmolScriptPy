from internals.variable_types.smol_variable_type import SmolVariableType
from internals.variable_types.smol_native_callable import ISmolNativeCallable
from internals.variable_types.smol_number import SmolNumber


class SmolArray(ISmolNativeCallable):

    def __init__(self):
        self.array:list[SmolVariableType] = []

    def getValue(self) -> SmolVariableType:
        return self

    def __str__(self):
        return f"(SmolArray, length = {self.array.__len__()})"

    def toString(self):
        return f"(SmolArray, length = {self.array.__len__()})"
    

    def getProp(self, propName:str) -> SmolVariableType:
    
        match (propName):
        
            case "length":
                return SmolNumber(self.array.__len__())

            case default:
                #if (String(propName).match(/[0-9]+/)):
                return self.array[int(propName)] # ?? new SmolUndefined();

                #raise Runtime(f"Array does not contain property ${propName}")

    def setProp(self, propName:str, value:SmolVariableType) -> None:

        #if (String(propName).match(/[0-9]+/))
        
        index = int(propName)

        self.array[index] = value
        
        #else:
        #    throw new Error("Not a valid index")
        
    def nativeCall(self, funcName:str, parameters:list[SmolVariableType]) -> SmolVariableType:

        match (funcName):
            case 'pop':
                val = self.array.pop()
                return val # != None ? val : new SmolUndefined();
            
            case 'push':
                self.array.append(parameters[0])
                return SmolNumber(self.array.__len__())

            case default:
                raise RuntimeError(f"Array cannot handle native function ${funcName}")

    @staticmethod
    def staticCall(funcName:str, parameters:list[SmolVariableType]) -> SmolVariableType:
    
        match (funcName):
        
            case 'constructor':
                new_object = SmolArray()
    
                for p in parameters:
                    new_object.array.append(p)

                return new_object

            case default:
                raise RuntimeError(f"Array class cannot handle static function '{funcName}'");