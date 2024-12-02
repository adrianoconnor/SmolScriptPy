from internals.compiler import Compiler
from internals.scanner import Scanner
from internals.parser import Parser
from internals.token_types import TokenType
from smolvm import SmolVM

def test_tokenizer_simple_example_a():

    sx = Scanner("var a = 10 * 3 + 2; // Test")
    sx.scan()

    assert sx.tokens[9].type == TokenType.EOF
    assert sx.tokens.__len__() == 10

def test_tokenizer_simple_example_b():

    sx = Scanner("var x = 1; for(var a = 0; a < 10; a++) { x += a; }")
    sx.scan()

    assert sx.tokens.__len__() == 26
    assert sx.tokens[25].type == TokenType.EOF
