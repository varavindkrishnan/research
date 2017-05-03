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
from cfg import initialize_ckt_data
from generate_ip_vector import write_vector_to_file, generate_random_ip_vector, run_sim, read_coverage_pt_toggles, write_new_inputs, vector_resize
from parse_tree import get_second_level, get_third_level, get_assign_tree, indent_level, get_last_level, get_token, get_width, get_var_type
from scan_file import get_operator, coverage_nu
from tree import control_flow_tree, swap_operator
from operator_types import *
from cfg_functions import *
from ast_2_constrain import add_variables_to_solver, solve_now, add_constraints_to_solver, invert_constraints, analyze_constraints
from z3 import *
from known_signals import resets_and_clocks, relevant_ids



# count = [Int('count%s'%i) for i in range(20)]


# for i in range(19):
#     s.add(count[i + 1] - count[i] == 1)
#
# s.add(count[19] == 129)

# x = BitVec('x', 6)
# y2 = BitVec('y2', 6)
# y4 = BitVec('y4', 6)
# y8 = BitVec('y8', 6)
# v__DOT__r_in = BitVec('v__DOT__r_in', 6)
# # eval("s.add(x&2 != 0, ~x&4 != 0, ~x&8 != 0, y2 == 2, y4 == 4, y8 == 8)")
# # exec "s.add((x>>2)&63 != 0, ~x&4 != 0, ~x&8 != 0, y2 == 2, y4 == 4, y8 == 8)"
# exec "s.add((~(x)<<2)&8 == 0)"
# exec "s.add((((v__DOT__r_in) >> 2) & 3) != 0)"
# exec "s.add((((v__DOT__r_in) >> 2) & 3) != 1)"
# exec "s.add((((v__DOT__r_in) >> 2) & 3) != 2)"
# s.add(v__DOT__r_in == 10)
#
# exec "r = BitVec(\'reset_0_0\', 1)"
# exec "v__DOT__stato_0_0 = BitVec(\'v__DOT__stato_0_0\', 5)"
# exec "s.add((~(r)) != 0 ,v__DOT__stato_0_0 == 15 , ((v__DOT__stato_0_0) & 8) != 0 ,  ~(((v__DOT__stato_0_0) & 4)) != 0 ,  (~(((v__DOT__stato_0_0) & 2))) != 0 ,  ((v__DOT__stato_0_0) & 1) != 0)"
# #
# ctx = main_ctx()
#
#
# def add_variables():
#     v__DOT__r_in_3_0 = BitVec('v__DOT__r_in_3_0', 6, ctx)
#
#
# def add_constraints_1():
#     v__DOT__r_in_3_0 = BitVec('v__DOT__r_in_3_0', 6)
#     s.add( Not(Or((v__DOT__r_in_3_0 == 18), (v__DOT__r_in_3_0 == 22))))
#
#
# def add_constraints_2():
#     v__DOT__r_in_3_0 = BitVec('v__DOT__r_in_3_0', 6)
#     s.add( Not(Or((v__DOT__r_in_3_0 == 41), (v__DOT__r_in_3_0 == 12))))
#     v__DOT__r_in_3_0.size()
#     print v__DOT__r_in_3_0.size()
#
# # s.add(((v__DOT__r_in_3_0) & 63) != 0)
#
# add_constraints_1()
# add_constraints_2()
# s.check()
# try:
#     print(s.model())
#     k = s.model()
#     #print(k)
#
# except Z3Exception:
#     print("Expression is unsat")

# s = Solver()
#
# constrains = [['reset_0_0 != 0', '(v__DOT__stato_0_1 == 0)', '(v__DOT__r_in_0_1 == 0)', '(v__DOT__cont_0_1 == 0)', '(v__DOT__cont1_0_1 == 0)', '(x_out_0_1 == 0)'],
#               ['v__DOT__r_in_1_0 == v__DOT__r_in_0_1', 'v__DOT__stato_1_0 == v__DOT__stato_0_1', 'v__DOT__cont_1_0 == v__DOT__cont_0_1', 'v__DOT__cont1_1_0 == v__DOT__cont1_0_1', '(reset_1_0 == 0)', '(((v__DOT__stato_1_0) & 8) == 0)', '(((v__DOT__stato_1_0) & 4) == 0)', '(((v__DOT__stato_1_0) & 2) == 0)', '(((v__DOT__stato_1_0) & 1) == 0)', '(v__DOT__cont_1_1 == 0)', '(v__DOT__r_in_1_1 == x_in_1_0)', '(x_out_1_1 == 0)', '(v__DOT__stato_1_1 == 1)'],
#               ['v__DOT__r_in_2_0 == v__DOT__r_in_1_1', 'v__DOT__stato_2_0 == v__DOT__stato_1_1', 'v__DOT__cont_2_0 == v__DOT__cont_1_1', 'v__DOT__cont1_2_0 == v__DOT__cont1_1_0', '(reset_2_0 == 0)', '(((v__DOT__stato_2_0) & 8) == 0)', '(((v__DOT__stato_2_0) & 4) == 0)', '(((v__DOT__stato_2_0) & 2) == 0)', '((v__DOT__stato_2_0) & 1) != 0', '(v__DOT__r_in_2_1 == x_in_2_0)', '(stbi_2_0 == 0)', '(v__DOT__stato_2_1 == 2)'],
#               ['v__DOT__r_in_3_0 == v__DOT__r_in_2_1', 'v__DOT__stato_3_0 == v__DOT__stato_2_1', 'v__DOT__cont_3_0 == v__DOT__cont_2_0', 'v__DOT__cont1_3_0 == v__DOT__cont1_2_0', '(reset_3_0 == 0)', '(((v__DOT__stato_3_0) & 8) == 0)', '(((v__DOT__stato_3_0) & 4) == 0)', '((v__DOT__stato_3_0) & 2) != 0', '(((v__DOT__stato_3_0) & 1) == 0)', 'Or(((v__DOT__r_in_3_0) == 63),((v__DOT__r_in_3_0) == 0))', '(v__DOT__cont1_3_1 == v__DOT__r_in_3_0)', '(v__DOT__stato_3_1 == 8)']]
# variables = ['reset', 'v__DOT__stato', 'v__DOT__r_in', 'v__DOT__cont', 'v__DOT__cont1', 'x_out', 'x_in', 'v__DOT__r_in', 'stbi']
# variables_width = {}
# variables_width['reset'] = 1
# variables_width['x_in'] = 6
# variables_width['stbi'] = 1
# variables_width['x_out'] = 6
# variables_width['v__DOT__r_in'] = 6
# variables_width['v__DOT__stato'] = 4
# variables_width['v__DOT__cont1'] = 9
# variables_width['v__DOT__cont'] = 5
#
# for varia in variables:
#     for i in range(4):
#         for j in range(2):
#             cmd = varia + "_" + str(i) + "_" + str(j) + "=BitVec(\'" + varia + "_" + str(i) + "_" + str(j) + "\',32)"
#             exec cmd
#             command = "s.add(" + varia + "_" + str(i) + "_" + str(j) + " < " + str(
#                 2 ** variables_width[varia]) + ")"
#             # print(command)
#             exec command
#             command = "s.add(" + varia + "_" + str(i) + "_" + str(j) + " >= " + str(0) + ")"
#             # print(command)
#             exec command
#
#
# for constrain in constrains:
#     # print(constrain)
#     for atomic in constrain:
#         command = "s.add(" + atomic + ")"
#         # print command
#         exec command
#
# print s.check()
# print(s.model())

