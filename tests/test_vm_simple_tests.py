from smol_runtime import SmolRuntime

def test_parser_simple_example():

    vm = SmolRuntime.create("var x = 1; for(var a = 1; a <= 2; a++) { x += a; }", True)

    assert vm.environment._variables["x"].value == 4

def test_strings():

    vm = SmolRuntime.create("var a = 'test'; var b = 1; var c = a+b;", True)

    assert vm.environment._variables["c"].value == "test1"

def test_call():

    vm = SmolRuntime.create("function pow(x) { return x ** 2; }", True)

    r = vm.call("pow", 2)

    assert r == 4


def test_array():

    #vm = SmolRuntime.create("var a = []; a.push(123); b = a[0]; c = a.pop(); // d = a.length();}", True)
    vm = SmolRuntime.create("var a = []; a.push(123); var b = a[0];", True)



    assert vm.environment._variables["b"].value == 123
    #assert vm.environment._variables["c"].value == 123
    #assert vm.environment._variables["d"].value == 0

