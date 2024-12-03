from typing import Dict, Optional
from .variable_types.smol_variable_type import SmolVariable
from .token_types import TokenType

class ScopeEnvironment():

    enclosing:Optional['ScopeEnvironment'] = None
    _variables: Dict[str, TokenType] = {}

    def __init__(self, enclosing:Optional['ScopeEnvironment'] = None):
        self._variables = {}
        self.enclosing = enclosing

    def define(self, name:str, value:SmolVariable) -> None:
        #print(f"Define -- name: {name}, value: {value}")
        self._variables[name] = value

    def assign(self, name:str, value:SmolVariable, isThis:bool = False) -> None:
        #print(f"Assign -- name: {name}, value: {value}")
        if (self._variables.__contains__(name)):
            self._variables[name] = value
        elif (isThis):
            self.define(name, value)
        elif (self.enclosing != None):
            self.enclosing.assign(name, value)
        else:
            raise RuntimeError("Variable undefined")

    def get(self, name:str) ->  SmolVariable:
        if (self._variables.__contains__(name)):
            return self._variables[name]
        elif (self.enclosing != None):
            return self.enclosing.get(name)
        else:
            raise RuntimeError("Variable undefined")

    def tryGet(self, name:str) -> Optional[SmolVariable]:
        if (self._variables.__contains__(name)):
            return self._variables[name]
        elif (self.enclosing != None):
            return self.enclosing.tryGet(name)
        else:
            return None