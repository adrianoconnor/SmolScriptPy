from internals.compiler import Compiler
from internals.scanner import Scanner
from internals.parser import Parser
from internals.token_types import TokenType
from smol_runtime import SmolRuntime

def test_parser_simple_example():

    src = """function demo_func(start, end) { 
  var y = 0;
  for (var x = start; x < end; x++) {
    y += x;
  }
  return y;
}

var a = demo_func(-2, 10);"""

    vm = SmolRuntime.init(src)

    assert vm.environment._variables["a"].value == 42

