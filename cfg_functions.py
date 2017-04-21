from tree import *

leaf_predicate ={}
leaf_covid = {}


def _get_leaves_and_trace(nodes, predicate_list, cov_list):
    # need to add assignment to predicate list or create a new list for predicates
    this_covlist = cov_list[:] + [nodes.cov_id]
    this_predicatelist = predicate_list[:] + [nodes.predicate]

    for assigns in nodes.key:
        this_predicatelist = this_predicatelist[:] + [assigns]

    if len(nodes.children) == 0:
        leaf_covid[nodes.cov_id] = this_covlist[:]
        leaf_predicate[nodes.cov_id] = this_predicatelist[:]
        return

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


def constraints_from_coverage(list):
    # from a given list of terminal branches construct the constraint stack
    # how to handle multiple assign and references to variables during the same cycle?
    # keep track of variables assigned in a given flow, if assigned track only the last assignment, if used then use
    # that assignment if not assigned use from prev cycle.
    # use defenition chains for multiple assigns in the same cycle <var_name>_<cycle_no>_<define_no>
    constraints = []
    cycle_number = 0
    for nodes in list:
        if nodes not in leaf_covid:
            print("This node ", nodes, " is not a leaf node")
            assert False

        for predicates in leaf_predicate[nodes]:
            constraints.append(predicates.get_string(cycle_number))

        cycle_number += 1

    return constraints
