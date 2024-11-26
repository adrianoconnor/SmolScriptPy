from .smol_variable_type import SmolVariable

class SmolFunction(SmolVariable):

    global_function_name:str
    code_section:int
    arity:int
    param_variable_names:list[str] = []

    def __init__(self, global_function_name:str, code_section:int, arity:int, param_variable_names:list[str]):
    
        super().__init__()
        self.global_function_name = global_function_name
        self.code_section = code_section
        self.arity = arity
        self.param_variable_names = param_variable_names
    
    def getValue(self):
        return self

    def __str__(self) -> str:
        return f"(SmolFunction) {self.global_function_name}"
