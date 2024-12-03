from .smol_variable_type import SmolVariableType

class SmolFunction(SmolVariableType):

    def __init__(self, global_function_name:str, code_section:int, arity:int, param_variable_names:list[str]):
        self.global_function_name:str = global_function_name
        self.code_section:int = code_section
        self.arity:int = arity
        self.param_variable_names:list[str] = param_variable_names
    
    def getValue(self):
        return self

    def __str__(self) -> str:
        return f"(SmolFunction) {self.global_function_name}"
