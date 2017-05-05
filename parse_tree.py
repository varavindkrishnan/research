from tree import *
from operator_types import *


def get_var_type(line):
    split = line.split(" ")
    temp = []
    for element in split:
        if not (element == ""):
            temp.append(element)

    return temp[-1][:-1]


def get_width(line):
    # print(line)
    a, b = line.split("(")
    # print(b)
    a, b = b.split(")")
    return int(a[3:])


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


def get_child(j, lines):
    this_operator = get_operator(lines[j])
    if this_operator in terminals:
        this_token = get_token(lines[j])
        node = assign_tree(this_token)
        return node

    elif this_operator == "CCAST":
        child = get_child(j+1, lines)
        node = assign_tree(this_operator, [child])
        return node

    else:
        return get_assign_tree(j, lines)


def indent(line):
    split = line.split(" ")
    temp = []
    for element in split:
        if not (element == ""):
            temp.append(element)

    temp = temp[0]
    return temp


def indent_level(line):
    # print("From inside indent level :", line)
    split = line.split(" ")
    temp = []
    for element in split:
        if not (element == ""):
            temp.append(element)

    temp = temp[0].split(":")
    levels = []
    for element in temp:
        if element is not "":
            levels.append(int(element))

    #print(levels)
    return levels[-1], len(levels)


def get_second_level(i, lines):
    # print("From inside second level ")
    num, level = indent_level(lines[i])
    this_level = level
    assert(num == 1)
    while num != 2 or level != this_level:
        i += 1
        num, level = indent_level(lines[i])

    return i


def get_third_level(i, lines):
    # print("From inside third level ")
    num, level = indent_level(lines[i])
    this_level = level
    assert(num == 1)
    while num != 3 or level > this_level:
        # print(lines[i])
        i += 1
        num, level = indent_level(lines[i])

    return i


def get_last_level(j, lines):
    # print("From inside last level ")
    level = indent(lines[j])
    reference_size = len(level)
    j += 1
    level = indent(lines[j])
    this_level = level
    this_size = len(level)
    this_operator = get_operator(lines[j])
    while this_size > reference_size or this_level == level:
        j += 1
        if j >= len(lines):
            return j - 1

        this_operator = get_operator(lines[j])
        this_level = indent(lines[j])
        this_size = len(this_level)

    return j


def get_assign_tree(i, lines):
    this_operator = get_operator(lines[i])

    if this_operator in single_operand:
        child = get_child(i + 1, lines)
        node = assign_tree(this_operator, [child])
        return node

    if this_operator in two_operand:
        k = get_second_level(i + 1, lines)
        right_child = get_child(i + 1, lines)
        left_child = get_child(k, lines)
        if this_operator == "SUB" or this_operator == "SHIFTR" or this_operator == "SHIFTL" or this_operator == "LT"or this_operator == "LTE" or this_operator == "GT" or this_operator == "GTE":
            node = assign_tree(this_operator, [right_child, left_child])

        else:
            node = assign_tree(this_operator, [left_child, right_child])

        return node

    if this_operator in three_operand:
        k = get_second_level(i+1, lines)
        l = get_third_level(i+1, lines)
        predicate_child = get_child(i + 1, lines)
        right_child = get_child(k, lines)
        left_child = get_child(l, lines)
        node = assign_tree(this_operator, [predicate_child, left_child, right_child])
        return node

    if this_operator not in operators:
        token = get_token(lines[i])
        node = assign_tree(token,)
        return node

# lines= []
# lines.append("    1:2:3:3:2:3:3:3:3: ASSIGN 0x194b970 <e6963> {d172} @dt=0x190c810@(G/wu32/6)\n")
# lines.append("    1:2:3:3:2:3:3:3:3:1: AND 0x1927be0 <e6972> {d172} @dt=0x190c810@(G/wu32/6)\n")
# lines.append("    1:2:3:3:2:3:3:3:3:1:1: CONST 0x1933fa0 <e6968> {d172} @dt=0x1914e10@(G/w32)  32'h3f\n")
# lines.append("    1:2:3:3:2:3:3:3:3:1:2: CCAST 0x1913450 <e8256> {d172} @dt=0x190c810@(G/wu32/6) sz32\n")
# lines.append("    1:2:3:3:2:3:3:3:3:1:2:1: VARREF 0x1956ee0 <e8255> {d172} @dt=0x190c810@(G/wu32/6)  v__DOT__cont1 [RV] "
#              "<- VAR 0x1922420 <e1495> {d58} @dt=0x190f7e0@(G/w9)  v__DOT__cont1 [P] VAR\n")
# lines.append("    1:2:3:3:2:3:3:3:3:2: VARREF 0x1957240 <e6962> {d172} @dt=0x190c810@(G/wu32/6)  x_out [LV] => "
#              "VAR 0x1932620 <e2888> {d39} @dt=0x190b310@(G/w6)  x_out [PO] [P] OUTPUT\n")
#
# node = get_assign_tree(0, lines)
# print node.key
# for nodes in node.children:
#     print nodes.key
