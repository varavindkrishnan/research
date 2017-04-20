from operator_types import *

var_stack = []
predicate_stack = []
id_stack = []
assign_stack = []
child1_stack = []
child2_stack = []
node_list = []
indent_stack = []


class node:
    def __init__(self, id, parent_num, parent_id, child1_id, child2_id, predicate, assigns):
        self.id = id
        self.parent_num = parent_num
        self.parent_id = parent_id
        self.child1_id = child1_id
        self.child2_id = child2_id
        self.predicate = predicate
        self.assigns = assigns


def add_node(node_list, id, parent_num, parent_id, child1_id, child2_id, predicate, assigns):
    node_list.append(node(id, parent_num, parent_id, child1_id, child2_id, predicate, assigns))
    node_list[-1].num = len(node_list) - 1


def indent_level(line):
    split = line.split(" ")
    temp = []
    for element in split:
        if not (element == ""):
            temp.append(element)

    temp = temp[0].split(":")
    return len(temp)


def coverage_nu(line):
    #print(line)
    split = line.split(" ")
    temp = None
    for element in split:
        if not (element == ""):
            temp = element

    if "}" in temp:
        return 0

    return int(temp[3:])


def get_token(line):
    split = line.split(" ")
    temp = []
    for element in split:
        if not (element == ""):
            temp.append(element)

    return temp[6]


def get_operator(line):
    split = line.split(" ")
    temp = []
    for element in split:
        if not (element == ""):
            temp.append(element)

    return temp[1]


def push_exp(text):
    var_stack.append(get_token(text))


def get_exp(line, f):
    temp = []
    operator = get_operator(line)
    if operator in operators:
        n_line = f.readline()

        if operator in single_operand:
            n_line, wew = get_exp(n_line, f)
            temp = temp[:] + wew[:]
            return n_line, temp

        elif operator == "COND":
            n_line, wew = get_exp(n_line, f)
            temp = temp[:] + wew[:]
            n_line = f.readline()
            n_line, wew = get_exp(n_line, f)
            temp = temp[:] + wew[:]
            n_line = f.readline()
            n_line, wew = get_exp(n_line, f)
            temp = temp[:] + wew[:]
            return n_line, temp

        elif operator == "ARRAYSEL":
            n_line, wew = get_exp(n_line, f)
            temp = temp[:] + wew[:]
            n_line = f.readline()
            n_line, wew = get_exp(n_line, f)
            temp = temp[:] + wew[:]
            return n_line, temp

        else:
            n_line, wew = get_exp(n_line, f)
            temp = temp[:] + wew[:]
            n_line = f.readline()
            n_line, wew = get_exp(n_line, f)
            temp = temp[:] + wew[:]
            return n_line, temp

    elif operator in terminals:
        temp.append(get_token(line))
        return line, temp

    else:
        return line, temp


def rewrite(exp):
    lhs = []
    rhs = []
    for rows in exp:
        lhs.append(rows[-1])
        temp = []
        for i in range(len(rows) - 1):
            temp.append(rows[i])

        rhs.append(temp)

    return lhs, rhs

#########################################################
#
# def get_branch_details(line, f):
#     exp = []
#     operator = get_operator(line)
#     while operator in assigns:
#         line, temp = get_exp(line, f)
#         exp.append(temp)
#         assignments[-1].append(temp[:])
#         exp_b.append(num)
#         line = f.readline()
#         operator = get_operator(line)
#
#     return exp, line, f
#
#
# f = open("Vtop_990_final.tree", 'r')
# line = f.readline()
# exp = []
# exp_b = []
# assignments = []
# assignments.append([])
# flag = 1
# temp_p = None
# num = -1
# indent = 0
# curr = 0
# this_indent = 0
# child = [[], ]
# level_branch = {}
#
#
# while line != "":
#     print(level_branch)
#     this_indent = indent_level(line)
#     if "_eval" in line:
#         break
#
#     if len(indent_stack) > 0:
#         if indent_stack[0] > this_indent:
#             if len(indent_stack) == 1:
#                 parent_id = -1
#             else:
#                 parent_id = level_branch[indent_stack[1]]
#             print("Adding", id_stack[0])
#             add_node(node_list, id_stack.pop(0), 0, parent_id, 0, 0, predicate_stack.pop(0), assignments.pop(0))
#
#             indent_stack.pop(0)
#
#     operator = get_operator(line)
#
#     if operator == cover:
#         # add_node(node_list, id, parent_num, parent_id, child1_id, child2_id, predicate, assigns)
#         print("Adding", id_stack[0])
#         if len(indent_stack) == 1:
#             parent_id = -1
#         else:
#             parent_id = level_branch[indent_stack[1]]
#         add_node(node_list, id_stack.pop(0), 0, parent_id, 0, 0, predicate_stack[0], assignments.pop(0))
#         level_branch[indent_stack[0]] = num
#         num = coverage_nu(line)
#         id_stack.insert(0, num)
#         indent -= 1
#         assignments.insert(0, [])
#         line = f.readline()
#
#     elif operator == "VAR":
#         potential = get_token(line)
#         if not(potential in var_stack):
#             var_stack.append(get_token(line))
#         line = f.readline()
#
#     elif operator in assigns:
#         line, temp = get_exp(line, f)
#         exp.append(temp)
#         assignments[0].append(temp[:])
#         exp_b.append(num)
#         line = f.readline()
#
#     elif operator == "IF":
#         indent += 1
#         line = f.readline()
#         line, temp = get_exp(line, f)
#         predicate_stack.insert(0, temp[:])
#         line = f.readline()
#         num = coverage_nu(line)
#         temp_indent = indent_level(line)
#         id_stack.insert(0, num)
#         indent_stack.insert(0, temp_indent)
#         assignments.insert(0, [])
#         line = f.readline()
#         level_branch[temp_indent] = num
#
#     else:
#         line = f.readline()


######################################################################################

# print("Printing Vars:")
# for elements in var_stack:
#     print elements

# for i in range(len(exp)):
#     print("in branch", exp_b[i]," ", exp[i])
#
# lhs, rhs = rewrite(exp)
#
# for i in range(len(lhs)):
#     print(lhs[i], " = ", rhs[i])
#
#
# dependency_m = []
# for i in range(len(var_stack)):
#     dependency_m.append([])
#
#
# for i in range(len(lhs)):
#     for j in range(len(rhs[i])):
#         if rhs[i][j] in var_stack:
#             k = var_stack.index(rhs[i][j])
#             if lhs[i] in var_stack:
#                 q = var_stack.index(lhs[i])
#                 if k not in dependency_m[q]:
#                     dependency_m[q].append(k)
#
#
# for i in range(len(dependency_m)):
#     print(i, " ", var_stack[i], " ", dependency_m[i])

for i in range(len(node_list)):
    print("ID", node_list[i].id, node_list[i].predicate, node_list[i].assigns, node_list[i].parent_id)


