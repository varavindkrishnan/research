from parse_tree import get_second_level, get_third_level, get_assign_tree, indent_level, get_last_level, get_token, get_width, get_var_type
from scan_file import get_operator, coverage_nu
from tree import control_flow_tree, swap_operator
from operator_types import *
from cfg_functions import *

global last_number


def get_predicate(j, lines):
    return get_assign_tree(j, lines)


def get_then(j, lines, predicate):
    global last_number
    # get assigns from here
    # if u see another predicate call get if then nodes
    # initialize node using above predicate
    assert(indent_level(lines[j])[0] == 2)
    end = get_last_level(j, lines)
    # print(lines[j])
    # print("End of this block :", end)
    children = []
    key = []
    cov_id = None
    flag = 0
    while j < end:
        operator = get_operator(lines[j])
        if operator == "IF":
            temp = get_if_then_nodes(j, lines)
            j = get_last_level(j, lines)
            for elements in temp:
                children.append(elements)

        elif operator in assigns:
            assignment = get_assign_tree(j, lines)
            j = get_last_level(j, lines)
            key.append(assignment)

        elif operator == cover:
            cov_id = coverage_nu(lines[j])
            j += 1
            assert flag == 0
            flag += 1

        else:
            j += 1

    if cov_id is None:
        last_number += 1
        cov_id = last_number

    if len(children) == 2:
        children[0].opposite_id = children[1].cov_id
        children[1].opposite_id = children[0].cov_id

    predicate.is_predicate = True
    return control_flow_tree(predicate, True, key, children, cov_id)


def get_otherwise(j, lines, predicate):
    global last_number
    # get assigns from here
    # if u see another predicate call get if then nodes
    # initialize node using above predicate
    assert (indent_level(lines[j])[0] == 3)
    end = get_last_level(j, lines)
    # print(lines[j])
    # print("End of this block :", end)
    children = []
    key = []
    cov_id = None
    while j < end:

        operator = get_operator(lines[j])
        # if cov_id == 30:
        #     print(operator)
        #     print operator in assigns

        if operator == "IF":
            temp = get_if_then_nodes(j, lines)
            j = get_last_level(j, lines)
            for elements in temp:
                children.append(elements)

        elif operator in assigns:
            assignment = get_assign_tree(j, lines)
            j = get_last_level(j, lines)
            key.append(assignment)

        elif operator == cover:
            cov_id = coverage_nu(lines[j])
            j += 1

        else:
            j += 1

    swap_operator(predicate)
    if cov_id is None:
        last_number += 1
        cov_id = last_number

    if len(children) == 2:
        children[0].opposite_id = children[1].cov_id
        children[1].opposite_id = children[0].cov_id

    predicate.is_predicate = True
    return control_flow_tree(predicate, False, key, children, cov_id)


def indent(line):
    split = line.split(" ")
    temp = []
    for element in split:
        if not (element == ""):
            temp.append(element)

    temp = temp[0]
    return temp


def get_if_then_nodes(i, lines):
    j = get_second_level(i + 1, lines)
    q = get_last_level(i, lines)
    level = indent(lines[q - 1])
    predicate_1 = get_predicate(i + 1, lines)
    predicate_2 = get_predicate(i + 1, lines)

    if level[-2] == 2:
        then = get_then(j, lines, predicate_1)
        return [then]

    else:
        k = get_third_level(i + 1, lines)
        then = get_then(j, lines, predicate_1)
        otherwise = get_otherwise(k, lines, predicate_2)
        return [then, otherwise]


def initialize_ckt_data(file_name = "b11_Vtop_990_final.tree"):
    global last_number
    last_number = 0
    num_cov_pts = 0
    ast = open(file_name, 'r')
    lines = ast.readlines()
    ast.close()
    i = 0
    node_a = []
    variables = []
    variables_width = {}
    top_scope_not_seen = True
    inputs = []
    outputs = []

    while i < len(lines):

        operator = get_operator(lines[i])

        if operator == "IF":
            temp = get_if_then_nodes(i, lines)
            i = get_last_level(i, lines)
            if len(temp) == 1:
                assert isinstance(temp[0], control_flow_tree)
                node_a.append(temp[0])

            elif len(temp) == 2:
                assert isinstance(temp[0], control_flow_tree)
                assert isinstance(temp[1], control_flow_tree)
                temp[0].opposite_id = temp[1].cov_id
                temp[1].opposite_id = temp[0].cov_id
                node_a.append(temp[0])
                node_a.append(temp[1])

            else:
                assert False

        elif operator == "VAR":
            if top_scope_not_seen:
                variables.append(get_token(lines[i]))
                variables_width[variables[-1]] = (get_width(lines[i]))
                var_type = get_var_type(lines[i])

                # print(var_type, " ", var_type == "INPUT")
                if var_type == "INPUT":
                    inputs.append(variables[-1])

                elif var_type == "OUTPUT":
                    outputs.append(variables[-1])

            i += 1

        elif operator == "COVERDECL":
            last_number = coverage_nu(lines[i])
            num_cov_pts = last_number
            i += 1

        elif operator == "TOPSCOPE":
            top_scope_not_seen = False
            i += 1

        else:
            i += 1

    return node_a, variables, variables_width, inputs, outputs, num_cov_pts, last_number


