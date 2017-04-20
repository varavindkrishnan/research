# Copyright (c) Microsoft Corporation 2015, 2016

# The Z3 Python API requires libz3.dll/.so/.dylib in the 
# PATH/LD_LIBRARY_PATH/DYLD_LIBRARY_PATH
# environment variable and the PYTHON_PATH environment variable
# needs to point to the `python' directory that contains `z3/z3.py'
# (which is at bin/python in our binary releases).

# If you obtained example.py as part of our binary release zip files,
# which you unzipped into a directory called `MYZ3', then follow these
# instructions to run the example:

# Running this example on Windows:
# set PATH=%PATH%;MYZ3\bin
# set PYTHONPATH=MYZ3\bin\python
# python example.py

# Running this example on Linux:
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:MYZ3/bin
# export PYTHONPATH=MYZ3/bin/python
# python example.py

# Running this example on OSX:
# export DYLD_LIBRARY_PATH=$DYLD_LIBRARY_PATH:MYZ3/bin
# export PYTHONPATH=MYZ3/bin/python
# python example.py


from z3 import *

count = [Int('count%s'%i) for i in range(20)]
s = Solver()

# for i in range(19):
#     s.add(count[i + 1] - count[i] == 1)
#
# s.add(count[19] == 129)

x = BitVec('x', 6)
y2 = BitVec('y2', 6)
y4 = BitVec('y4', 6)
y8 = BitVec('y8', 6)
v__DOT__r_in = BitVec('v__DOT__r_in', 6)
# eval("s.add(x&2 != 0, ~x&4 != 0, ~x&8 != 0, y2 == 2, y4 == 4, y8 == 8)")
# exec "s.add((x>>2)&63 != 0, ~x&4 != 0, ~x&8 != 0, y2 == 2, y4 == 4, y8 == 8)"
exec "s.add((~(x)<<2)&8 == 0)"
exec "s.add((((v__DOT__r_in) >> 2) & 3) != 0)"
exec "s.add((((v__DOT__r_in) >> 2) & 3) != 1)"
exec "s.add((((v__DOT__r_in) >> 2) & 3) != 2)"
# s.add(v__DOT__r_in == 10)
s.check()

try:
    print(s.model())
    k = s.model()
    print(k[v__DOT__r_in])

except Z3Exception:
    print("Expression is unsat")

