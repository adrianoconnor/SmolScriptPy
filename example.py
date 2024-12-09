from smol_runtime import SmolRuntime

print("\n**********************************")
print("*** SmolScript for Python Demo ***")
print("**********************************\n")
print(f"Example Javascript (SmolScript) source code to compile and run:")
print("----------------------------------------")

example_smolscript_source_code = """
function demo_func(start, end) { 
  var y = 0;
  for (var x = start; x < end; x++) {
    y += x;
  }
  return y;
}

var some_number = demo_func(-2, 10);
"""

print(example_smolscript_source_code)
print("----------------------------------------\n")
print("Creating...")

vm = SmolRuntime.create(example_smolscript_source_code)

print("Running...")

vm.run()

print("Completed.\n")
print(f"After execution, the value of varable 'some_number' in the vm's memory is {vm.globalEnv._variables["some_number"].value}")

print("\nDo you want to see the compiled bytecode that we generated and executed in the VM? (y/n)")

opt = input()

if (opt == "y"):
  print("Decompiled byte code:")
  print(vm.program.decompile())

