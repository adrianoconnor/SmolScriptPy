from internals.compiler import Compiler
from internals.scanner import Scanner
from internals.parser import Parser
from internals.token_types import TokenType
from smolvm import SmolVM

def test_parser_simple_example():

    vm = SmolVM.Init("var x = 1; for(var a = 1; a <= 2; a++) { x += a; }")

    assert vm.environment._variables["x"].value == 4

