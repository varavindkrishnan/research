#
# def coverage_nu(line):
#     print(line)
#     split = line.split(" ")
#     temp = None
#     for element in split:
#         if not (element == ""):
#             temp = element
#
#     temp = temp[3:]
#     temp = int(temp)
#     return temp
#
#
# def get_operator(line):
#     split = line.split(" ")
#     temp = []
#     for element in split:
#         if not (element == ""):
#             temp.append(element)
#
#     return temp[1]
#
#
# f = open("Vtop_990_final.tree", 'r')
# line = f.readline()
# exp = []
# exp_b = []
# flag = 1
# while line != "":
#     operator = get_operator(line)
#     if operator == "COVERINC":
#         num = coverage_nu(line)
#
#     line = f.readline()

#
# def indent_level(line):
#     split = line.split(" ")
#     temp = []
#     for element in split:
#         if not (element == ""):
#             temp.append(element)
#
#     temp = temp[0].split(":")
#     levels = []
#     for element in temp:
#         if element is not "":
#             levels.append(int(element))
#
#     #print(levels)
#     return levels[-1]
#
# line = "    1:2:3:3:2:1:2:1: VARREF 0x195ad00 <e8217> {d74} @dt=0x190bbf0@(G/wu32/4)  v__DOT__stato [RV] <- VAR 0x1923e30 " \
#        "<e1479> {d55} @dt=0x190dc30@(G/w4)  v__DOT__stato [P] VAR\n"
#
# indent_level(line)

#
# def indent(line):
#     split = line.split(" ")
#     temp = []
#     for element in split:
#         if not (element == ""):
#             temp.append(element)
#
#     temp = temp[0]
#     return temp
#
#
# def get_last_level(j, lines):
#     level = indent(lines[j])
#     reference_size = len(level)
#     j += 1
#     level = indent(lines[j])
#     this_size = len(level)
#
#     while this_size > reference_size:
#         j += 1
#         if j >= len(lines):
#             return j - 1
#
#         level = indent(lines[j])
#         this_size = len(level)
#
#     return j
#
# lines= []
# lines.append("    1:2:3:3:2:3:3:3:3: ASSIGN 0x194b970 <e6963> {d172} @dt=0x190c810@(G/wu32/6)\n")
# lines.append("    1:2:3:3:2:3:3:3:3:1: AND 0x1927be0 <e6972> {d172} @dt=0x190c810@(G/wu32/6)\n")
# lines.append("    1:2:3:3:2:3:3:3:3:1:1: CONST 0x1933fa0 <e6968> {d172} @dt=0x1914e10@(G/w32)  32'h3f\n")
# lines.append("    1:2:3:3:2:3:3:3:3:1:2: CCAST 0x1913450 <e8256> {d172} @dt=0x190c810@(G/wu32/6) sz32\n")
# lines.append("    1:2:3:3:2:3:3:3:3:1:2:1: VARREF 0x1956ee0 <e8255> {d172} @dt=0x190c810@(G/wu32/6)  v__DOT__cont1 [RV] "
#              "<- VAR 0x1922420 <e1495> {d58} @dt=0x190f7e0@(G/w9)  v__DOT__cont1 [P] VAR\n")
# lines.append("    1:2:3:3:2:3:3:3:3:2: VARREF 0x1957240 <e6962> {d172} @dt=0x190c810@(G/wu32/6)  x_out [LV] => "
#              "VAR 0x1932620 <e2888> {d39} @dt=0x190b310@(G/w6)  x_out [PO] [P] OUTPUT\n")
# lines.append("    1:2:3:3:2:3:3:3:4:1 ASSIGN 0x194b970 <e6963> {d172} @dt=0x190c810@(G/wu32/6)\n")
#
# print(get_last_level(0, lines))

# f = open("b11_Vtop_990_final.tree", 'r')
#
#
# def get_width(line):
#     print(line)
#     a, b = line.split("(")
#     print(b)
#     a, b = b.split(")")
#     return int(a[3:])
#
#
# for lines in f:
#     if " VAR " in lines:
#         print(get_width(lines))
#
# import exmod
#
# print(exmod.add(12.1, 3.1))
#
# from ast_2_constrain import parse_trace
#
# toggles = parse_trace("coverage_cycle.trace", 19)
#
# for i in range(len(toggles)):
#     print "Toggles in cycle ", i, " : ",
#     for c in toggles[i]:
#         print c,
#     print("")
# from subprocess import call
# call(["./bench/get_sim_trace.o", "-libpath", "./bench/b11.so"])

from ast_2_constrain import analyze_constraints
from cfg import initialize_ckt_data


node_a, variables, variables_width, inputs, outputs, num_cov_pts, total_pts = initialize_ckt_data()

nodeid_node_mapping = {}
for node in node_a[:2]:
    node.get_nodeid_node_map(nodeid_node_mapping)
    print(node)
coverage_sequence = [[0], [32, 45, 44, 43, 1], [32, 45, 44, 43, 4, 3], [32, 45, 44, 42, 10, 7]]
# coverage_sequence = [[0], [32, 45, 44, 43, 1], [32, 45, 44, 43, 4, 3], [32, 45, 44, 42, 10, 41, 9], [32, 45, 44, 43, 4, 3]]
temp = analyze_constraints(coverage_sequence, nodeid_node_mapping, variables, inputs)
print "Is this exp mutable ? ", temp
