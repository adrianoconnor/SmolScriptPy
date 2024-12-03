from internals.scanner import Scanner
from internals.token_types import TokenType

def test_tokenizer_simple_example_a():

    tokens = Scanner.scan("var a = 10 * 3 + 2; // Test")

    assert tokens[9].type == TokenType.EOF
    assert tokens.__len__() == 10

def test_tokenizer_simple_example_b():

    tokens = Scanner.scan("var x = 1; for(var a = 0; a < 10; a++) { x += a; }")

    print (tokens)


    assert tokens.__len__() == 26
    assert tokens[25].type == TokenType.EOF
