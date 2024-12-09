import re
from enum import Enum
from typing import Any, Dict, Optional, Callable
from internals.scope_environment import ScopeEnvironment
from internals.smol_program import SmolProgram
from internals.compiler import Compiler
from internals.opcodes import OpCode
from internals.stack_types.smol_call_site_save_state import SmolCallSiteSaveState
from internals.stack_types.smol_loop_marker import SmolLoopMarker
from internals.stack_types.smol_native_function_result import SmolNativeFunctionResult
from internals.stack_types.smol_try_region_save_state import SmolTryRegionSaveState
from internals.variable_types.smol_error import SmolError
from internals.variable_types.smol_function import SmolFunction
from internals.variable_types.smol_native_callable import ISmolNativeCallable
from internals.variable_types.smol_object import SmolObject
from internals.stack_types.smol_stack_type import SmolStackType
from internals.variable_types.smol_bool import SmolBool
from internals.variable_types.smol_string import SmolString
from internals.variable_types.smol_undefined import SmolUndefined
from internals.variable_types.smol_number import SmolNumber
from internals.variable_types.smol_nan import SmolNaN
from internals.variable_types.smol_variable_type import SmolVariableType
from internals.stack_types.smol_stack_type import SmolStackType
from internals.variable_types.smol_variable_creator import SmolVariableCreator
from internals.variable_types.smol_array import SmolArray

class RunMode(Enum):
    Ready = 0,
    Run = 1,
    Paused = 2,
    Step = 3,
    InstructionStep = 4,
    Done = 5

class SmolThrownFromInstruction(BaseException):

    def __init__(self, *args):
        super().__init__(*args)

