from tree import assign_tree
from operator_types import *
from z3 import *
from known_signals import *
s = Solver()
mapping = {}

#
# def _ast_2_const(ast, exp = ""):
#     return exp
#
#
# def ast_2_const(ast):
#     assert isinstance(ast, assign_tree)
#     constrain = None
#     key = ast.key
#
#     if key in operators:
#         constrain = _ast_2_const(ast)
#         return constrain
#
#     elif key in variables:
#         return constrain
#
#     else:
#         assert False


def add_constraints_to_solver(constrains, var_2_z3_var = None):
    for constrain in constrains:
        for atomic in constrain:
            command = "s.add(" + atomic + ")"
            exec command
    # return solver


def add_variables_to_solver_dict(var_2_z3_var, var_assign_count_cycle, variables, variables_width):
    cycles = len(var_assign_count_cycle)
    # var_z3_type = []

    for variable in variables:
        if variable not in clocks:
            # x = BitVec('x', 6)
            command = ""
            assert isinstance(variable, str)
            for c in range(cycles):

                if variable not in var_assign_count_cycle[c]:
                    # print c, " ",
                    # command = variable + "_" + str(c) + "_" + str(0) + "=BitVec( \'" + variable + "_" + str(
                    #   c) + "_" + str(0) + "\'," + str(variables_width[variable]) + ")"
                    var_2_z3_var[variable + "_" + str(c) + "_" + str(0)] = BitVec(variable + "_" + str(c) + "_" + str(0)
                                                                                  , variables_width[variable])
                    # print(command)
                    # exec command

                else:
                    for i in range(var_assign_count_cycle[c][variable] + 1):
                        # print c, " ",
                        # command = variable + "_" + str(c) + "_" + str(i) + "=BitVec( \'" + variable + "_" + str(
                        #     c) + "_" + str(i) + "\'," + str(variables_width[variable]) + ")"
                        var_2_z3_var[variable + "_" + str(c) + "_" + str(i)] = BitVec(
                            variable + "_" + str(c) + "_" + str(i), variables_width[variable])
                        # print(command)
                        # exec command

    return


def add_variables_to_solver(var_assign_count_cycle, variables, variables_width, constrains, s, inputs):
    cycles = len(var_assign_count_cycle)
    # var_z3_type = []

    for variable in variables:
        if variable not in clocks:
        # x = BitVec('x', 6)
            command = ""
            assert isinstance(variable, str)
            for c in range(cycles):

                if variable not in var_assign_count_cycle[c]:
                    # print c, " ",
                    command = variable + "_" + str(c) + "_" + str(0) + "=BitVec( \'" + variable + "_" + str(c) + "_" + str(0) + "\'," + str(32) + ")"
                    # print(command)
                    exec command
                    command = "s.add(" + variable + "_" + str(c) + "_" + str(0) + " < " + str(2**variables_width[variable]) + ")"
                    # print(command)
                    exec command
                    command = "s.add(" + variable + "_" + str(c) + "_" + str(0) + " >= " + str(0) + ")"
                    # print(command)
                    exec command

                else:
                    for i in range(var_assign_count_cycle[c][variable] + 1):
                        # print c, " ",
                        command = variable + "_" + str(c) + "_" + str(i) + "=BitVec( \'" + variable + "_" + str(c) + "_" + str(i) + "\'," + str(32) + ")"
                        # print(command)
                        exec command
                        command = "s.add(" + variable + "_" + str(c) + "_" + str(i) + " < " + str(2**variables_width[variable]) + ")"
                        # print(command)
                        exec command
                        command = "s.add(" + variable + "_" + str(c) + "_" + str(i) + " >= " + str(0) + ")"
                        # print(command)
                        exec command

        # var_z3_type.append(BitVec(variable + "_" + str(cycles) + "_" + str(var_assign_count_cycle[cycles][variable]),
        #  variables_width[variable]))

    for constrain in constrains:
        # print(constrain)
        for atomic in constrain:
            command = "s.add(" + atomic + ")"
            # print command
            exec command


    if s.check() == unsat:
        # print("UNSAT")
        return "unsat"

    else:
        # print("SAT")
        new_values = []
        # print(s.model())
        solution = s.model()
        for cycle in range(cycles):
            cycle_values = {}
            for var in inputs:
                if var not in clocks:
                    var_name = var + "_" + str(cycle) + "_0"
                    command = "value = solution[" + var + "_" + str(cycle) + "_0]"
                    exec command
                    cycle_values[var] = int(value.as_long())
                    # print(var_name, " : ", value)

            new_values.append(cycle_values)
        return new_values


def solve_now(s):
    status = s.check()
    if status == unsat:
        print("UNSAT")
        return None

    else:

        return s.model()


def analyze_constraints(coverage_sequence, nodeid_node_mapping, variables, inputs):
    # If returns true, can mutate, if returns false, means conflict
    # mutated coverage sequence, includes all branches, not just leaves
    # get the trace
    # compare var assignment in new predicate to the assignment in previous cycle
    # return True
    if len(coverage_sequence) < 2:
        return True

    last_node = coverage_sequence[-1][-1]
    last_cycle = coverage_sequence[-1][:-1]
    last_but_one_cycle = coverage_sequence[-2][:]
    this_predicate = nodeid_node_mapping[last_node].predicate
    var_list = this_predicate.variables(variables)
    # print("I/p Coverage Sequence : ", coverage_sequence)
    # print("Variables to analyze : ", var_list)
    is_var_static = {}
    for e in var_list:
        is_var_static[e] = True
        if e in inputs:
            return True


    # Analyze this cycle
    length = len(last_cycle)
    for i in range(length):
        assigns_in_this_node = nodeid_node_mapping[last_cycle[length - 1 - i]].key
        for assign in assigns_in_this_node:
            # print(assign)
            for elements in var_list:
                if (assign.children[0].key in var_list) and not (assign.is_const(variables)):
                    is_var_static[elements] = False

    for e in var_list:
        if not(is_var_static[e]):
            return True

    # Analyze previous cycle
    length = len(last_but_one_cycle)
    for i in range(length):
        assigns_in_this_node = nodeid_node_mapping[last_but_one_cycle[length - 1 - i]].key
        for assign in assigns_in_this_node:
            # print(assign)
            for elements in var_list:
                # print(assign.children[0].key in var_list)
                # print(assign.is_const(variables))
                if (assign.children[0].key in var_list) and not (assign.is_const(variables)):
                    # print("Making it not a constant")
                    is_var_static[elements] = False

    for e in var_list:
        if not(is_var_static[e]):
            return True

    return False


def parse_trace(num_points):
    f = open("bench/coverage_cycle.trace", 'r')
    lines = f.readlines()
    coverage_cycle = []
    for line in lines:
        coverage_cycle.append([0]*num_points)
        line = line[:-2]
        values = line.split(',')
        for number in values:
            coverage_cycle[-1][int(number)] = 1

    return coverage_cycle
