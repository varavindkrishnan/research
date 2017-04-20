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
