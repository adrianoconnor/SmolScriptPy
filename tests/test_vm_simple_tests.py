from internals.compiler import Compiler
from internals.scanner import Scanner
from internals.parser import Parser
from internals.token_types import TokenType
from smol_runtime import SmolRuntime

def test_parser_simple_example():

    vm = SmolRuntime.init("var x = 1; for(var a = 1; a <= 2; a++) { x += a; }")

    assert vm.environment._variables["x"].value == 4

