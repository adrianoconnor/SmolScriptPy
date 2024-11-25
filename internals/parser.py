from typing import Optional, cast
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
from internals.variable_types.smol_bool import SmolBool
from internals.variable_types.smol_null import SmolNull
from internals.variable_types.smol_number import SmolNumber
from internals.variable_types.smol_string import SmolString
from internals.variable_types.smol_undefined import SmolUndefined
from .token_types import TokenType
from .token import Token

class Parser():

    tokens:list[Token]
    current:int = 0

    def __init__(self, tokens):
        self.tokens = tokens
    
    def parse(self) -> list[Statement]:

        statements:list[Statement] = []
        
        while(not(self.reachedEnd())):

            if (self.peek().type == TokenType.SEMICOLON):
                self.consume(TokenType.SEMICOLON, "")
            else:
                statements.append(self.declaration())

        print(statements)

        return statements

    def reachedEnd(self, skip = 0) -> bool:
        return self.peek().type == TokenType.EOF
    
    def peek(self, skip = 0) -> Token:
        return self.tokens[self.current + skip]

    def check(self, tokenType, skip = 0) -> bool:
        if (self.reachedEnd()):
            return False
    
        return self.peek(skip).type == tokenType
    
    def match(self, *tokenTypes) -> bool:
        for tokenType in tokenTypes:
            if (self.check(tokenType)):
                self.advance()
                return True        
        return False

    def consume(self, tokenType, errorMessageIfNotFound) -> Token:
        if (self.check(tokenType)):
            return self.advance()

        if (tokenType == TokenType.SEMICOLON and self.tokens[self.current - 1].isFollowedByLineBreak):
            return Token(TokenType.SEMICOLON, "", "", -1, -1, -1, -1)

        if (tokenType == TokenType.SEMICOLON and self.check(TokenType.RIGHT_BRACE)):
            return Token(TokenType.SEMICOLON, "", "", -1, -1, -1, -1)

        if (tokenType == TokenType.SEMICOLON and self.check(TokenType.EOF)):
            return Token(TokenType.SEMICOLON, "", "", -1, -1, -1, -1)
        
        raise SmolCompilerError(errorMessageIfNotFound)
    
    def advance(self) -> Token:
        if (not(self.reachedEnd())):
            self.current += 1
        
        return self.previous()

    def previous(self, skip = 0) -> Token:
        return self.tokens[self.current - 1 - skip]


    #######################

    def declaration(self) -> Statement:

        if (self.match(TokenType.VAR)):
            return self.varDeclaration()
        elif (self.match(TokenType.FUNC)):
            return self.functionDeclaration()
        elif (self.match(TokenType.CLASS)):
            return self.classDeclaration()
        else:
            return self.statement()

    def varDeclaration(self) -> VarStatement:

        firstTokenIndex = self.current - 1

        varNameToken = self.consume(TokenType.IDENTIFIER, "Expected variable name")

        initializerExpression:Expression

        if (self.match(TokenType.EQUAL)):
            initializerExpression = self.expression()

        semiColonIndex = self.consume(TokenType.SEMICOLON, "Expected either a value to be assigned or the end of the statement").startPos

        lastTokenIndex = self.current - (1 if semiColonIndex == -1 else 2)

        stmt = VarStatement(varNameToken, initializerExpression)

        stmt.firstTokenIndex = firstTokenIndex
        stmt.lastTokenIndex = lastTokenIndex

        return stmt

    def functionDeclaration(self) -> FunctionStatement:

        functionName:Token = self.consume(TokenType.IDENTIFIER, "Expected function name")
        functionParameters:list[Token] = []

        self.consume(TokenType.LEFT_BRACKET, "Expected (")

        if (not self.check(TokenType.RIGHT_BRACKET)):
            while(True):

                # Number of params limit?

                functionParameters.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name"))
        
                if (not self.match(TokenType.COMMA)):
                    break        
        
        self.consume(TokenType.RIGHT_BRACKET, "Expected )")
        self.consume(TokenType.LEFT_BRACE, "Expected {")
        
        functionBody = self.block()

        return FunctionStatement(functionName, functionParameters, functionBody)


    def classDeclaration(self) -> ClassStatement:
       
        className:Token = self.consume(TokenType.IDENTIFIER, "Expected function name")
        superclassName:Token
        functions:list[FunctionStatement] = []

        if (self.match(TokenType.COLON)):
            superclassName = self.consume(TokenType.IDENTIFIER, "Expected superclass name")
    
        self.consume(TokenType.LEFT_BRACE, "Expected {")
        
        while (not(self.check(TokenType.RIGHT_BRACE)) and not(self.reachedEnd())):
            if (self.check(TokenType.IDENTIFIER) and self.check(TokenType.LEFT_BRACKET, 1)):
                classFn = self.functionDeclaration()
                functions.append(classFn)
            else:            
                raise SmolCompilerError(f"Didn't expect to find {self.peek()} in the class body")
            
        
        self.consume(TokenType.RIGHT_BRACE, "Expected }")

        return ClassStatement(className, superclassName, functions)

    def statement(self) -> Statement:

        if (self.match(TokenType.IF)):
            return self.ifStatement() 
        elif (self.match(TokenType.WHILE)):
            return self.whileStatement()
        elif (self.match(TokenType.LEFT_BRACE)):
            return self.block()
        elif (self.match(TokenType.BREAK)):
            return self.breakStatement()
        elif (self.match(TokenType.CONTINUE)):
            return self.continueStatement()
        elif (self.match(TokenType.RETURN)):
            return self.returnStatement()
        elif (self.match(TokenType.TRY)):
            return self.tryStatement()
        elif (self.match(TokenType.THROW)):
            return self.throwStatement()
        elif (self.match(TokenType.FOR)):
            return self.forStatement()
        elif (self.match(TokenType.DEBUGGER)):
            return self.debuggerStatement()

        return self.expressionStatement()
    

    def ifStatement(self) -> Statement:

        self.consume(TokenType.LEFT_BRACKET, "Expected (")

        test_expression = self.expression()

        self.consume(TokenType.RIGHT_BRACKET, "Expected )")

        if_true_statement = self.statement()

        else_statement:Statement

        if (self.match(TokenType.ELSE)):
            else_statement = self.statement()   

        if_statement = IfStatement(test_expression, if_true_statement, else_statement)

        return if_statement
    
    def whileStatement(self) -> Statement:

        self.consume(TokenType.LEFT_BRACKET, "Expected (")

        expr = self.expression()

        self.consume(TokenType.RIGHT_BRACKET, "Expected )")

        stmt = self.statement()

        return WhileStatement(expr, stmt)

    def block(self) -> BlockStatement:
    
        stmts:list[Statement] = []

        while (not(self.check(TokenType.RIGHT_BRACE)) and not(self.reachedEnd())):
            stmts.append(self.declaration())
    
        self.consume(TokenType.RIGHT_BRACE, "Expected '}' after block.")
        
        return BlockStatement(stmts)    

    def breakStatement(self) -> BreakStatement:

        self.consume(TokenType.SEMICOLON, "Expected ;")
        
        return BreakStatement()

    def continueStatement(self) -> ContinueStatement:

        self.consume(TokenType.SEMICOLON, "Expected ;")

        return ContinueStatement()
    
    def returnStatement(self) -> ReturnStatement:

        next = self.peek().type

        if (next == TokenType.SEMICOLON or next == TokenType.RIGHT_BRACE or self.previous().isFollowedByLineBreak):
                                        
            self.consume(TokenType.SEMICOLON, "Expected ;")

            return ReturnStatement()
        
        else:
        
            expr = self.expression()
            
            self.consume(TokenType.SEMICOLON, "Expected ;")

            return ReturnStatement(expr)

    def tryStatement(self) -> TryStatement:

        self.consume(TokenType.LEFT_BRACE, "Expected {")

        tryBody:BlockStatement = self.block()
        catchBody:BlockStatement
        finallyBody:BlockStatement
        exceptionVarName:Token

        if (self.match(TokenType.CATCH)):
        
            if (self.match(TokenType.LEFT_BRACKET)):            
                exceptionVarName = self.consume(TokenType.IDENTIFIER, "Expected a single variable name for exception variable")
                self.consume(TokenType.RIGHT_BRACKET, "Expected )")
            
            self.consume(TokenType.LEFT_BRACE, "Expected {")
            catchBody = self.block()
    
        if (self.match(TokenType.FINALLY)):
            self.consume(TokenType.LEFT_BRACE, "Expected {")
            finallyBody = self.block()
        
        if (catchBody == None or finallyBody == None):
            self.consume(TokenType.CATCH, "Expected catch or finally")
        
        return TryStatement(tryBody, exceptionVarName, catchBody, finallyBody)

    def throwStatement(self) -> ThrowStatement:
        expr:Expression = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ;")
        return ThrowStatement(expr)
    
    def debuggerStatement(self) -> DebuggerStatement:
        self.consume(TokenType.SEMICOLON, "Expected ;")
        return DebuggerStatement()

    def forStatement(self) -> Statement:

        self.consume(TokenType.LEFT_BRACKET, "Expected (")

        initialiser:Optional[Statement]

        if (self.match(TokenType.SEMICOLON)):
            initialiser = None
        elif (self.match(TokenType.VAR)):
            initialiser = self.varDeclaration()
        else:
            initialiser = self.expressionStatement()

        condition:Expression

        if (not self.check(TokenType.SEMICOLON)):
            condition = self.expression()
        else:
            condition = LiteralExpression(SmolBool(True))

        self.consume(TokenType.SEMICOLON, "Expected ;")

        incrementer:Expression

        if (not self.check(TokenType.RIGHT_BRACKET)):
            incrementer = self.expression()

        self.consume(TokenType.RIGHT_BRACKET, "Expected )")

        body = self.statement()

        if (incrementer != None):
            incrExprStmt = ExpressionStatement(incrementer)
            innerStmts:list[Statement] = [body, incrExprStmt]

            body = BlockStatement(innerStmts, True) # true is for 'inserted by parser' on the block statement
        

        whileStmt = WhileStatement(condition, body)

        if (initialiser != None):            
            return BlockStatement([cast(Statement, initialiser), whileStmt], True)
        else:
            return whileStmt

    def expressionStatement(self) -> ExpressionStatement:
        
        return ExpressionStatement(self.expression())

    #######################

    def expression(self):

        expr = self.assignment()

        if (self.match(TokenType.QUESTION_MARK)):
            thenExpression = self.expression()
            self.consume(TokenType.COLON, "Expected :")
            elseExpression = self.expression()

            return TernaryExpression(expr, thenExpression, elseExpression)

        return expr

    def assignment(self) -> Expression:

        expr = self.functionExpression()

        if (self.match(TokenType.EQUAL)):

            value:Expression = self.assignment()

            if (isinstance(expr, VariableExpression)):
                return AssignExpression(expr.name, value)
            elif (isinstance(expr, GetExpression)):
                return SetExpression(expr.obj, expr.name, value)
            elif (isinstance(expr, IndexerGetExpression)):
                return IndexerSetExpression(expr.obj, expr.indexerExpression, value)
            
            raise SmolCompilerError("Invalid assignment target")

        if (self.match(TokenType.PLUS_EQUALS)):
            return self.compoundAssignmentExpressionHelper(TokenType.PLUS, "+=", expr)
        if (self.match(TokenType.MINUS_EQUALS)):
            return self.compoundAssignmentExpressionHelper(TokenType.MINUS, "-=", expr)
        if (self.match(TokenType.DIVIDE_EQUALS)):
            return self.compoundAssignmentExpressionHelper(TokenType.DIVIDE, "/=", expr)
        if (self.match(TokenType.REMAINDER_EQUALS)):
            return self.compoundAssignmentExpressionHelper(TokenType.REMAINDER, "%=", expr)
        if (self.match(TokenType.MULTIPLY_EQUALS)):
            return self.compoundAssignmentExpressionHelper(TokenType.MULTIPLY, "*=", expr)
        if (self.match(TokenType.POW_EQUALS)):
            return self.compoundAssignmentExpressionHelper(TokenType.POW, "**=", expr)

        return expr
    

    def compoundAssignmentExpressionHelper(self, tokenForExpression:TokenType, literalForExpression:str, expr:Expression) -> Expression:

        originalToken:Token = self.previous()
        value:Expression = self.assignment()
        binExpr = BinaryExpression(expr, Token(tokenForExpression, literalForExpression, None, originalToken.line, originalToken.col, originalToken.startPos, originalToken.endPos), value)

        if (isinstance(expr, VariableExpression)):
            return AssignExpression(expr.name, binExpr)
        elif (isinstance(expr, GetExpression)):
            return SetExpression(expr.obj, expr.name, binExpr)
        elif (isinstance(expr, IndexerGetExpression)):
            return IndexerSetExpression(expr.obj, expr.indexerExpression, binExpr)
        
        raise SmolCompilerError("Invalid assignment target")
        
    def functionExpression(self) -> Expression:

        if ((self.peek().type == TokenType.LEFT_BRACKET or self.peek().type == TokenType.IDENTIFIER) and self.checkIsStartOfFatArrow(False)):
            return self.fatArrowFunctionExpression(False)
        elif (self.match(TokenType.FUNC)):
    
            functionParams:list[Token] = []

            self.consume(TokenType.LEFT_BRACKET, "Expected (")

            if (not self.check(TokenType.RIGHT_BRACKET)):
                while(True):
                    functionParams.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name"))
                    if (not self.match(TokenType.COMMA)):
                        break

            self.consume(TokenType.RIGHT_BRACKET, "Expected )")
            self.consume(TokenType.LEFT_BRACE, "Expected {")

            functionBody = self.block()

            return FunctionExpression(functionParams, functionBody)

        return self.logicalOr()

    def fatArrowFunctionExpression(self, openBracketConsumed:bool = False) -> FunctionExpression:
    
        if (not openBracketConsumed and self.check(TokenType.LEFT_BRACKET)):
            self.consume(TokenType.LEFT_BRACKET, "Expected (")    
            openBracketConsumed = True
        
        functionParams:list[Token] = []
                
        if (not self.check(TokenType.RIGHT_BRACKET)):
            while(True):
                functionParams.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name"))
                if (not self.match(TokenType.COMMA)):
                    break

        if (openBracketConsumed):
            self.consume(TokenType.RIGHT_BRACKET, "Expected )")

        self.consume(TokenType.FAT_ARROW, "Expected =>")

        if (self.check(TokenType.LEFT_BRACE)):
            self.consume(TokenType.LEFT_BRACE, "Expected {")
            functionBody = self.block()
            return FunctionExpression(functionParams, functionBody)
        else:
            funcBodyStmts:list[Statement] = []
            funcBodyStmts.append(ReturnStatement(self.expression()))
            functionBody = BlockStatement(funcBodyStmts)
            return FunctionExpression(functionParams, functionBody)

    def checkIsStartOfFatArrow(self, openBracketConsumed:bool = True) -> bool:
    
        # If we've jsut consumed an opening bracket we need to look ahead for
        #  (x) => 
        # or
        #  (x, y, z) =>
        
        index = self.current
        
        # If we're looking at an expression, the current token could be an identifier and we just need to check if the next token is =>
        
        if (not openBracketConsumed):
        
            if (not(self.tokens[self.current].isFollowedByLineBreak) and (self.tokens)[self.current + 1].type == TokenType.FAT_ARROW):
                return True
            elif (self.tokens[self.current].type == TokenType.LEFT_BRACKET):
                index += 1 # pretend we consumed the left brack and next section can serve both needs
            else:
                return False
        
        # The logic for brackets is a bit more involved...
        
        previous = TokenType.LEFT_BRACKET

        while (True):
        
            if (self.tokens[index].isFollowedByLineBreak and self.tokens[index].type != TokenType.FAT_ARROW): # => has to be on same line as (...), but newline can come after =>
                break
            
            next = self.tokens[index]

            if (previous == TokenType.LEFT_BRACKET and next.type == TokenType.RIGHT_BRACKET):
                # Valid, move on to the next token
                index += 1
            elif (previous == TokenType.LEFT_BRACKET and next.type == TokenType.IDENTIFIER):
                # Valid, move on to the next token
                index += 1
            elif (previous == TokenType.IDENTIFIER and (next.type == TokenType.COMMA or next.type == TokenType.RIGHT_BRACKET)):
                # Valid, move on to the next token
                index += 1
            elif (previous == TokenType.COMMA and next.type == TokenType.IDENTIFIER):
                # Valid, move on to the next token
                index += 1
            elif (previous == TokenType.RIGHT_BRACKET or next.type == TokenType.FAT_ARROW):
                # Valid, we're definitely dealing with a fat arrow
                return True
            else:
                break
            
            previous = next.type

        return False
    
    def logicalOr(self) -> Expression:
    
        expr = self.logicalAnd()

        while(self.match(TokenType.LOGICAL_OR)):
            op = self.previous()
            right = self.logicalAnd()
            expr = LogicalExpression(expr, op, right)

        return expr

    def logicalAnd(self) -> Expression:
        
        expr = self.equality()

        while(self.match(TokenType.LOGICAL_AND)):
            op = self.previous()
            right = self.equality()
            expr = LogicalExpression(expr, op, right)

        return expr

    def equality(self) -> Expression:
        
        expr = self.comparison()

        while(self.match(TokenType.NOT_EQUAL, TokenType.EQUAL_EQUAL)):
            op = self.previous()
            right = self.comparison()
            expr = BinaryExpression(expr, op, right)

        return expr

    def comparison(self) -> Expression:

        expr = self.bitwise_op()

        while(self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL)):
            op = self.previous()
            right = self.term()
            expr = BinaryExpression(expr, op, right)

        return expr

    def bitwise_op(self) -> Expression:
    
        expr = self.term()

        while (self.match(TokenType.BITWISE_AND, TokenType.BITWISE_OR, TokenType.REMAINDER)):
            op = self.previous()
            right = self.term()
            expr = BinaryExpression(expr, op, right)

        return expr

    def term(self) -> Expression:

        expr:Expression = self.factor()

        while(self.match(TokenType.MINUS, TokenType.PLUS)):
            op:Token = self.previous()
            right:Expression = self.factor()
            expr = BinaryExpression(expr, op, right)

        return expr

    def factor(self) -> Expression:
        
        expr:Expression = self.pow()

        while(self.match(TokenType.MULTIPLY, TokenType.DIVIDE)):
            op:Token = self.previous()
            right:Expression = self.pow()
            expr = BinaryExpression(expr, op, right)

        return expr

    def pow(self) -> Expression:

        expr = self.unary()

        while(self.match(TokenType.POW)):    
            op = self.previous()
            right = self.unary()
            expr = BinaryExpression(expr, op, right)
    
        return expr

    def unary(self) -> Expression:

        if(self.match(TokenType.NOT, TokenType.MINUS)):
            op = self.previous()
            right = self.unary()
            return UnaryExpression(op, right)

        return self.call()

    def call(self) -> Expression:
    
        expr = self.primary()

        while (True):
            if (self.match(TokenType.LEFT_BRACKET)):
                expr = self.finishCall(expr, (isinstance(expr, GetExpression)))
            elif (self.match(TokenType.LEFT_SQUARE_BRACKET)):
                indexerExpression = self.expression()
                self.consume(TokenType.RIGHT_SQUARE_BRACKET, "Expected ]")
                expr = IndexerGetExpression(expr, indexerExpression)
            elif (self.match(TokenType.DOT)):
                name = self.consume(TokenType.IDENTIFIER, "Expect property name after '.'.")
                expr = GetExpression(expr, name)
            else:
                break
            
        return expr

    def finishCall(self, callee:Expression, isFollowingGetter = False) -> Expression:
    
        args:list[Expression] = []

        if (not self.check(TokenType.RIGHT_BRACKET)):        
            while(True):
                args.append(self.expression())
                if (not self.match(TokenType.COMMA)):
                    break

        self.consume(TokenType.RIGHT_BRACKET, "Expected )")

        return CallExpression(callee, args, isFollowingGetter)
    
    
    def primary(self):

        if (self.match(TokenType.FALSE)):
            return LiteralExpression(SmolBool(False))
        if (self.match(TokenType.TRUE)):
            return LiteralExpression(SmolBool(True))
        if (self.match(TokenType.NULL)):
            return LiteralExpression(SmolNull())
        if (self.match(TokenType.UNDEFINED)):
            return LiteralExpression(SmolUndefined())

        if(self.match(TokenType.NUMBER)):
            return LiteralExpression(SmolNumber(float(self.previous().literal)))

        if(self.match(TokenType.STRING)):
            return LiteralExpression(SmolString(str(self.previous().literal)))

        if (self.match(TokenType.PREFIX_INCREMENT)):
            if (self.match(TokenType.IDENTIFIER)):
                return VariableExpression(self.previous(), TokenType.PREFIX_INCREMENT)
            
        if (self.match(TokenType.PREFIX_DECREMENT)):
            if (self.match(TokenType.IDENTIFIER)):
                return VariableExpression(self.previous(), TokenType.PREFIX_DECREMENT)

        if (self.match(TokenType.IDENTIFIER)):
            if (self.match(TokenType.POSTFIX_INCREMENT)):
                return VariableExpression(self.previous(1), TokenType.POSTFIX_INCREMENT)
            elif (self.match(TokenType.POSTFIX_DECREMENT)):
                return VariableExpression(self.previous(1), TokenType.POSTFIX_DECREMENT)
            else:
                return VariableExpression(self.previous(), None)
            
        

        if (self.match(TokenType.NEW)):
        
            className = self.consume(TokenType.IDENTIFIER, "Expected identifier after new")

            self.consume(TokenType.LEFT_BRACKET, "Expect ')' after expression.")

            # If these three blocks all create a list called function_args I get a mypy re-def error -- not sure why
            function_args_1:list[Expression] = []

            if (not self.check(TokenType.RIGHT_BRACKET)):
                while(True):
                    function_args_1.append(self.expression())
                    if (not self.match(TokenType.COMMA)):
                        break

            self.consume(TokenType.RIGHT_BRACKET, "Expected )")

            return NewInstanceExpression(className, function_args_1)

        if (self.match(TokenType.LEFT_SQUARE_BRACKET)):
        
            originalToken = self.previous()
            className = Token(TokenType.IDENTIFIER, "Array", None, originalToken.line, originalToken.col, originalToken.startPos, originalToken.endPos);
            
            function_args_2:list[Expression] = []

            if (not self.check(TokenType.RIGHT_SQUARE_BRACKET)):            
                while(True):
                    function_args_2.append(self.expression())
                    if (not self.match(TokenType.COMMA)):
                        break
        
            self.consume(TokenType.RIGHT_SQUARE_BRACKET, "Expected ]")

            return NewInstanceExpression(className, function_args_2)

        if (self.match(TokenType.LEFT_BRACE)):
            originalToken = self.previous()
            className = Token(TokenType.IDENTIFIER, "Object", None, originalToken.line, originalToken.col, originalToken.startPos, originalToken.endPos)

            function_args_3:list[Expression] = []

            if (not self.check(TokenType.RIGHT_BRACE)):
                while(True):
                    name = self.consume(TokenType.IDENTIFIER, "Expected idetifier")
                    self.consume(TokenType.COLON, "Exepcted :")
                    value = self.expression()

                    function_args_3.append(ObjectInitializerExpression(name, value))

                    if (not self.match(TokenType.COMMA)):
                        break

            self.consume(TokenType.RIGHT_BRACE, "Expected }")

            return NewInstanceExpression(className, function_args_3)


        if (self.match(TokenType.LEFT_BRACKET)):
            expr = self.expression()
            self.consume(TokenType.RIGHT_BRACKET, "Expect ')' after expression.")
            return GroupingExpression(expr)
        

        if (self.match(TokenType.START_OF_EMBEDDED_STRING_EXPRESSION)):
            expr = self.expression()
            self.consume(TokenType.END_OF_EMBEDDED_STRING_EXPRESSION, "Expect ')' after expression.")
            return GroupingExpression(expr, True)

        raise SmolCompilerError(f'Parser did not expect to see token "{self.peek().type}" on line {self.peek().line}, sorry :(')
