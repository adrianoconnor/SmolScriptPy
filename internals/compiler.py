from compiler_error import SmolCompilerError
from internals.bytecode_instruction import ByteCodeInstruction
from internals.opcodes import OpCode
from internals.parser import Parser
from typing import Any, Optional, cast
from compiler_error import SmolCompilerError
from internals.ast.expressions.assign import AssignExpression
from internals.ast.expressions.binary import BinaryExpression
from internals.ast.expressions.call import CallExpression
from internals.ast.expressions.expression import Expression
from internals.ast.expressions.function import FunctionExpression
from internals.ast.expressions.get import GetExpression
from internals.ast.expressions.grouping import GroupingExpression
from internals.ast.expressions.indexer_get import IndexerGetExpression
from internals.ast.expressions.indexer_set import IndexerSetExpression
from internals.ast.expressions.literal import LiteralExpression
from internals.ast.expressions.logical import LogicalExpression
from internals.ast.expressions.new_instance import NewInstanceExpression
from internals.ast.expressions.object_intializer import ObjectInitializerExpression
from internals.ast.expressions.set import SetExpression
from internals.ast.expressions.ternary import TernaryExpression
from internals.ast.expressions.unary import UnaryExpression
from internals.ast.expressions.variable import VariableExpression
from internals.ast.statements.block_statement import BlockStatement
from internals.ast.statements.break_statement import BreakStatement
from internals.ast.statements.class_statement import ClassStatement
from internals.ast.statements.continue_statement import ContinueStatement
from internals.ast.statements.debugger_statement import DebuggerStatement
from internals.ast.statements.expression_statement import ExpressionStatement
from internals.ast.statements.function_statement import FunctionStatement
from internals.ast.statements.if_statement import IfStatement
from internals.ast.statements.return_statement import ReturnStatement
from internals.ast.statements.statement import Statement
from internals.ast.statements.throw_statement import ThrowStatement
from internals.ast.statements.try_statement import TryStatement
from internals.ast.statements.var_statement import VarStatement
from internals.ast.statements.while_statement import WhileStatement
from internals.scanner import Scanner
from internals.smol_program import SmolProgram
from internals.variable_types.smol_bool import SmolBool
from internals.variable_types.smol_function import SmolFunction
from internals.variable_types.smol_null import SmolNull
from internals.variable_types.smol_number import SmolNumber
from internals.variable_types.smol_string import SmolString
from internals.variable_types.smol_undefined import SmolUndefined
from internals.variable_types.smol_variable_type import SmolVariable
from .token_types import TokenType
from .token import Token

class WhileLoop:
    startOfLoop:int
    endOfLoop:int

    def __init__(self, startOfLoop:int, endOfLoop:int):
        self.startOfLoop = startOfLoop
        self.endOfLoop = endOfLoop
    
