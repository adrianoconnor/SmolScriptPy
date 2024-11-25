from .expression import Expression

class CallExpression(Expression):

    callee:Expression
    args:list[Expression]
    useObjectRef:bool

    def __init__(self, callee:Expression, args:list[Expression], useObjectRef:bool):
        super().__init__()
        self.callee = callee
        self.args = args
        self.useObjectRef = useObjectRef

    def accept(self, visitor):
        return visitor.visitCallExpression(self)
    