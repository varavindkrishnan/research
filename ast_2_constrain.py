from tree import assign_tree
from operator_types import *
from cfg import variables, variables_width
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


def add_variables_to_solver():
    var_z3_type = []

    for variable in variables:
        # x = BitVec('x', 6)
        var_z3_type.append(BitVec(variable, variables_width[variable]))
        mapping[variable] = len(var_z3_type) - 1

    return


def solve_now(solver):
    status = solver.check()
    if status == "unsat":
        return None

    else:
        return solver.model()

