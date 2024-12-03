from typing import cast
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
from internals.ast.statements.class_statement import ClassStatement
from internals.ast.statements.expression_statement import ExpressionStatement
from internals.ast.statements.function_statement import FunctionStatement
from internals.ast.statements.if_statement import IfStatement
from internals.ast.statements.return_statement import ReturnStatement
from internals.ast.statements.throw_statement import ThrowStatement
from internals.ast.statements.try_statement import TryStatement
from internals.ast.statements.var_statement import VarStatement
from internals.ast.statements.while_statement import WhileStatement

class AstPrinter():

    def __init__(self):
        self.indent_val:int = 0

    def processStatement(self, statement):
        return statement.accept(self)
    
    # def visitVarStatement(self, var):
    #     if (var.initializer != None):
    #         return f"[VarStatement name = {var.name.lexeme}, initializer = {var.initializer.accept(self)}]"
    #     else:
    #         return f"[VarStatement name = {var.name.lexeme}]"
        
    # def visitLiteralExpression(self, exp):
    #     return f"[LiteralExpression value={exp.value}]"
    
    # def visitBinaryExpression(self, exp):
    #     return f"[BinaryExpression\n   left: {exp.left.accept(self)}\n     op:\n  right:\n]"


    def indent(self) -> str:
        self.indent_val += 1
        pad = ''
        i = 0
        while(i < (self.indent_val - 1) * 2):
            pad += ' '
            i += 1
        return pad

    def outdent(self) -> None:
        self.indent_val -= 1


    def visitBlockStatement(self, stmt:BlockStatement):

        i = self.indent()
        rt = ''

        rt += f'{i}[block]\n'

        for x in stmt.statements:
            rt += x.accept(self)
    
        rt += f'{i}[/block]\n'

        self.outdent()

        return rt 


    # Break, continue and debug can receive their stmt objects, but they don't use them and ununsed
    # vars are an eslint error so they aren't declared.
    def visitBreakStatement(self):
        i = self.indent()
        rt = ''

        rt = f'{i}[break]\n'

        self.outdent()
        return rt

    def visitClassStatement(self, stmt:ClassStatement) -> str:

        i = self.indent()
        rt = ''

        rt += f'{i}[class name={stmt.className}]\n'
        i2 = self.indent()
        for f in stmt.functions:
            rt += f'{i2}[classFunction name={f.name.lexeme}]\n'
            n2 = 1
            for p in f.parameters:
                rt += f'{i2}  param {n2}: {p.lexeme}\n'
                n2 += 1

            rt += f.functionBody.accept(self)
            rt += f'{i2}[/classFunction]\n'            
        
        self.outdent()
        rt += f'{i}[/class]\n'
        
        self.outdent()
        return rt
    

    def visitContinueStatement(self):
        i = self.indent()
        rt = ''

        rt = f'{i}[continue]\n'

        self.outdent()
        return rt

    def visitDebuggerStatement(self):
        i = self.indent()
        rt = ''

        rt = f'{i}[debugger]\n'

        self.outdent()
        return rt


    def visitExpressionStatement(self, stmt:ExpressionStatement) -> str:
        i = self.indent()
        rt = ''

        rt += f'{i}[exprStmt {stmt.expression.accept(self)}]\n'

        self.outdent()
        return rt
        
    def visitFunctionStatement(self, stmt:FunctionStatement) -> str:

        i = self.indent()
        rt = ''

        rt += f'{i}[function name={stmt.name.lexeme}]\n'
        
        n = 1
        for p in stmt.parameters:
            rt += f'{i}  param {n}: {p.lexeme}\n'
            n += 1

        rt += stmt.functionBody.accept(self)
        rt += f'{i}[/functionExpression]\n'
        
        self.outdent()
        return rt  

    def visitIfStatement(self, stmt:IfStatement) -> str:
        i = self.indent()
        rt = ''

        rt += f'{i}[if testExpr:{stmt.expression.accept(self)}]\n'
        rt += stmt.thenStatement.accept(self)
        
        if (stmt.elseStatement != None):
            rt += f'{i}[else]\n'
            rt += stmt.elseStatement.accept(self)
        

        rt += f'{i}[end if]\n'

        self.outdent()

        return rt
    



    def visitReturnStatement(self, stmt:ReturnStatement) -> str:
        
        i = self.indent()
        rt = ''

        if (stmt.expression == None):
            rt = f'{i}[return default(undefined)]\n'
        else:
            rt = f'{i}[return expr:{cast(Expression, stmt.expression).accept(self)}]\n'
        
        self.outdent()

        return rt


    def visitTryStatement(self, stmt:TryStatement) -> str:

        i = self.indent()
        rt = ''

        rt += f'{i}[try]\n'
        rt += stmt.tryBody.accept(self)
        rt += f'{i}[/try]\n'
        
        if (stmt.catchBody != None):
            if (stmt.exceptionVariableName != None):
                rt = f'{i}[catch exceptionletiable={stmt.exceptionVariableName.lexeme}]\n'
            else:
                rt = f'{i}[catch]\n'

            rt += stmt.catchBody.accept(self)
            rt = f'{i}[/catch]\n'

        if (stmt.finallyBody != None):
            rt = f'{i}[finally]\n'
            rt += stmt.finallyBody.accept(self)
            rt = f'{i}[/finally]\n'

        self.outdent()
        return rt

    def visitThrowStatement(self, stmt:ThrowStatement) -> str:

        i = self.indent()
        rt = ''

        if (stmt.expression != None):
            rt = f'{i}[throw expr:{stmt.expression.accept(self)}]\n'
        else:
            rt = f'{i}[throw]\n'
        
        self.outdent()
        return rt


    def visitVarStatement(self, stmt:VarStatement) -> str:

        i = self.indent()
        rt = ''

        if (stmt.initializer != None):
            rt += f'{i}[declare var {stmt.name.lexeme} initializer:{stmt.initializer.accept(self)}]\n'
        else:
            rt = f'{i}[declare var {stmt.name.lexeme}]\n'

        self.outdent()
        return rt

    def visitWhileStatement(self, stmt:WhileStatement) -> str:
        
        i = self.indent()
        rt = ''

        rt += f'{i}[while expr:{stmt.whileCondition.accept(self)}]\n'
        rt += stmt.executeStatement.accept(self)
        rt += f'{i}[/while]\n'

        self.outdent()
        return rt


    def visitAssignExpression(self, expr:AssignExpression) -> str:
        return f'(assign var {expr.name.lexeme} = {expr.value.accept(self)})'

    def visitBinaryExpression(self, expr:BinaryExpression) -> str:
        return f'({expr.op.lexeme} {expr.left.accept(self)} {expr.right.accept(self)})'

    def visitCallExpression(self, expr:CallExpression) -> str:
        return f'(call {expr.callee.accept(self)} with {expr.args.__len__()} args)'
    

    def visitFunctionExpression(self, expr:FunctionExpression) -> str:

        i = self.indent()
        rt = ''

        rt = '(functionExpression)\n'
        rt += f'{i}[functionExpression]\n'
        n = 1
        for p in expr.parameters:
            rt += f'{i}  param {n}: {p.lexeme}\n'
            n += 1
        rt += expr.functionBody.accept(self)
        rt += f'{i}[/functionExpression]\n'

        self.outdent()

        return rt

    def visitGetExpression(self, expr:GetExpression) -> str:
        return f'(get obj:{expr.obj.accept(self)} name:{expr.name.lexeme})'
    

    def visitGroupingExpression(self, expr:GroupingExpression) -> str:
        return f'(group expr:{expr.expr.accept(self)})'
    

    def visitIndexerGetExpression(self, expr:IndexerGetExpression) -> str:
        return f'(indexerGet obj:{expr.obj.accept(self)} property:{expr.obj.accept(self)})'

    
    def visitIndexerSetExpression(self, expr:IndexerSetExpression) -> str:
        return f'(indexerSet obj:{expr.obj.accept(self)} property:{expr.obj.accept(self)} value:{expr.value.accept(self)})'


    def visitLiteralExpression(self, expr:LiteralExpression) -> str:
        return f'(literal {"nil" if expr.value == None else expr.value.__str__()})'


    def visitLogicalExpression(self, expr:LogicalExpression) -> str:
        return f'({expr.op.lexeme} {expr.left.accept(self)} {expr.right.accept(self)})'


    def visitNewInstanceExpression(self, expr:NewInstanceExpression) -> str:
        return f'(new {expr.className.lexeme} with {expr.ctorArgs.__len__()} args in ctor)'


    def visitObjectInitializerExpression(self, expr:ObjectInitializerExpression) -> str:
        return f'(initialize {expr.name.lexeme} value:{expr.value.accept(self)})'


    def visitSetExpression(self, expr:SetExpression) -> str:
        return f'(set obj:{expr.obj.accept(self)} name:{expr.name.lexeme} value:{expr.value.accept(self)})'
    

    def visitTernaryExpression(self, expr:TernaryExpression) -> str:
        return f'({expr.evaluationExpression.accept(self)} ? {expr.expresisonIfTrue.accept(self)} : {expr.expresisonIfFalse.accept(self)})'
    

    def visitUnaryExpression(self, expr:UnaryExpression) -> str:
        return f'({expr.op.lexeme} {expr.right.accept(self)})'
    

    def visitVariableExpression(self, expr:VariableExpression) -> str:
        return f'(var {expr.name.lexeme})'