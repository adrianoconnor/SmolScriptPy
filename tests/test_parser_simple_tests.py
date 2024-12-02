from internals.compiler import Compiler
from internals.scanner import Scanner
from internals.parser import Parser
from internals.token_types import TokenType
from smolvm import SmolVM

def test_parser_simple_example():

    scanner = Scanner("var x = 1; for(var a = 0; a < 10; a++) { x += a; }")
    scanner.scan()
    parser = Parser(scanner.tokens)
    statements = parser.parse()

    assert statements.__len__() == 2
