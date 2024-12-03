from internals.compiler import Compiler
from internals.scanner import Scanner
from internals.parser import Parser
from internals.ast.ast_printer import AstPrinter
from smol_runtime import SmolRuntime

s = """
function demo_func(start, end) { 
  var y = 0;
  for (var x = start; x < end; x++) {
    y += x;
  }
  return y;
}

var some_number = demo_func(-2, 10);
"""

scanner = Scanner("var x = 1; for(var a = 0; a < 10; a++) { x += a; }")
scanner.scan()
parser = Parser(scanner.tokens)
statements = parser.parse()
ast = AstPrinter()
for stmt in statements:
    print(ast.processStatement(stmt))

#compiler = Compiler()
#prg = compiler.Compile("var x = 1; for(var a = 0; a < 10; a++) { x += a; }")
#print(prg.decompile())

vm = SmolRuntime.Init("var a = 1; for(var i = 0; i <= 10; i++) { a = a + 1; }")

print(vm.program.decompile())

print(vm.globalEnv._variables)
print(vm.globalEnv._variables["a"].value)

exit(0)


p = Parser(sx.tokens)
stmts = p.parse()
#ast = AstPrinter()
#for stmt in stmts:
#    print(ast.processStatement(stmt))

#c = Compiler()
#prg = c.Compile("var x = 1; x = x + 1;")
#print(prg.decompile())

vm = SmolVM.init("""var a = 10 * (3 + 4);""")

print(vm.runMode)

print(vm.globalEnv._variables)
print(vm.globalEnv._variables["a"].value)