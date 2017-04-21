from operator_types import *
from cfg import variables

class assign_tree:
    " assignment trees inside each node"
    def __init__(self, key=None, children = None):
        self.key = key
        self.children = []
        if children is not None:
            for child in children:
                assert isinstance(child, assign_tree)
                self.children.append(child)

    def __repr__(self):
        assert isinstance(self, assign_tree)
        if len(self.children) == 2:
            ret = "(" + repr(self.children[0]) + " " + repr(self.key) + " " + repr(self.children[1]) + ")"
            return ret

        elif len(self.children) == 1:
            ret = "(" + repr(self.key) + "(" + repr(self.children[0]) + "))"
            return ret

        elif len(self.children) == 0:
            return repr(self.key)

        else:
            assert False

    def get_string(self, cycle_number = 0, level = 0, var_assign_count = None):
        # accept a dict var count which keeps track of blocking assigns to the var for one cycle for use define purpose
        # use new dict evey cycle
        # if two non blocking assings only the last one matters, this can be done when post processing
        assert isinstance(self, assign_tree)
        count = 0
        assign_dly = False
        blocking_assign_operator = False
        assign_operator = False
        ret = ""
        append_flag = False
        if var_assign_count is None:
            var_assign_count = {}

        if self.key not in comparators and level == 0:
            append_flag = True

        if self.key in transform:
            if self.key == "ASSIGNDLY":
                assign_dly = True

            elif self.key == "ASSIGN":
                blocking_assign_operator = True

            if self.key in assigns:
                assign_operator = True

            key = transform[self.key]

        else:
            key = self.key

        if len(self.children) == 2:
            if assign_operator and blocking_assign_operator:
                assert self.children[0].key in variables
                if self.children[0].key in var_assign_count:
                    count = var_assign_count[self.children[0].key]

                if assign_dly:
                    ret = ret + "(" + self.children[0].get_string(cycle_number + 1, 1) + " " + key + " " + \
                          self.children[1].get_string(cycle_number, 1) + ")"

                else:
                    # ret = ret + "(" + self.children[0].get_string(cycle_number, 1) + " " + key + " " + \
                    #       self.children[1].get_string(cycle_number, 1) + ")"
                    ret = ret + "(" + self.children[0].get_string(cycle_number + 1, 1) + " " + key + " " + \
                          self.children[1].get_string(cycle_number, 1) + ")"

            else:
                ret = ret + "(" + self.children[0].get_string(cycle_number, 1) + " " + key + " " + \
                      self.children[1].get_string(cycle_number, 1) + ")"

            if append_flag:
                ret = ret + " != 0"

            return ret

        elif len(self.children) == 1:

            if key == "CCAST":
                if "\n" in self.children[0].key:
                    temp = self.children[0].key[:-1]
                    a, b = temp.split("h")
                    temp = str(int(b, 16))
                    ret = ret + "(" + temp + ")"
                    return ret

                if self.children[0].key in var_assign_count:
                    count = var_assign_count[self.children[0].key]
                    var_assign_count[self.children[0].key] += 1

                ret = ret + "(" + self.children[0].key + "_" + str(cycle_number) + ")"

                if append_flag:
                    ret = ret + " != 0"
                return ret

            else:
                ret = ret + "(" + key + "(" + self.children[0].get_string(cycle_number, 1) + "))"
                if append_flag:
                    ret = ret + " != 0"
                return ret

        elif len(self.children) == 0:
            if "\n" in key:
                key = key[:-1]
                a, b = key.split("h")
                key = str(int(b, 16))

                return key

            if append_flag:
                return key + "_" + str(cycle_number) + " != 0"

            else:
                return key + "_" + str(cycle_number)

        else:
            assert False


class control_flow_tree:
    " models if then else control flow "
    def __init__(self, predicate = None, state = True, key=None, children = None, cov_id = None):
        self.key = []
        for elements in key:
            assert isinstance(elements, assign_tree)
            self.key.append(elements)

        assert isinstance(predicate, assign_tree)
        self.predicate = predicate
        self.children = []
        self.state = state
        if children is not None:
            for child in children:
                assert isinstance(child, control_flow_tree)
                self.children.append(child)

        if cov_id is not None:
            assert isinstance(cov_id, int)
            self.cov_id = cov_id

        else:
            self.cov_id = None

    def __repr__(self, level = 0):
        ret = "\t" * level + repr(self.cov_id) + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret


def swap_operator(ast_tree):
    assert isinstance(ast_tree, assign_tree)
    # print(ast_tree)

    if ast_tree.key in inversions:
        ast_tree.key = invert[ast_tree.key]

    else:
        new_node = assign_tree(ast_tree.key, ast_tree.children)
        ast_tree.key = "NOT"
        ast_tree.children = [new_node]




