from tree import assign_tree
from operator_types import *
from z3 import *

solver = Solver()
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


def add_to_solver(solver, constrains):
    for constrain in constrains:
        command = "solver.add(" + constrain + ")"
        exec command
    return solver


def add_variables_to_solver(var_assign_count_cycle, variables, variables_width):
    cycles = len(var_assign_count_cycle)
    # var_z3_type = []

    for variable in variables:
        # x = BitVec('x', 6)
        command = ""
        assert isinstance(variable, str)
        for c in range(cycles):
            if variable not in var_assign_count_cycle:
                command = variable + "_" + str(c) + "_" + str(0) + "=BitVec( \'" + variable + "_" + str(c) + "_" + str(0) + "\'", variables_width[variable] + ")"

            else:
                for i in range(var_assign_count_cycle[variable]):
                    command = variable + "_" + str(c) + "_" + str(i) + "=BitVec( \'" + variable + "_" + str(c) + "_" + str(i) + "\'", variables_width[variable] + ")"
        exec command

        # var_z3_type.append(BitVec(variable + "_" + str(cycles) + "_" + str(var_assign_count_cycle[cycles][variable]),
        #  variables_width[variable]))
    return


def solve_now(solver):
    status = solver.check()
    if status == "unsat":
        return None

    else:
        return solver.model()