class SmolRuntime():

    def __init__(self, source:str):

        self.code_section:int = 0
        self.pc:int = 0
        self.runMode:RunMode = RunMode.Paused
        self.stack:list[SmolStackType] = []
        self.jmplocs:Dict[int, int] = {}
        self.maxStackSize:int = -1
        self.maxCycles:int = -1

        self.globalEnv:ScopeEnvironment = ScopeEnvironment()
        self.environment:ScopeEnvironment
        self.staticTypes:Dict[str, Any] = {} 
        self.externalMethods:Dict[str, Callable] = {} 

        self.classMethodRegEx = "@([A-Za-z]+)[.]([A-Za-z]+)"

        self.program:SmolProgram = Compiler.compile(source)

        self.environment = self.globalEnv

        self.createStdLib()
        self.buildJumpTable()

        self.runMode = RunMode.Ready
    

    @staticmethod
    def create(source:str, initialize:bool = False) -> 'SmolRuntime': 
        vm = SmolRuntime(source)
        if (initialize):
            vm.run()
        return vm

    def get_variable(self, variable_name):
        if variable_name in self.environment._variables:
            smol_var = self.environment._variables[variable_name]
            assert isinstance(smol_var, SmolVariableType)
            return smol_var.getValue()
        else:
            return None

    def buildJumpTable(self):
    
        # Loop through all labels in all code sections, capturing
        # the label number (always unique) and the location/index
        # in the instructions for that section so we can jump
        # if we need to.

        for i in range(self.program.code_sections.__len__()):
        
            # Not sure if this will hold up, might be too simplistic
            for j in range(self.program.code_sections[i].__len__()):
            
                instr = self.program.code_sections[i][j]

                if (instr.opcode == OpCode.LABEL):
                
                    assert instr.operand1 != None
                    # We're not storing anything about the section
                    # number but this should be ok becuase we should
                    # only ever jump inside the current section...
                    # Jumps to other sections are handled in a different
                    # way using the CALL instruction
                    self.jmplocs[int(str(instr.operand1))] = j
        
        #print (f"jmplocs: {self.jmplocs}")
                
    

    def createStdLib(self): 
    #    pass
    #    self.staticTypes['Object'] = SmolObject
    #    self.staticTypes['String'] = SmolString
        self.staticTypes["Array"] = SmolArray
    #    self.staticTypes['RegExp'] = SmolRegExp
    
    #def registerMethod(methodName:str, closure:Function):
        # console.log(`type = $typeof closure`) # function
        # self.externalMethods[methodName] = closure
    
    def callExternalMethod(self, methodName:str, numberOfPassedArgs:int): 

        methodArgs:list[Any] = []
        
        for i in range(numberOfPassedArgs):
            value = self.stack.pop()
            assert isinstance(value, SmolVariableType)
            methodArgs.append(value.getValue())

        # returnValue = self.externalMethods[methodName].apply(None, methodArgs)
        returnValue = None

        if (returnValue == None):
            return SmolUndefined()
        else:
            return SmolVariableCreator(returnValue)

    def call(self, functionName:str, *args:list[Any]) -> Any:
        if (self.runMode != RunMode.Done):
            raise RuntimeError("Init() should be used before calling a function, to ensure the vm state is prepared")
        
        # Let the VM know that it's ok to proceed from wherever the PC was pointing next
        self.runMode = RunMode.Paused

        # Store the current state. This doesn't matter too much, because it shouldn't really
        # be runnable after we're done, but it doesn't hurt to do this.
        state = SmolCallSiteSaveState(self.code_section, self.pc, self.environment, True)

        # Create an environment for the function
        env = ScopeEnvironment(self.globalEnv)
        self.environment = env

        fnIndex = -1

        for i in range(self.program.function_table.__len__()):
            if (self.program.function_table[i].global_function_name == functionName):
                fnIndex = i
                break

        if (fnIndex == -1):
            raise RuntimeError(f"Could not find a function named '{functionName}'")

        fn = self.program.function_table[i]

        # Prime the environment with variables for
        # the parameters in the function declaration (actual number
        # passed might be different)
        for i in range(fn.arity):
            if (args.__len__() > i):
                env.define(fn.param_variable_names[i], SmolVariableCreator(args[i]))
            else:
                env.define(fn.param_variable_names[i], SmolUndefined())
            
        self.stack.append(state)

        self.pc = 0
        self.code_section = fn.code_section

        self.run()

        returnValue = self.stack.pop()

        assert isinstance(returnValue, SmolVariableType) 
        return returnValue.getValue()

    def run(self) -> None:
        if (self.runMode == RunMode.Ready or self.runMode == RunMode.Paused): 
            self._run(RunMode.Run)
        
    def getCurrentRunMode(self) -> RunMode: 
        return self.runMode
    
    def step(self, vmInstrStep:bool = False) -> None: 
        if (self.runMode == RunMode.Ready or self.runMode == RunMode.Paused): 
            self._run(RunMode.InstructionStep if vmInstrStep else RunMode.Step)
        
    def _run(self, newRunMode:RunMode) -> None:
    
        self.runMode = newRunMode
        hasExecutedAtLeastOnce = False # Used to ensure Step-through trips after at least one instruction is executed
        consumedCycles = 0

        while (self.runMode == RunMode.Run or self.runMode == RunMode.Step or self.runMode == RunMode.InstructionStep):
           
            if (self.runMode == RunMode.Step and self.code_section == 0 and self.program.code_sections[0].__len__() < (self.pc - 1)):
                self.runMode = RunMode.Done
                return
                 
            # Peek at the next instruction to execute and see if it's a step break point
            elif (self.runMode == RunMode.Step
                    and self.program.code_sections[self.code_section][self.pc].isStatementStartpoint
                    and hasExecutedAtLeastOnce):
            
                self.runMode = RunMode.Paused
                return
            
            elif (self.runMode == RunMode.InstructionStep and hasExecutedAtLeastOnce):
                self.runMode = RunMode.Paused
                return
            
            # Fetch the next instruciton and advance the program counter
            instr = self.program.code_sections[self.code_section][self.pc]

            self.pc += 1

            # For debug...
            #print ("=+=+=+=+=+=+=")
            #print (self.stack)
            #print (instr)
            #print (f"op1: {instr.operand1}, op2: {instr.operand2}")

            try:
                match (instr.opcode):
                
                    case OpCode.NOP:
                        True
                     
                    case OpCode.START:
                        # Just skip over this instruction, no-op
                        True

                    case OpCode.CONST:
                        # Load a value from the program constants at specified index (op1) and place it on the stack
                        assert instr.operand1 != None
                        self.stack.append(self.program.constants[int(str(instr.operand1))])
        
                    case OpCode.CALL:
                        
                        callData = self.stack.pop()
                        
                        # If we've got a SmolNativeFunctionResult, then we know that the FETCH that
                        # previously executed for this function handled the actual function call
                        # and left the result on the stack, so we don't have anything to do here.
                        if (not isinstance(callData, SmolNativeFunctionResult)):
                            
                            assert isinstance(callData, SmolFunction)

                            # First create the env for our function

                            env = ScopeEnvironment(self.globalEnv)

                            if (isinstance(instr.operand2, bool) and instr.operand2 == True):
                            
                                # If op2 is true, that means we're calling a method
                                # on an object/class, so we need to get the objref
                                # (from the next value on the stack) and use that
                                # objects environment instead.

                                obj = self.stack.pop()
                                assert isinstance(obj, SmolObject)
                                env = (obj).object_env

                            # Next pop args off the stack. Op1 is number of args.                    

                            paramValues:list[SmolVariableType] = []

                            assert instr.operand1 != None

                            for i in range(int(str(instr.operand1))):
                                paramValue = self.stack.pop()
                                assert isinstance(paramValue, SmolVariableType)
                                paramValues.append(paramValue)

                            # Now prime the environment with variables for
                            # the parameters in the function declaration (actual number
                            # passed might be different)

                    
                            
                            for i in range(callData.arity):
                                if (paramValues.__len__() > i):
                                    env.define(callData.param_variable_names[i], paramValues[i])
                                else:                            
                                    env.define(callData.param_variable_names[i], SmolUndefined())

                            # Store our current program/vm state so we can restor

                            state = SmolCallSiteSaveState(
                                self.code_section,
                                self.pc,
                                self.environment,
                                False # call is extern
                            )

                            # Switch the active env in the vm over to the one we prepared for the call

                            self.environment = env

                            self.stack.append(state)

                            # Finally set our PC to the start of the function we're about to execute

                            self.pc = 0
                            self.code_section = callData.code_section
                    
                    case OpCode.ADD:
                        
                        right = self.stack.pop()
                        left = self.stack.pop()

                        assert isinstance(left, SmolVariableType)
                        assert isinstance(right, SmolVariableType)

                        if (isinstance(left, SmolNumber) and isinstance(right, SmolNumber)):
                            self.stack.append(SmolNumber(left.getValue() + right.getValue()))
                        else :                            
                            self.stack.append(SmolString(left.toString() + right.toString()))
                        
                    case OpCode.SUB:
                        
                        right = self.stack.pop()
                        left = self.stack.pop()

                        if isinstance(left, SmolNumber) and isinstance(right, SmolNumber):
                            assert isinstance(left, SmolNumber)
                            assert isinstance(right, SmolNumber)
     
                            self.stack.append(SmolNumber(left.getValue() - right.getValue()))
                        else:
                            self.stack.append(SmolNaN())

                    case OpCode.MUL:
                        
                        right = self.stack.pop()
                        left = self.stack.pop()

                        if isinstance(left, SmolNumber) and isinstance(right, SmolNumber):
                            assert isinstance(left, SmolNumber)
                            assert isinstance(right, SmolNumber)
                            
                            self.stack.append(SmolNumber(left.getValue() * right.getValue()))
                        else:
                            self.stack.append(SmolNaN())

                    case OpCode.DIV:
                        
                        right = self.stack.pop()
                        left = self.stack.pop()

                        if isinstance(left, SmolNumber) and isinstance(right, SmolNumber):
                            assert isinstance(left, SmolNumber)
                            assert isinstance(right, SmolNumber)
                            
                            self.stack.append(SmolNumber(left.getValue() / right.getValue()))
                        else:
                            self.stack.append(SmolNaN())

                    case OpCode.REM:
                        
                        right = self.stack.pop()
                        left = self.stack.pop()

                        if isinstance(left, SmolNumber) and isinstance(right, SmolNumber):
                            assert isinstance(left, SmolNumber)
                            assert isinstance(right, SmolNumber)
                            
                            self.stack.append(SmolNumber(left.getValue() % right.getValue()))
                        else:
                            self.stack.append(SmolNaN())

                    case OpCode.POW:
                        
                        right = self.stack.pop()
                        left = self.stack.pop()

                        if isinstance(left, SmolNumber) and isinstance(right, SmolNumber):
                            assert isinstance(left, SmolNumber)
                            assert isinstance(right, SmolNumber)
                            
                            self.stack.append(SmolNumber(left.getValue() ** right.getValue()))
                        else:
                            self.stack.append(SmolNaN())

                    case OpCode.EQL:
                        
                        right = self.stack.pop()
                        left = self.stack.pop()

                        assert isinstance(left, SmolVariableType)
                        assert isinstance(right, SmolVariableType)

                        self.stack.append(SmolBool(left.equals(right)))

                    case OpCode.NEQ:
                        
                        right = self.stack.pop()
                        left = self.stack.pop()

                        assert isinstance(left, SmolVariableType)
                        assert isinstance(right, SmolVariableType)

                        self.stack.append(SmolBool(not left.equals(right)))

                    case OpCode.GT:
                        
                        right = self.stack.pop()
                        left = self.stack.pop()
                        
                        assert isinstance(left, SmolVariableType)
                        assert isinstance(right, SmolVariableType)

                        self.stack.append(SmolBool(left.getValue() > right.getValue()))

                    case OpCode.LT:
                        
                        right = self.stack.pop()
                        left = self.stack.pop()

                        assert isinstance(left, SmolVariableType)
                        assert isinstance(right, SmolVariableType)

                        self.stack.append(SmolBool(left.getValue() < right.getValue()))

                    case OpCode.GTE:
                        
                        right = self.stack.pop()
                        left = self.stack.pop()

                        assert isinstance(left, SmolVariableType)
                        assert isinstance(right, SmolVariableType)

                        self.stack.append(SmolBool(left.getValue() >= right.getValue()))

                    case OpCode.LTE:
                        
                        right = self.stack.pop()
                        left = self.stack.pop()

                        assert isinstance(left, SmolVariableType)
                        assert isinstance(right, SmolVariableType)

                        self.stack.append(SmolBool(left.getValue() <= right.getValue()))

                    case OpCode.BITWISE_OR:
                        
                        right = self.stack.pop()
                        left = self.stack.pop()

                        assert isinstance(left, SmolVariableType)
                        assert isinstance(right, SmolVariableType)

                        self.stack.append(SmolNumber(left.getValue() | right.getValue()))

                    case OpCode.BITWISE_AND:
                        
                        right = self.stack.pop()
                        left = self.stack.pop()

                        assert isinstance(left, SmolVariableType)
                        assert isinstance(right, SmolVariableType)

                        self.stack.append(SmolNumber(left.getValue() & right.getValue()))

                    case OpCode.EOF:
                        
                        #console.log(`Done, stack size = $self.stack.__len__(), consumed cycles = $consumedCycles`)
                        self.runMode = RunMode.Done
                        self.pc -= 1

                    case OpCode.RETURN:
                        
                        # Return to the previous code section, putting
                        # a return value on the stack and restoring the PC

                        # Top value on the stack is the return value

                        return_value = self.stack.pop()

                        # Next value should be the original pre-call state that we saved

                        _savedCallState = self.stack.pop()

                        if (not(isinstance(_savedCallState, SmolCallSiteSaveState))):
                            raise RuntimeError("Tried to return but found something unexecpted on the stack")
                        
                        savedCallState = _savedCallState

                        self.environment = savedCallState.previous_env
                        self.pc = savedCallState.pc
                        self.code_section = savedCallState.code_section

                        # Return value needs to go back on the stack
                        self.stack.append(SmolUndefined() if return_value == None else return_value)

                        if (savedCallState.call_is_extern):
                        
                            # Not sure what to do about return value here

                            self.runMode = RunMode.Paused
                            return # Don't like this, error prone
                    
                        if (self.runMode == RunMode.Step):    
                            self.runMode = RunMode.Paused
                            return
                        
                    case OpCode.DECLARE:
                        self.environment.define(str(instr.operand1), SmolUndefined())

                    case OpCode.STORE:
                    
                        name = str(instr.operand1)

                        if (name == "@IndexerSet"):
                        
                            # Special case for square brackets!

                            # Not sure about this cast, might need to add an extra check for type
                            indexer_name_variable = self.stack.pop()
                            assert isinstance(indexer_name_variable, SmolVariableType)
                            name = indexer_name_variable.getValue()
                        

                        value = self.stack.pop() # Hopefully always true...
                        
                        assert isinstance(value, SmolVariableType)
                        
                        env_in_context = self.environment
                        isPropertySetter = False

                        if (instr.operand2 != None and bool(instr.operand2)):
                        
                            objRef = self.stack.pop()

                            isPropertySetter = True

                            if (isinstance(objRef, SmolObject)):
                            
                                env_in_context = (objRef).object_env
                            
                            elif (isinstance(objRef, ISmolNativeCallable)):
                            
                                (objRef).setProp(name, value)
                            
                            else:                            
                                raise RuntimeError(f"$objRef is not a valid target for this call")

                        assert isinstance(value, SmolVariableType)    
                        env_in_context.assign(name, value, isPropertySetter)                    

                    case OpCode.FETCH:
                        
                        # Could be a variable or a function
                        name = str(instr.operand1)
                        env_in_context = self.environment

                        # Small hacky variable because Python's match doesn't support break, unlike switch in JS/C#
                        break_fetch_early = False


                        # WARNING -- Difference heere between .net and ts versions and I can't remember why .net was changed :(
                        # TODO: Check why the difference and fix...           
                        if (name == "@IndexerGet" or name == "@IndexerSet"):
                        
                            # Special case for square brackets!
                            indexer_name_variable = self.stack.pop()
                            assert isinstance(indexer_name_variable, SmolVariableType)
                            indexer_name_value = indexer_name_variable.getValue()

                            if (isinstance(indexer_name_value, float)):
                                name = int(indexer_name_value).__str__()
                            else:
                                name = indexer_name_value.__str__() #.toString()
                        

                        if (instr.operand2 != None and bool(instr.operand2)):
                    
                            objRef = self.stack.pop()
                            peek_instr = self.program.code_sections[self.code_section][self.pc]
                           
                            if (isinstance(objRef, SmolObject)):
                            
                                env_in_context = (objRef).object_env

                                if (peek_instr.opcode == OpCode.CALL and bool(peek_instr.operand2)):
                                    self.stack.append(objRef)
                            else:
                                
                                if (isinstance(objRef, ISmolNativeCallable)):
                                    
                                    isFuncCall = (peek_instr.opcode == OpCode.CALL and peek_instr.operand2)
                                    if (isFuncCall):
                                    
                                        # We need to get some arguments

                                        fetchFuncCallParamValues:list[SmolVariableType] = []

                                        assert peek_instr.operand1 != None

                                        for i in range(int(str(peek_instr.operand1))):
                                            value_to_push = self.stack.pop()
                                            assert isinstance(value_to_push, SmolVariableType)
                                            fetchFuncCallParamValues.append(value_to_push)
                                        
                                        self.stack.append(objRef.nativeCall(name, fetchFuncCallParamValues))
                                        self.stack.append(SmolNativeFunctionResult()) # Call will use this to see that the call is already done.
                                        break_fetch_early = True

                                    else:                                    
                                        # For now won't work with Setter
                                        self.stack.append((objRef).getProp(name))
                                        break_fetch_early = True
                                    
                                
                                elif (isinstance(objRef, SmolNativeFunctionResult)):

                                    if (re.match(self.classMethodRegEx, name) != None):

                                        print(self.classMethodRegEx)             
                                        print(name)
                                        rexResult = re.match(self.classMethodRegEx, name)
                                        print(rexResult.groups())

                                        #if (rexResult == None):
                                        #    raise RuntimeError("class method name regex failed")
                                        

                                        # TODO: Document why this is any and why the first
                                        # value is the regex second group match
                                        #parameters:any[] = [rexResult[2]]
                                        assert rexResult != None
                                        functionName = str(rexResult.groups()[1])

                                        functionArgs:list[SmolVariableType] = []

                                        if (name != "@Object.constructor"):                                            
                                            
                                            assert peek_instr.operand1 != None

                                            for i in range(int(str(peek_instr.operand1))):
                                                value_to_pass = self.stack.pop()
                                                assert isinstance(value_to_pass, SmolVariableType)
                                                functionArgs.append(value_to_pass)
                                            
                                        # Now we've got rid of the params we can get rid
                                        # of the dummy object that create_object left
                                        # on the stack

                                        self.stack.pop()

                                        # Put our actual object on after calling the ctor:                                            
                                        r = self.staticTypes[rexResult.groups()[0]].staticCall(functionName, functionArgs)
                                    
                                        if (name == "@Object.constructor"):
                                        
                                            # Hack alert!!!
                                            (r).object_env = ScopeEnvironment(self.globalEnv)
                                        

                                        self.stack.append(r)

                                        # And now fill in some fake object refs again:
                                        self.stack.append(SmolNativeFunctionResult()) # Call will use this to see that the call is already done.
                                        self.stack.append(SmolNativeFunctionResult()) # Pop and Discard following Call will discard this

                                        break_fetch_early = True
                                else:
                                    raise RuntimeError(f"{objRef} is not a valid target for this call")
                        
                        if (not break_fetch_early):
                            fetchedValue = env_in_context.tryGet(name)

                            if (isinstance(fetchedValue, SmolFunction)):
                                assert isinstance(fetchedValue, SmolFunction)
                        
                            if (fetchedValue != None):
                                assert isinstance(fetchedValue, SmolVariableType)               
                                self.stack.append(fetchedValue)

                            else:
                            
                                fn = None
                                for f in self.program.function_table:
                                    if (f.global_function_name == name):
                                        fn = f
                                        break
                                
                                if (fn != None):
                                    assert isinstance(fn, SmolStackType)
                                    self.stack.append(fn)
                                
                                elif (name in self.externalMethods):
                                    peek_instr = self.program.code_sections[self.code_section][self.pc]

                                    self.stack.append(self.callExternalMethod(name, int(str(peek_instr.operand1))))

                                    self.stack.append(SmolNativeFunctionResult())
                                else:
                                    self.stack.append(SmolUndefined())

                    case OpCode.JMPFALSE:
                        
                        value = self.stack.pop()
                        assert isinstance(value, SmolVariableType)
                        
                        if (value.getValue() == False): # .isFalsey())
                            assert isinstance(instr.operand1, int) 
                            self.pc = self.jmplocs[instr.operand1]
                        
                    case OpCode.JMPTRUE:
                    
                        #.IsTruthy())
                        value = self.stack.pop()
                        assert isinstance(value, SmolVariableType)

                        if (value.getValue() == True): # .isFalsey())
                            assert isinstance(instr.operand1, int) 
                            self.pc = self.jmplocs[instr.operand1]

                    case OpCode.JMP:
                        self.pc = self.jmplocs[instr.operand1]

                    case OpCode.LABEL:
                        # Just skip over this instruction, it's only here
                        # to support branching
                        True

                    case OpCode.ENTER_SCOPE:
                        
                        self.environment = ScopeEnvironment(self.environment)
                        
                    case OpCode.LEAVE_SCOPE:
                    
                        self.environment = self.environment.enclosing

                    case OpCode.DEBUGGER:
                        
                        if (hasExecutedAtLeastOnce):
                            # Don't break if we're starting from a prevoiusly hit break point
                            self.runMode = RunMode.Paused
                            return
                        
                    case OpCode.POP_AND_DISCARD:
                        # operand1 is optional bool, default true means fail if nothing to pop
                        if (self.stack.__len__() > 0 or instr.operand1 == None or bool(instr.operand1)):
                        
                            self.stack.pop()

                    case OpCode.TRY:

                        exception:Optional[SmolVariableType]

                        if (instr.operand2 != None and bool(instr.operand2)):
                        
                            # This is a special flag for the try instruction that tells us to
                            # take the exception that's already on the stack and leave it at the
                            # top after creating the try checkpoint.

                            exception = self.stack.pop()
                        

                        self.stack.append(SmolTryRegionSaveState(
                                self.code_section,
                                self.pc,
                                self.environment,
                                self.jmplocs[instr.operand1]
                            )
                        )

                        if (exception != None):
                            self.stack.append(exception)

                    case OpCode.THROW:
                                            
                        raise SmolThrownFromInstruction()                 
                        
                    case OpCode.LOOP_START:

                        self.stack.append(SmolLoopMarker(self.environment))

                    case OpCode.LOOP_END:

                        self.stack.pop()

                    case OpCode.LOOP_EXIT:

                        while (self.stack.__len__() > 0):
                        
                            next = self.stack.pop()

                            if (isinstance(next, SmolLoopMarker)):
                            
                                self.environment = (next).current_env

                                self.stack.append(next) # Needs to still be on the stack

                                if (instr.operand1 != None):
                                    self.pc = self.jmplocs[instr.operand1]
                                
                                break

                    case OpCode.CREATE_OBJECT:
                        
                        # Create a environment and store it as an instance/ref variable
                        # For now we'll just have it 'inherit' the global env, but scope is
                        # a thing we need to think about, but I'll work out how JS does it
                        # first and try and do the same (I think class hierarchies all share
                        # a single env?!

                        class_name = str(instr.operand1)

                        if (class_name in self.staticTypes):
                            self.stack.append(SmolNativeFunctionResult())
                        else:
                            obj_environment = ScopeEnvironment(self.globalEnv)
                            
                            for fn in self.program.function_table:
                                #.filter((el) => el.global_function_name.startsWith(`@$class_name.`)).forEach(classFunc => 

                                if (fn.global_function_name.startswith("@$class_name.")):

                                    funcName = fn.global_function_name.substring(class_name.__len__() + 2)

                                    obj_environment.define(funcName, SmolFunction(
                                        fn.global_function_name,
                                        fn.code_section,
                                        fn.arity,
                                        fn.param_variable_names
                                    ))                        

                            new_object = SmolObject(obj_environment, class_name)
                            self.stack.append(new_object)

                            obj_environment.define("this", new_object)

                    case OpCode.DUPLICATE_VALUE:
                    
                        skip = int(str(instr.operand1)) if instr.operand1 != None else 0

                        itemToDuplicate = self.stack[self.stack.__len__() - 1 - skip]

                        self.stack.append(itemToDuplicate)
                                            
                    case default:
                        raise RuntimeError(f"You forgot to handle an opcode: {instr.opcode}")
                
            except Exception as e:
                
                handled = False
                throwObject:SmolVariableType = SmolError(e)
                
                if (isinstance(e, SmolThrownFromInstruction)): 
                    thrownObject = self.stack.pop()
                    throwObject = thrownObject
                

                while (self.stack.__len__() > 0):
                
                    next = self.stack.pop()

                    if (isinstance(next, SmolTryRegionSaveState)):
                    
                        # We found the start of a try section, restore our state and jump to the exception handler location

                        tryState = next

                        self.code_section = tryState.code_section
                        self.pc = tryState.jump_exception
                        self.environment = tryState.this_env

                        self.stack.append(throwObject)

                        handled = True
                        break
                
                if (not handled):
                    raise e
            
            if (self.maxStackSize > -1 and self.stack.__len__() > self.maxStackSize):
                raise RuntimeError("Stack overflow")

            hasExecutedAtLeastOnce = True

            consumedCycles += 1

            if (self.maxCycles > -1 and consumedCycles > self.maxCycles):
                raise RuntimeError("Too many cycles")
