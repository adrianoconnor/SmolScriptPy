from internals.scanner import Scanner
from internals.parser import Parser

def test_parser_simple_example():

    tokens = Scanner.scan("var x = 1; for(var a = 0; a < 10; a++) { x += a; }")
    statements = Parser.parse(tokens)

    assert statements.__len__() == 2


