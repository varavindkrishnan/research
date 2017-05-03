from tree import *
from known_signals import relevant_ids

leaf_predicate ={}
leaf_covid = {}

node_predicate = {}
node_covid = {}

def _get_leaves_and_trace(nodes, predicate_list, cov_list):
    # need to add assignment to predicate list or create a new list for predicates
    this_covlist = cov_list[:] + [nodes.cov_id]
    this_predicatelist = predicate_list[:] + [nodes.predicate]

    for assigns in nodes.key:
        this_predicatelist = this_predicatelist[:] + [assigns]

    if len(nodes.children) == 0:
        leaf_covid[nodes.cov_id] = this_covlist[:]
        leaf_predicate[nodes.cov_id] = this_predicatelist[:]
        node_predicate[nodes.cov_id] = this_predicatelist[:]
        node_covid[nodes.cov_id] = this_covlist[:]
        return

    node_predicate[nodes.cov_id] = this_predicatelist[:]
    node_covid[nodes.cov_id] = this_covlist[:]


    for children in nodes.children:
        _get_leaves_and_trace(children, this_predicatelist, this_covlist)

    return


def get_leaves_and_trace(node_a):
    for nodes in node_a:
        assert isinstance(nodes, control_flow_tree)
        _get_leaves_and_trace(nodes, [], [])

    return leaf_covid, leaf_predicate


def extract_relevant_constraints(constraint_stack):
    # get all variables in the candidate constrain which is going to be inverted
    # use DDG plus branch ids, remove those variables that are not involved
    # if not input in the final list, cant really solve
    # Check for conflicts, ie, variable in the candidate constraint assigned values guarenteed not to satisfy
    # some values can be extracted directly from the simulator
    return


def constraints_from_coverage(list_cov_pts, predicate_of_leaves, variables, inputs, outputs):
    # from a given list of terminal branches construct the constraint stack
    # how to handle multiple assign and references to variables during the same cycle?
    # keep track of variables assigned in a given flow, if assigned track only the last assignment, if used then use
    # that assignment if not assigned use from prev cycle.
    # use defenition chains for multiple assigns in the same cycle <var_name>_<cycle_no>_<define_no>
    constraints = []
    cycle_number = 0
    var_assign_count_cycle = []
    for cycles in list_cov_pts:
        var_assign_count = {}
        initial_list = []
        if cycle_number > 0:
            for vars in variables:
                if (vars not in inputs) and (vars not in outputs):
                    line = ""
                    if vars in var_assign_count_cycle[cycle_number - 1]:
                        temp = str(var_assign_count_cycle[cycle_number - 1][vars])

                    else:
                        temp = "0"
                    line += vars + "_" + str(cycle_number) + "_0 == " + vars + "_" + str(cycle_number - 1) + "_" + temp
                    initial_list.append(line)

        constraints.append(initial_list)
        for nodes in cycles:
            if nodes not in leaf_covid:
                print("This node ", nodes, " is not a leaf node")
                assert False

            for predicates in predicate_of_leaves[nodes]:
                constraints[-1].append(predicates.get_string(cycle_number, 0, var_assign_count))

        cycle_number += 1
        var_assign_count_cycle.append(var_assign_count)

    return constraints, var_assign_count_cycle


def build_incremental_constraints(constraints, list, variables, inputs, outputs, cycle_number, curr_id, var_assign_count_cycle):
    initial_list = []
    assert cycle_number > 0

    for vars in variables:
        if (vars not in inputs) and (vars not in outputs):
            line = ""
            if vars in var_assign_count_cycle[cycle_number - 1]:
                temp = str(var_assign_count_cycle[cycle_number - 1][vars])

            else:
                temp = "0"
            line += vars + "_" + str(cycle_number) + "_0 == " + vars + "_" + str(cycle_number - 1) + "_" + temp
            initial_list.append(line)

    constraints.append(initial_list)
    var_assign_count = {}
    for predicates in node_predicate[curr_id]:
        constraints[-1].append(predicates.get_string(cycle_number, 0, var_assign_count))

    return constraints


def clock_reset_vars(inputs, file_name):
    f = open(file_name, 'r')
    lines = f.readlines()

    safe_inputs = []
    for vars in inputs:
        if vars not in lines:
            safe_inputs.append(vars)

    return safe_inputs


def take_next_constraint(list_cov_pts, constraints, nodeid_node_mapping, var_assign_count_cycle, variables, inputs, outputs):
    # This list_cov_pts includes all non leaf nodes in the trace also
    if(len(constraints) == 0):
        print("Empty stack")
        return None
    
    here_list = list_cov_pts[:]
    here_constraints = constraints[:]

    if len(here_list[-1]) == 0:
        here_list.pop(-1)
        here_constraints.pop(-1)
        var_assign_count_cycle.pop(-1)
        return take_next_constraint(here_list, here_constraints, nodeid_node_mapping, var_assign_count_cycle, variables, inputs, outputs)

    last_id = here_list[-1].pop(-1)

    here_constraints.pop(-1)

    if (nodeid_node_mapping[last_id].opposite_id is not None) and (last_id in relevant_ids):
        constraints = build_incremental_constraints(constraints, here_list, variables, inputs, outputs, len(here_list), nodeid_node_mapping[last_id].opposite_id, var_assign_count_cycle)

    else:
        take_next_constraint(here_list, here_constraints, nodeid_node_mapping, var_assign_count_cycle, variables, inputs, outputs)

    return constraints
