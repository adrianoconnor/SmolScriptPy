class AstPrinter():

    def processStatement(self, statement):
        return statement.accept(self)
    
    def visitVarStatement(self, var):
        if (var.initializer != None):
            return f"[VarStatement name = {var.name.lexeme}, initializer = {var.initializer.accept(self)}]"
        else:
            return f"[VarStatement name = {var.name.lexeme}]"
        
    def visitLiteralExpression(self, exp):
        return f"[LiteralExpression value={exp.value}]"
    
    def visitBinaryExpression(self, exp):
        return f"[BinaryExpression\n   left: {exp.left.accept(self)}\n     op:\n  right:\n]"