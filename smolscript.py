from internals.scanner import Scanner
from internals.parser import Parser
from internals.ast.ast_printer import AstPrinter

sx = Scanner("""var a = (123 + 321) * 456; /* Blah */
var b = a / 10; //* Test
var c = 'test';
""")

s = Scanner("var x = 1;")
s.scan()

# print(*s.tokens, sep = '\n')

p = Parser(s.tokens)

stmts = p.parse()

ast = AstPrinter()

print(ast.processStatement(stmts[0]))