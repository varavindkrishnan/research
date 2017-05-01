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


def add_constraints_to_solver(constrains):
    for constrain in constrains:
        print(constrain)
        for atomic in constrain:
            command = "s.add(" + atomic + ")"
            exec command
    # return solver


def add_variables_to_solver(var_assign_count_cycle, variables, variables_width, constrains):
    cycles = len(var_assign_count_cycle)
    # var_z3_type = []

    for variable in variables:
        if variable not in clocks:
        # x = BitVec('x', 6)
            command = ""
            assert isinstance(variable, str)
            for c in range(cycles):

                if variable not in var_assign_count_cycle[c]:
                    print c, " ",
                    command = variable + "_" + str(c) + "_" + str(0) + "=BitVec( \'" + variable + "_" + str(c) + "_" + str(0) + "\'," + str(variables_width[variable]) + ")"
                    print(command)
                    exec command

                else:
                    for i in range(var_assign_count_cycle[c][variable] + 1):
                        print c, " ",
                        command = variable + "_" + str(c) + "_" + str(i) + "=BitVec( \'" + variable + "_" + str(c) + "_" + str(i) + "\'," + str(variables_width[variable]) + ")"
                        print(command)
                        exec command

        # var_z3_type.append(BitVec(variable + "_" + str(cycles) + "_" + str(var_assign_count_cycle[cycles][variable]),
        #  variables_width[variable]))
    for constrain in constrains:
        print(constrain)
        for atomic in constrain:
            command = "s.add(" + atomic + ")"
            print command
            exec command

    return


def solve_now():
    status = s.check()
    if status == "unsat":
        return None

    else:
        print(s.model())
        return s.model()


def analyze_constraints(constraint_stack):
    return


def invert_constraints(constraints_stack):
    return


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
