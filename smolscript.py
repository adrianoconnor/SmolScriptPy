from internals.compiler import Compiler
from internals.scanner import Scanner
from internals.parser import Parser
from internals.ast.ast_printer import AstPrinter
from smolvm import SmolVM

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

#sx = Scanner("var x = 1;")
#s.scan()

# print(*s.tokens, sep = '\n')

#p = Parser(s.tokens)
#stmts = p.parse()
#ast = AstPrinter()
#for stmt in stmts:
#    print(ast.processStatement(stmt))

#c = Compiler()
#prg = c.Compile("var x = 1; x = x + 1;")
#print(prg.decompile())

vm = SmolVM.Init("""var a = 10 * (3 + 4);""")

print(vm.runMode)

print(vm.globalEnv._variables)
print(vm.globalEnv._variables["a"].value)