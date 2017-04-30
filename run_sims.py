from cfg import initialize_ckt_data
from generate_ip_vector import write_vector_to_file
from parse_tree import get_second_level, get_third_level, get_assign_tree, indent_level, get_last_level, get_token, get_width, get_var_type
from scan_file import get_operator, coverage_nu
from tree import control_flow_tree, swap_operator
from operator_types import *
from cfg_functions import *


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

node_a, variables, variables_width, inputs, outputs = initialize_ckt_data()


print_cfg(node_a)


for nodes in node_a:
    print(nodes)

a, b = get_leaves_and_trace(node_a[:2])

for keys in a:
    print(keys, " ", a[keys])
print("")

print("Input Vars")
for elements in inputs:
    print(elements, " : ", variables_width[elements])
print("")

for keys in b:
    print keys, " ",
    for elements in b[keys]:
        print(elements.get_string()), ", ",

    print(" ")

nodeid_node_mapping = {}
for node in node_a[:2]:
    node.get_nodeid_node_map(nodeid_node_mapping)


coverage_sequence = [28, 20, 5, 14, 2]

constraint_sequence, var_assign_count = constraints_from_coverage(coverage_sequence, b)

print("Constraints for node")

print(len(constraint_sequence))
for lines in constraint_sequence:
    print(lines)
