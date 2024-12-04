from typing import Dict, Optional
from .variable_types.smol_variable_type import SmolVariableType

class ScopeEnvironment():

    def __init__(self, enclosing:Optional['ScopeEnvironment'] = None):
        self._variables:Dict[str, SmolVariableType] = {}
        self.enclosing:Optional['ScopeEnvironment'] = enclosing

    def define(self, name:str, value:SmolVariableType) -> None:
        #print(f"Define -- name: {name}, value: {value}")
        self._variables[name] = value

    def assign(self, name:str, value:SmolVariableType, isThis:bool = False) -> None:
        #print(f"Assign -- name: {name}, value: {value}")
        if (self._variables.__contains__(name)):
            self._variables[name] = value
        elif (isThis):
            self.define(name, value)
        elif (self.enclosing != None):
            assert self.enclosing
            self.enclosing.assign(name, value)
        else:
            raise RuntimeError("Variable undefined")

    def get(self, name:str) ->  SmolVariableType:
        if (self._variables.__contains__(name)):
            return self._variables[name]
        elif (self.enclosing != None):
            assert self.enclosing
            return self.enclosing.get(name)
        else:
            raise RuntimeError("Variable undefined")

    def tryGet(self, name:str) -> Optional[SmolVariableType]:
        if (self._variables.__contains__(name)):
            return self._variables[name]
        elif (self.enclosing != None):
            assert self.enclosing
            return self.enclosing.tryGet(name)
        else:
            return None