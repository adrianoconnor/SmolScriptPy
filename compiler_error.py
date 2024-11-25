class SmolCompilerError(BaseException):

    def __init__(self, *args):
        super().__init__(*args)