from internals.compiler import Compiler
from internals.scanner import Scanner
from internals.parser import Parser
from internals.ast.ast_printer import AstPrinter

s = Scanner("""
function pow(n) {
    return n ** 2;
}
                        
var a = (123 + 321) * 456; /* Blah */
var b = a / 10; //* Test
var c = 'test';
var d = pow(a);
""")

sx = Scanner("var x = 1;")
s.scan()

# print(*s.tokens, sep = '\n')

#p = Parser(s.tokens)

#stmts = p.parse()

#ast = AstPrinter()

#for stmt in stmts:
#    print(ast.processStatement(stmt))

c = Compiler()
prg = c.Compile("var x = 1; x = x + 1;")

print(prg.decompile())