class Compiler:
    _function_table:list[SmolFunction] = []
    _function_bodies:list[list[ByteCodeInstruction]] = []

    _nextLabel:int = 1

    # Labels for jumoing to are just numeric place holders. When a code gen section needs to
    # create a new jump-location, it can use this function
    def reserveLabelId(self) -> int:
        self._nextLabel += 1
        return self._nextLabel
    
    @staticmethod
    def appendInstruction(the_list:list[ByteCodeInstruction], opcode:OpCode, operand1:Optional[Any] = None, operand2:Optional[Any] = None) -> list[ByteCodeInstruction]:
        instr = ByteCodeInstruction(opcode, operand1, operand2)
        the_list.append(instr)
        return the_list
    
    # elem was list[ByteCodeInstruction] | ByteCodeInstruction) in TS
    @staticmethod
    def appendChunk(the_list:list[ByteCodeInstruction], elem:Any) -> list[ByteCodeInstruction]:
        if (isinstance(elem, list)):
            for element in elem:
                the_list.append(element)
        elif (isinstance(elem, ByteCodeInstruction)):
            the_list.append(elem)
        else:
            raise SmolCompilerError(f"Can't append {elem} to chunk")

        return the_list
    
    @staticmethod
    def peek_last(the_list:list[Any]) -> Any:
        return the_list[the_list.__len__() - 1]
    
    # This is our structure to hold the constants that appear in source and need to be
    # referenced by the program (e.g., numbers, strings, bools). We define some here
    # so that a few common ones always have the same index.
    _constants:list[SmolVariable] = []

    _loopStack:list[WhileLoop] = []
    
    # This method can be called by any block that needs to create/reference a constant, either
    # getting the existing index of the value if we already have it, or inserting and returning
    # the new index 
    def ensureConst(self, value:SmolVariable) -> int:

        constIndex = -1

        i = 0
        while i < self._constants.__len__():
            e = self._constants[i]
            
            if (e == value):
                constIndex = i
                break
            i += 1

        if (constIndex == -1):
            self._constants.append(value)
            constIndex = self._constants.__len__() - 1

        return constIndex
    
    def Compile(self, source:str) -> SmolProgram:

        scanner = Scanner(source)
        scanner.scan()
        parser = Parser(scanner.tokens)
        statements = parser.parse()

        mainChunk = self.createChunk()
        Compiler.appendInstruction(mainChunk, OpCode.START) # This NOP is here so if the user starts the program with step, it will immediately hit this and show the first real statement as the next/first instruction to execute
        mainChunk[0].isStatementStartpoint = True
        
        i = 0
        while(i < statements.__len__()):
            Compiler.appendChunk(mainChunk, statements[i].accept(self))
            i += 1

        Compiler.appendInstruction(mainChunk, OpCode.EOF)
        mainChunk[mainChunk.__len__() - 1].isStatementStartpoint = True

        program = SmolProgram()
        program.constants = self._constants
        program.code_sections.append(mainChunk)
        
        for b in self._function_bodies:
            program.code_sections.append(b)

        program.function_table = self._function_table
        program.tokens = scanner.tokens
        program.source = source

        return program

    # Short hand helper method to keep the code a little tidier 
    def createChunk(self) -> list[ByteCodeInstruction]:
        return []
    

    def visitBlockStatement(self, stmt:BlockStatement) -> list[ByteCodeInstruction]:

        chunk = self.createChunk()

        enterScope = ByteCodeInstruction(OpCode.ENTER_SCOPE)

        #enterScope.token_map_start_index = stmt.blockStartTokenIndex
        #enterScope.token_map_end_index = stmt.blockStartTokenIndex

        enterScope.isStatementStartpoint = not stmt.insertedByParser # Only break on this statement if it's directly linked to actual user code

        Compiler.appendChunk(chunk, enterScope)

        for blockStmt in stmt.statements:
            c = blockStmt.accept(self)
            Compiler.appendChunk(chunk, c)

        leaveScope = ByteCodeInstruction(OpCode.LEAVE_SCOPE)
        #leaveScope.token_map_start_index = stmt.blockEndTokenIndex;
        #leaveScope.token_map_end_index = stmt.blockEndTokenIndex;
        if (not stmt.insertedByParser):
            leaveScope.isStatementStartpoint = True
        
        Compiler.appendChunk(chunk, leaveScope)

        return chunk
    


    def visitBreakStatement(self, stmt:BreakStatement) -> list[ByteCodeInstruction]:         
        chunk = self.createChunk()

        Compiler.appendInstruction(chunk, OpCode.LOOP_EXIT, Compiler.peek_last(self._loopStack).endOfLoop)
        chunk[0].isStatementStartpoint = True
        #chunk.mapTokens(stmt.tokenIndex, stmt.tokenIndex)
        
        return chunk
    

    def visitClassStatement(self, stmt:ClassStatement) -> ByteCodeInstruction: 

        for fn in stmt.functions: 
        
            function_index = self._function_bodies.__len__() + 1
            function_name = f'@$stmt.className.lexeme.$fn.name.lexeme'

            param_names = []

            for p in fn.parameters:
                param_names.append(p.lexeme)

            self._function_table.append(SmolFunction(function_name, function_index, fn.parameters.__len__(), param_names))
    
            body = self.createChunk()

            Compiler.appendChunk(body, fn.functionBody.accept(self))
    
            if (body.__len__() == 0 or Compiler.peek_last(body).opcode != OpCode.RETURN):
            
                Compiler.appendInstruction(body, OpCode.CONST, self.ensureConst(SmolNull()))
                Compiler.appendInstruction(body, OpCode.RETURN)
            
    
            self._function_bodies.append(body)

        # We are declaring a function, we don't add anything to the byte stream at the current loc.
        # When we allow functions as expressions and assignments we'll need to do something
        # here, I guess something more like load constant but for functions
        return ByteCodeInstruction(OpCode.NOP)
    

    def visitContinueStatement(self, stmt:ContinueStatement) -> list[ByteCodeInstruction]: 

        chunk = self.createChunk()

        Compiler.appendInstruction(chunk, OpCode.LOOP_EXIT, Compiler.peek_last(self._loopStack).startOfLoop)
        chunk[0].isStatementStartpoint = True
        #chunk.mapTokens(stmt.tokenIndex, stmt.tokenIndex)
        
        return chunk
    

    def visitDebuggerStatement(self, stmt:DebuggerStatement) -> list[ByteCodeInstruction]: 

        chunk = self.createChunk()

        Compiler.appendInstruction(chunk, OpCode.DEBUGGER)
        chunk[0].isStatementStartpoint = True
        #chunk.mapTokens(stmt.tokenIndex, stmt.tokenIndex)

        return chunk
    

    def visitExpressionStatement(self, stmt:ExpressionStatement) -> list[ByteCodeInstruction]: 

        chunk = self.createChunk()

        Compiler.appendChunk(chunk, stmt.expression.accept(self))
        Compiler.appendInstruction(chunk, OpCode.POP_AND_DISCARD)

        chunk[0].isStatementStartpoint = True
        #chunk.mapTokens(stmt.firstTokenIndex, stmt.lastTokenIndex)

        return chunk
    
    
    def visitFunctionStatement(self, stmt:FunctionStatement) -> ByteCodeInstruction: 

        function_index = self._function_bodies.__len__() + 1
        function_name = stmt.name.lexeme

        param_names = []

        for p in stmt.parameters:
            param_names.append(p.lexeme)

        self._function_table.append(SmolFunction(function_name, function_index, stmt.parameters.__len__(), param_names))

        body = self.createChunk()

        Compiler.appendChunk(body, stmt.functionBody.accept(self))

        if (body.__len__() == 0 or Compiler.peek_last(body).opcode != OpCode.RETURN):
        
            Compiler.appendInstruction(body, OpCode.CONST, self.ensureConst(SmolNull()))
            Compiler.appendInstruction(body, OpCode.RETURN)
        

        self._function_bodies.append(body)

        # We are declaring a function, we don't add anything to the byte stream at the current loc.
        # When we allow functions as expressions and assignments we'll need to do something
        # here, I guess something more like load constant but for functions
        return ByteCodeInstruction(OpCode.NOP)
    
    

    def visitIfStatement(self, stmt:IfStatement) -> list[ByteCodeInstruction]: 

        chunk = self.createChunk()

        notTrueLabel = self.reserveLabelId()

        Compiler.appendChunk(chunk, stmt.expression.accept(self))
        chunk[0].isStatementStartpoint = True

        Compiler.appendInstruction(chunk, OpCode.JMPFALSE, notTrueLabel)

        thenChunk = stmt.thenStatement.accept(self)
        
        if (isinstance(list, thenChunk)):
            #thenChunk.mapTokens(stmt.thenFirstTokenIndex, stmt.thenLastTokenIndex)
            if (isinstance(stmt.thenStatement, BlockStatement)): # .getStatementType() != "Block"):
                thenChunk[0].isStatementStartpoint = True
          
        Compiler.appendChunk(chunk, thenChunk)

        if (stmt.elseStatement == None):        
            Compiler.appendInstruction(chunk, OpCode.LABEL, notTrueLabel)
        else:        
            skipElseLabel = self.reserveLabelId()
            
            Compiler.appendInstruction(chunk, OpCode.JMP, skipElseLabel)
            Compiler.appendInstruction(chunk, OpCode.LABEL, notTrueLabel)

            Compiler.appendChunk(chunk, stmt.elseStatement.accept(self))

            Compiler.appendInstruction(chunk, OpCode.LABEL, skipElseLabel)
        

        #chunk.mapTokens(stmt.exprFirstTokenIndex, stmt.exprLastTokenIndex)

        return chunk

    

    def visitReturnStatement(self, stmt:ReturnStatement) -> list[ByteCodeInstruction]: 

        chunk = self.createChunk()

        if (stmt.expression != None):
            assert stmt.expression is not None
            Compiler.appendChunk(chunk, stmt.expression.accept(self))
        else:        
            Compiler.appendInstruction(chunk, OpCode.CONST, self.ensureConst(SmolNull()))
        

        Compiler.appendInstruction(chunk, OpCode.RETURN)
        ##chunk.mapTokens(stmt.tokenIndex, stmt.exprLastTokenIndex ?? stmt.tokenIndex)
        chunk[0].isStatementStartpoint = True

        return chunk
    

    def visitTryStatement(self, stmt:TryStatement) -> list[ByteCodeInstruction]: 

        chunk = self.createChunk()

        exceptionLabel = self.reserveLabelId()
        finallyLabel = self.reserveLabelId()
        finallyWithExceptionLabel = self.reserveLabelId()

        # self will create a try 'checkpoint' in the vm. If we hit an exception the
        # vm will rewind the stack back to self instruction and jump to the catch/finally.
        Compiler.appendInstruction(chunk, OpCode.TRY, exceptionLabel, False)

        # If an exception happens inside the body, it will rewind the stack to the try that just went on
        # and that tells us where to jump to

        Compiler.appendChunk(chunk, stmt.tryBody.accept(self))

        # If there was no exception, we need to get rid of that try checkpoint that's on the stack, we aren't
        # going back there even if there's an exception in the finally

        Compiler.appendInstruction(chunk, OpCode.POP_AND_DISCARD)

        # Now execute the finally

        Compiler.appendInstruction(chunk, OpCode.JMP, finallyLabel)
        Compiler.appendInstruction(chunk, OpCode.LABEL, exceptionLabel)

        # We're now at the catch part -- even if the user didn't specify one, we'll have a default (of  throw )
        # We now should have the thrown exception on the stack, so if a throw happens inside the catch that will
        # be the thing that's thrown.

        Compiler.appendInstruction(chunk, OpCode.TRY, finallyWithExceptionLabel, True) # True means keep the exception at the top of the stack

        if (stmt.catchBody != None):
        
            if (stmt.exceptionVariableName != None):
            
                Compiler.appendInstruction(chunk, OpCode.ENTER_SCOPE)

                # Top of stack will be exception so store it in variable name

                Compiler.appendInstruction(chunk, OpCode.DECLARE, stmt.exceptionVariableName.lexeme)
                Compiler.appendInstruction(chunk, OpCode.STORE, stmt.exceptionVariableName.lexeme)
            
            else:
            
                # Top of stack is exception, but no variable defined to hold it so get rid of it
                Compiler.appendInstruction(chunk, OpCode.POP_AND_DISCARD)
            

            Compiler.appendChunk(chunk, stmt.catchBody.accept(self)) # Might be a throw inside here...

            if (stmt.exceptionVariableName != None):
            
                Compiler.appendInstruction(chunk, OpCode.LEAVE_SCOPE)
            
        
        else:
        
            # No catch body is replaced by single instruction to rethrow the exception, which is already on the top of the stack

            Compiler.appendInstruction(chunk, OpCode.THROW)
        

        # If we made it here we got through the catch block without a throw, so we're free to execute the regular
        # finally and carry on with execution, exception is fully handled.

        # Top of stack has to the try checkpoint, so get rid of it because we aren't going back there
        Compiler.appendInstruction(chunk, OpCode.POP_AND_DISCARD)
        Compiler.appendInstruction(chunk, OpCode.JMP, finallyLabel)
        Compiler.appendInstruction(chunk, OpCode.LABEL, finallyWithExceptionLabel)

        # If we're here then we had a throw inside the catch, so execute the finally and then throw it again.
        # When we throw self time the try checkpoint has been removed so we'll bubble down the stack to the next
        # try checkpoint (if there is one -- and panic if not)

        if (stmt.finallyBody != None):
        
            Compiler.appendChunk(chunk, stmt.finallyBody.accept(self))

            # Instruction to check for unthrown exception and throw it
        

        Compiler.appendInstruction(chunk, OpCode.THROW)
        Compiler.appendInstruction(chunk, OpCode.LABEL, finallyLabel)

        if (stmt.finallyBody != None):
        
            Compiler.appendChunk(chunk, stmt.finallyBody.accept(self))

            # Instruction to check for unthrown exception and throw it
        

        # Hopefully that all works. It's mega dependent on the instructions leaving the stack in a pristine state -- no
        # half finished evaluations or anything. That's definitely going to be a problem.

        return chunk
    

    def visitThrowStatement(self, stmt:ThrowStatement) -> list[ByteCodeInstruction]: 

        chunk = self.createChunk()

        Compiler.appendChunk(chunk, stmt.expression.accept(self))
        Compiler.appendInstruction(chunk, OpCode.THROW)
        
        return chunk
    

    def visitVarStatement(self, stmt:VarStatement) -> list[ByteCodeInstruction]: 

        chunk = self.createChunk()

        Compiler.appendInstruction(chunk, OpCode.DECLARE, stmt.name.lexeme)

        if (stmt.initializer != None):  
            Compiler.appendChunk(chunk, stmt.initializer.accept(self))
            Compiler.appendInstruction(chunk, OpCode.STORE, stmt.name.lexeme)
        

        #chunk.mapTokens(stmt.firstTokenIndex, stmt.lastTokenIndex)
        chunk[0].isStatementStartpoint = True

        return chunk
    

    def visitWhileStatement(self, stmt:WhileStatement) -> list[ByteCodeInstruction]: 
        
        chunk = self.createChunk()

        startOfLoop = self.reserveLabelId()
        endOfLoop = self.reserveLabelId()

        self._loopStack.append(WhileLoop(startOfLoop, endOfLoop))

        Compiler.appendInstruction(chunk, OpCode.LOOP_START)
        Compiler.appendInstruction(chunk, OpCode.LABEL, startOfLoop)
        whileExpr = stmt.whileCondition.accept(self)
        if (whileExpr[0] == None):
            whileExpr.isStatementStartpoint = True
        else:
           whileExpr[0].isStatementStartpoint = True

        Compiler.appendChunk(chunk, whileExpr)
        Compiler.appendInstruction(chunk, OpCode.JMPFALSE, endOfLoop)

        stmtChunk = stmt.executeStatement.accept(self)
        #stmtChunk.mapTokens(stmt.stmtFirstTokenIndex, stmt.stmtLastTokenIndex)
        Compiler.appendChunk(chunk, stmtChunk)

        Compiler.appendInstruction(chunk, OpCode.JMP, startOfLoop)
        Compiler.appendInstruction(chunk, OpCode.LABEL, endOfLoop)
        Compiler.appendInstruction(chunk, OpCode.LOOP_END)

        #chunk.mapTokens(stmt.exprFirstTokenIndex, stmt.exprLastTokenIndex)
        self._loopStack.pop()

        return chunk
    


    def visitAssignExpression(self, expr:AssignExpression) -> list[ByteCodeInstruction]: 

        chunk = self.createChunk()

        Compiler.appendChunk(chunk, expr.value.accept(self))

        Compiler.appendInstruction(chunk, OpCode.STORE, expr.name.lexeme)

        # self is so inefficient

        Compiler.appendInstruction(chunk, OpCode.FETCH, expr.name.lexeme)

        chunk[0].isStatementStartpoint = True

        return chunk
    

    def visitBinaryExpression(self, expr:BinaryExpression) -> list[ByteCodeInstruction]: 
        
        chunk = self.createChunk()

        Compiler.appendChunk(chunk, expr.left.accept(self))
        Compiler.appendChunk(chunk, expr.right.accept(self))

        match (expr.op.type):
            case TokenType.MINUS:
                Compiler.appendInstruction(chunk, OpCode.SUB)
            case TokenType.DIVIDE:
                Compiler.appendInstruction(chunk, OpCode.DIV)
            case TokenType.MULTIPLY:
                Compiler.appendInstruction(chunk, OpCode.MUL)
            case TokenType.PLUS:
                Compiler.appendInstruction(chunk, OpCode.ADD)
            case TokenType.POW:
                Compiler.appendInstruction(chunk, OpCode.POW)
            case TokenType.REMAINDER:
                Compiler.appendInstruction(chunk, OpCode.REM)
            case TokenType.EQUAL_EQUAL:
                Compiler.appendInstruction(chunk, OpCode.EQL)
            case TokenType.NOT_EQUAL:
                Compiler.appendInstruction(chunk, OpCode.NEQ)
            case TokenType.GREATER:
                Compiler.appendInstruction(chunk, OpCode.GT)
            case TokenType.GREATER_EQUAL:
                Compiler.appendInstruction(chunk, OpCode.GTE)
            case TokenType.LESS:
                Compiler.appendInstruction(chunk, OpCode.LT)
            case TokenType.LESS_EQUAL:
                Compiler.appendInstruction(chunk, OpCode.LTE)
            case TokenType.BITWISE_AND:
                Compiler.appendInstruction(chunk, OpCode.BITWISE_AND)
            case TokenType.BITWISE_OR:
                Compiler.appendInstruction(chunk, OpCode.BITWISE_OR)

            case default:
                raise SmolCompilerError("Binary operation not impleented")
        

        return chunk
    

    def visitCallExpression(self, expr:CallExpression) -> list[ByteCodeInstruction]: 
        
        chunk = self.createChunk()

        # Evalulate the arguments from left to right and pop them on the stack.


        for arg in expr.args.__reversed__(): 
            Compiler.appendChunk(chunk, arg.accept(self))
        

        Compiler.appendChunk(chunk, expr.callee.accept(self)) # Load the function name onto the stack
        Compiler.appendInstruction(chunk, OpCode.CALL, expr.args.__len__(), expr.useObjectRef)

        return chunk
    

    def visitFunctionExpression(self, expr:FunctionExpression) -> ByteCodeInstruction: 

        function_index = self._function_bodies.__len__() + 1
        function_name = f'$_anon_$function_index'

        param_names = []

        for p in expr.parameters:
            param_names.append(p.lexeme)

        self._function_table.append(SmolFunction(function_name, function_index, expr.parameters.__len__(), param_names))

        body = self.createChunk()

        Compiler.appendChunk(body, expr.functionBody.accept(self))

        if (body.__len__() == 0 or Compiler.peek_last(body).opcode != OpCode.RETURN):
        
            Compiler.appendInstruction(body, OpCode.CONST, self.ensureConst(SmolNull()))
            Compiler.appendInstruction(body, OpCode.RETURN)
        

        self._function_bodies.append(body)

        return ByteCodeInstruction(OpCode.FETCH, function_name)
    

    def visitGetExpression(self, expr:GetExpression) -> list[ByteCodeInstruction]: 
        
        chunk = self.createChunk()

        Compiler.appendChunk(chunk, expr.obj.accept(self))
        Compiler.appendInstruction(chunk, OpCode.FETCH, expr.name.lexeme, True)

        return chunk
    

    def visitGroupingExpression(self, expr:GroupingExpression) -> list[ByteCodeInstruction]: 
        
        if (expr.castToStringForEmbeddedStringExpression):
        
            # We use a group with self special flag to force a cast of a varible like '$a' to string, where a is a number (or whatever).
            # self is important because interpolated strings are basically separate expressions joined with a +,
            # so '$a$b' is really a+b internally -- if we force both a and b to toString'd, then
            # you'll get a string concatenation instead of numbers being added...
            
            chunk = self.createChunk()
            
            Compiler.appendChunk(chunk, expr.expr.accept(self))
            Compiler.appendInstruction(chunk, OpCode.FETCH, "toString", True)
            Compiler.appendInstruction(chunk, OpCode.CALL, 0, True)
            
            return chunk
        
        else:
        
            return expr.expr.accept(self)
        
    

    def visitIndexerGetExpression(self, expr:IndexerGetExpression) -> list[ByteCodeInstruction]: 
        
        chunk = self.createChunk()

        Compiler.appendChunk(chunk, expr.obj.accept(self))
        Compiler.appendChunk(chunk, expr.indexerExpression.accept(self))
        Compiler.appendInstruction(chunk, OpCode.FETCH, "@IndexerGet", True)

        return chunk
    
    
    def visitIndexerSetExpression(self, expr:IndexerSetExpression) -> list[ByteCodeInstruction]: 
    
        chunk = self.createChunk()

        Compiler.appendChunk(chunk, expr.obj.accept(self))
        Compiler.appendChunk(chunk, expr.value.accept(self))
        Compiler.appendChunk(chunk, expr.indexerExpression.accept(self))
        Compiler.appendInstruction(chunk, OpCode.STORE, "@IndexerSet", True)

        # self is so inefficient, but we need to read the saved value back onto the stack

        Compiler.appendChunk(chunk, expr.obj.accept(self))

        # TODO: self won't even work for indexer++ etc.
        Compiler.appendChunk(chunk, expr.indexerExpression.accept(self))

        Compiler.appendInstruction(chunk, OpCode.FETCH, "@IndexerSet", True)

        return chunk
    

    def visitLiteralExpression(self, expr:LiteralExpression) -> ByteCodeInstruction: 

        constIndex = self.ensureConst(expr.value)

        return ByteCodeInstruction(OpCode.CONST, constIndex)
    

    def visitLogicalExpression(self, expr:LogicalExpression) -> list[ByteCodeInstruction]: 
        
        chunk = self.createChunk()

        shortcutLabel = self.reserveLabelId()
        testCompleteLabel = self.reserveLabelId()

        match (expr.op.type):
        
            case TokenType.LOGICAL_AND:

                Compiler.appendChunk(chunk, expr.left.accept(self))
                Compiler.appendInstruction(chunk,  OpCode.JMPFALSE, shortcutLabel)
                Compiler.appendChunk(chunk, expr.right.accept(self))
                Compiler.appendInstruction(chunk, OpCode.JMP, testCompleteLabel)
                Compiler.appendInstruction(chunk, OpCode.LABEL, shortcutLabel)

                # We arrived at self point from the shortcut, which had to be FALSE, and that Jump-not-True
                # instruction popped the False result from the stack, so we need to put it back. I think a
                # specific test instruction would make self nicer, but for now we can live with a few extra steps...

                Compiler.appendInstruction(chunk, OpCode.CONST, self.ensureConst(SmolBool(False)))
                Compiler.appendInstruction(chunk, OpCode.LABEL, testCompleteLabel)

            case TokenType.LOGICAL_OR:

                Compiler.appendChunk(chunk, expr.left.accept(self))
                Compiler.appendInstruction(chunk, OpCode.JMPTRUE, shortcutLabel)
                Compiler.appendChunk(chunk, expr.right.accept(self))
                Compiler.appendInstruction(chunk, OpCode.JMP, testCompleteLabel)
                Compiler.appendInstruction(chunk, OpCode.LABEL, shortcutLabel)
                Compiler.appendInstruction(chunk, OpCode.CONST, self.ensureConst(SmolBool(True)))
                Compiler.appendInstruction(chunk, OpCode.LABEL, testCompleteLabel)

        return chunk   
    

    def visitNewInstanceExpression(self, expr:NewInstanceExpression) -> list[ByteCodeInstruction]: 
        
        chunk = self.createChunk()

        className = expr.className.lexeme

        # We need to tell the VM that we want to create an instance of a class.
        # It will need its own environment, and the instance info needs to be on the stack
        # so we can call the ctor, which needs to leave it on the stack afterwards
        # ready for whatever was wanting it in the first place
        Compiler.appendInstruction(chunk, OpCode.CREATE_OBJECT, className)

        if (className != "Object"):
        
            for arg in expr.ctorArgs.__reversed__(): 
                Compiler.appendChunk(chunk, arg.accept(self))

            Compiler.appendInstruction(chunk, OpCode.DUPLICATE_VALUE, expr.ctorArgs.__len__()) # We need two copies of that ref
        
        else:
        
            Compiler.appendInstruction(chunk, OpCode.DUPLICATE_VALUE, 0) # We need two copies of that ref
        


        # Stack now has class instance value

        Compiler.appendInstruction(chunk, OpCode.FETCH, '@$expr.className.lexeme.constructor', True)

        if (className == "Object"):
            for arg in expr.ctorArgs.__reversed__():
                Compiler.appendChunk(chunk, arg.accept(self))
                

        Compiler.appendInstruction(chunk, OpCode.CALL, expr.ctorArgs.__len__(), True)
        Compiler.appendInstruction(chunk, OpCode.POP_AND_DISCARD) # We don't care about the ctor's return value

        return chunk
    

    def visitObjectInitializerExpression(self, expr:ObjectInitializerExpression) -> list[ByteCodeInstruction]: 
        
        chunk = self.createChunk()

        Compiler.appendInstruction(chunk, OpCode.DUPLICATE_VALUE, 2)
        Compiler.appendChunk(chunk, expr.value.accept(self))
        Compiler.appendInstruction(chunk, OpCode.STORE, expr.name.lexeme, True)

        # We don't reload the value onto the stack for these...

        return chunk
    

    def visitSetExpression(self, expr:SetExpression) -> list[ByteCodeInstruction]: 
        
        chunk = self.createChunk()

        Compiler.appendChunk(chunk, expr.obj.accept(self))
        Compiler.appendChunk(chunk, expr.value.accept(self))
        Compiler.appendInstruction(chunk, OpCode.STORE, expr.name.lexeme, True)

        # self is so inefficient, but we need to read the saved value back onto the stack

        Compiler.appendChunk(chunk, expr.obj.accept(self))
        Compiler.appendInstruction(chunk, OpCode.FETCH, expr.name.lexeme, True)

        return chunk
    

    def visitTernaryExpression(self, expr:TernaryExpression) -> list[ByteCodeInstruction]: 
        
        chunk = self.createChunk()
        notTrueLabel = self.reserveLabelId()
        endLabel = self.reserveLabelId()

        Compiler.appendChunk(chunk, expr.evaluationExpression.accept(self))
        Compiler.appendInstruction(chunk, OpCode.JMPFALSE, notTrueLabel)
        Compiler.appendChunk(chunk, expr.expresisonIfTrue.accept(self))
        Compiler.appendInstruction(chunk, OpCode.JMP, endLabel)
        Compiler.appendInstruction(chunk, OpCode.LABEL, notTrueLabel)
        Compiler.appendChunk(chunk, expr.expresisonIfFalse.accept(self))
        Compiler.appendInstruction(chunk, OpCode.LABEL, endLabel)

        return chunk
    

    def visitUnaryExpression(self, expr:UnaryExpression) -> list[ByteCodeInstruction]: 
        
        chunk = self.createChunk()

        match (expr.op.type):
        
            case TokenType.NOT:
                
                    Compiler.appendChunk(chunk, expr.right.accept(self))

                    isTrueLabel = self.reserveLabelId()
                    endLabel = self.reserveLabelId()

                    Compiler.appendInstruction(chunk, OpCode.JMPTRUE, isTrueLabel)

                    # If we're here it was False, so now it's True
                    Compiler.appendInstruction(chunk, OpCode.CONST, self.ensureConst(SmolBool(True)))
                    Compiler.appendInstruction(chunk, OpCode.JMP, endLabel)
                    Compiler.appendInstruction(chunk, OpCode.LABEL, isTrueLabel)

                    # If we're here it was True, so now it's False
                    Compiler.appendInstruction(chunk, OpCode.CONST, self.ensureConst(SmolBool(False)))
                    Compiler.appendInstruction(chunk, OpCode.LABEL, endLabel)
                

            case TokenType.MINUS:

                # self block looks to see if the minus sign is followed by a literal number. If it is,
                # we can create a constant for the negative number and load that instead of the more
                # generalised unary operator behaviour, which negates whatever expression might come 
                # after it in normal cirumstances.
                if (isinstance(expr.right, LiteralExpression) and isinstance(expr.right.value, SmolNumber)):
                    Compiler.appendInstruction(chunk, OpCode.CONST, self.ensureConst(SmolNumber(0 - expr.right.value.value)))
                

                Compiler.appendInstruction(chunk, OpCode.CONST, self.ensureConst(SmolNumber(0)))
                Compiler.appendChunk(chunk, expr.right.accept(self))
                Compiler.appendInstruction(chunk, OpCode.SUB)        

        return chunk
    

    def visitVariableExpression(self, expr:VariableExpression) -> list[ByteCodeInstruction]: 
        
        chunk = self.createChunk()

        Compiler.appendInstruction(chunk, OpCode.FETCH, expr.name.lexeme)

        if (expr.prepostfixOp != None):
        
            if (expr.prepostfixOp == TokenType.POSTFIX_INCREMENT):
            
                Compiler.appendInstruction(chunk, OpCode.FETCH, expr.name.lexeme)
                Compiler.appendInstruction(chunk, OpCode.CONST, self.ensureConst(SmolNumber(1)))
                Compiler.appendInstruction(chunk, OpCode.ADD)
                Compiler.appendInstruction(chunk, OpCode.STORE, expr.name.lexeme)
            

            if (expr.prepostfixOp == TokenType.POSTFIX_DECREMENT):
            
                Compiler.appendInstruction(chunk, OpCode.FETCH, expr.name.lexeme)
                Compiler.appendInstruction(chunk, OpCode.CONST, self.ensureConst(SmolNumber(1)))
                Compiler.appendInstruction(chunk, OpCode.SUB)
                Compiler.appendInstruction(chunk, OpCode.STORE, expr.name.lexeme)
            

            if (expr.prepostfixOp == TokenType.PREFIX_INCREMENT):
            
                Compiler.appendInstruction(chunk, OpCode.CONST, self.ensureConst(SmolNumber(1)))
                Compiler.appendInstruction(chunk, OpCode.ADD)
                Compiler.appendInstruction(chunk, OpCode.STORE, expr.name.lexeme)
                Compiler.appendInstruction(chunk, OpCode.FETCH, expr.name.lexeme)
            

            if (expr.prepostfixOp == TokenType.PREFIX_DECREMENT):
            
                Compiler.appendInstruction(chunk, OpCode.CONST, self.ensureConst(SmolNumber(1)))
                Compiler.appendInstruction(chunk, OpCode.SUB)
                Compiler.appendInstruction(chunk, OpCode.STORE, expr.name.lexeme)
                Compiler.appendInstruction(chunk, OpCode.FETCH, expr.name.lexeme)
            
        return chunk