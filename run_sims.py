from cfg import initialize_ckt_data
from generate_ip_vector import write_vector_to_file, generate_random_ip_vector, run_sim, read_coverage_pt_toggles, write_new_inputs
from parse_tree import get_second_level, get_third_level, get_assign_tree, indent_level, get_last_level, get_token, get_width, get_var_type
from scan_file import get_operator, coverage_nu
from tree import control_flow_tree, swap_operator
from operator_types import *
from cfg_functions import *
from ast_2_constrain import add_variables_to_solver, solve_now, add_constraints_to_solver, invert_constraints, analyze_constraints
from z3 import *
from known_signals import resets_and_clocks, relevant_ids

def print_node(node):
    if len(node.children) > 0:
        for child in node.children:
            print("inside :", node.cov_id)
            print_node(child)

        if node.predicate is not None:
            # print(node.predicate, " Cov id ", node.cov_id)
            temp = node.predicate.get_string()
            if "=" not in temp:
                temp = "( " + temp[:] + " != 0 )"
            print(temp)

        else:
            print("Cov id ", node.cov_id)

    if len(node.children) == 0:
        if node.predicate is not None:
            # print(node.predicate, " Cov id ", node.cov_id)
            temp = node.predicate.get_string()
            if "=" not in temp:
                temp = "( " + temp[:] + " != 0 )"
            print(temp)

        else:
            print("Cov id ", node.cov_id)


def print_cfg(node_a):
    for nodes in node_a:
        print_node(nodes)

# node_a contains list of parent nodes, ie for each always block


# get leaves and traces parses the the above node_a to get the list of leaves of each of the trees in each of the always
#  block along with its corresponding cov_id

# variable width hold the width of each variable

# inputs contains the list of input variables

# contraints from coverage takes the cov id of leaves covered as the trace of simulation and generates the contraits for
#  that trace taking care of UD. Returns Variable assign count a dict which hold assign counts for every variable across
#  all cycles. To be used to early bactrace

# get_nodeid_node_map, lets us access node by directly using cov id

node_a, variables, variables_width, inputs, outputs, num_cov_pts = initialize_ckt_data()


print_cfg(node_a)


for nodes in node_a:
    print(nodes)

leaf_covid, leaf_predicate = get_leaves_and_trace(node_a[:2])

for keys in leaf_covid:
    print(keys, " ", leaf_covid[keys])
print("")

print("Input Vars")
for elements in inputs:
    print(elements, " : ", variables_width[elements])
print("")

for keys in leaf_predicate:
    print keys, " ",
    for elements in leaf_predicate[keys]:
        print(elements.get_string()), ", ",

    print(" ")

nodeid_node_mapping = {}
for node in node_a[:2]:
    node.get_nodeid_node_map(nodeid_node_mapping)

for keys in nodeid_node_mapping:
    print("Iam :", keys, " and my opposite is", nodeid_node_mapping[keys].opposite_id)
#
# print("Constraints for node")
#
# print(len(constraint_sequence))
# for lines in constraint_sequence:
#     print(lines)

print("\n\n\n\n\n\n")
print("Completed CGF and AST parsing")
print("Starting concolic simulation")
print("\n\n\n\n\n\n")
cycles = 5
s = Solver()
ctx = main_ctx()
current_coverage = [0] * len(relevant_ids)

vector = generate_random_ip_vector(variables_width, inputs, cycles)
write_vector_to_file(vector, variables_width, inputs)
run_sim()
coverage_sequence = read_coverage_pt_toggles(cycles, leaf_covid, current_coverage)

complete_flag = True
for i in current_coverage:
    if i != 1:
        complete_flag = Flase
        break

if complete_flag:
    print("100% coverage")
    exit()

print("Coverage Sequence : ", coverage_sequence)
list_cov_pts = get_complete_trace_leaf(coverage_sequence)
print("Coverage trace : ", list_cov_pts)
constraint_sequence, var_assign_count_cycle = constraints_from_coverage(coverage_sequence, leaf_predicate, variables, inputs, outputs)

print("Constrain Sequence : ")
print(len(constraint_sequence))
for lines in constraint_sequence:
    print(lines)


new_constraint = take_next_constraint(list_cov_pts, constraints, nodeid_node_mapping, var_assign_count_cycle, variables, inputs, outputs, coverage_sequence)

print("New Constrain Sequence : ")
print(len(new_constraint))
for lines in new_constraint:
    print(lines)


#################################################################
# result = add_variables_to_solver(var_assign_count_cycle, variables, variables_width, constraint_sequence, s, inputs)
# write_new_inputs(result, variables_width)
# run_sim()
# coverage_sequence = read_coverage_pt_toggles(cycles, leaf_covid, current_coverage)
# print("Coverage Sequence : ", coverage_sequence)
#
#
##############################################################################
# add_constraints_to_solver(constraint_sequence)
# solution = solve_now(s)

# invert_constraints(constraint_sequence)
# if analyze_constraints(constraint_sequence):
#     add_variables_to_solver(var_assign_count_cycle, variables, variables_width)
#     add_constraints_to_solver(s, constraint_sequence)
#     solve_now(s)
#
# else:
#     # take next constraint

