from .expression import Expression

class CallExpression(Expression):

    def __init__(self, callee:Expression, args:list[Expression], useObjectRef:bool):
        self.callee:Expression = callee
        self.args:list[Expression] = args
        self.useObjectRef:bool = useObjectRef

    def accept(self, visitor):
        return visitor.visitCallExpression(self)
    