from ast_2_constrain import analyze_constraints
from cfg import initialize_ckt_data


node_a, variables, variables_width, inputs, outputs, num_cov_pts, total_pts = initialize_ckt_data()

nodeid_node_mapping = {}
for node in node_a[:2]:
    node.get_nodeid_node_map(nodeid_node_mapping)
    print(node)

leaf_covid, leaf_predicate = get_leaves_and_trace(node_a[:2])

s = Solver()
cov_pt_trace = [[0], [32, 45, 44, 43, 1], [32, 45, 44, 43, 4, 2], [32, 45, 44, 43, 4, 3], [32, 45, 44, 42, 10, 41, 8], [32, 45, 44, 42, 13, 11], [32, 45, 40, 39, 16, 15], [32, 45, 40, 38, 22, 21], [32, 45, 40, 38, 27, 37, 36, 25], [32, 35, 34, 33, 30, 29], [32, 45, 44, 43, 4, 2], [32, 45, 44, 43, 4, 2], [32, 45, 44, 43, 4, 3], [32, 45, 44, 42, 10, 41, 9], [32, 45, 44, 43, 4, 3], [32, 45, 44, 42, 10, 7, 5], [32, 35, 34, 33, 30, 29], [32, 45, 44, 43, 4, 3], [32, 45, 44, 42, 10, 41, 9], [32, 45, 44, 43, 4, 3], [32, 45, 44, 42, 10, 41, 9], [32, 45, 44, 43, 4, 2], [32, 45, 44, 43, 4, 2], [32, 45, 44, 43, 4, 2], [32, 45, 44, 43, 4, 2], [32, 45, 44, 43, 4, 2], [32, 45, 44, 43, 4, 2], [32, 45, 44, 43, 4, 3], [32, 45, 44, 42, 10, 7, 5], [32, 35, 34, 33, 30, 28]]
cov_pt_trace = [[0], [32, 45, 44, 43, 1], [32, 45, 44, 43, 4, 2], [32, 45, 44, 43, 4, 3], [32, 45, 44, 42, 10, 41, 8], [32, 45, 44, 42, 13, 11], [32, 45, 40, 39, 16, 15], [32, 45, 40, 38, 22, 21], [32, 45, 40, 38, 27, 37, 36, 25], [32, 35, 34, 33, 30, 29], [32, 45, 44, 43, 4, 2], [32, 45, 44, 43, 4, 2], [32, 45, 44, 43, 4, 3], [32, 45, 44, 42, 10, 41, 9], [32, 45, 44, 43, 4, 3], [32, 45, 44, 42, 10, 7, 5], [32, 35, 34, 33, 30, 29], [32, 45, 44, 43, 4, 3], [32, 45, 44, 42, 10, 41, 9], [32, 45, 44, 43, 4, 3], [32, 45, 44, 42, 10, 41, 9], [32, 45, 44, 43, 4, 2], [32, 45, 44, 43, 4, 2], [32, 45, 44, 43, 4, 2], [32, 45, 44, 43, 4, 2], [32, 45, 44, 43, 4, 2], [32, 45, 44, 43, 4, 2], [32, 45, 44, 43, 4, 3], [32, 45, 44, 42, 10, 7, 5], [32, 35, 34, 33, 30, 29]]
leaf_trace = []
for elements in cov_pt_trace:
    leaf_trace.append([elements[-1]])

constraint_sequence, var_assign_count_cycle = constraints_from_coverage(leaf_trace, leaf_predicate, variables, inputs, outputs)
result = add_variables_to_solver(var_assign_count_cycle, variables, variables_width, constraint_sequence, s, inputs)
print(result)