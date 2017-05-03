from operator_types import *
# from cfg import variables


class variable_object:
    " object to hold variable name and cycle and UD annotation and value"
    def __init__(self, key):
        self.key = key
        self.value = {}
        self.ud = []

    def __repr__(self, cycle):
        return repr(self.key) + "_" + str(cycle) + " " + str(self.ud[cycle])

    def value_of_cycle_define(self, cycle, define, value):
        if cycle in self.value:
            self.value[cycle][define] = value

        else:
            self.value[cycle] = {}
            self.value[cycle][define] = value


class assign_tree:
    " assignment trees inside each node "
    def __init__(self, key=None, children = None, is_predicate = False):
        self.key = key
        self.children = []
        self.is_predicate = is_predicate
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

    def variables(self, variables, curr_list = None):
        if curr_list is None:
            curr_list = []

        if self.key in variables:
            if self.key not in curr_list:
                curr_list.append(self.key)

        for child in self.children:
            child.variables(variables, curr_list)

        return curr_list

    def is_const(self, variables):
        if len(self.children) == 0:
            if (self.key not in operators) and (self.key not in variables):
                return True

            elif self.key in variables:
                return False

            else:
                assert False

        elif len(self.children) == 1:
            return self.children[0].is_const(variables)

        else:
            if self.key in assigns:
                return self.children[1].is_const(variables)

            else:
                return self.children[0].is_const(variables) and self.children[1].is_const(variables)

    def is_bool(self):

        if self.key in comparators:
            return True

        else:
            if len(self.children) == 0:
                return False

            elif len(self.children) == 1:
                return self.children[0].is_bool()

            else:
                return self.children[0].is_bool() and self.children[0].is_bool()

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

        if ((self.key == "OR" or self.key =="AND") and self.is_bool()) or self.key == "NOR" or self.key == "NAND":

            if self.key == "OR":
                op = "Or"
                temp = op + "(" + self.children[0].get_string(cycle_number, 1,  var_assign_count) + "," + self.children[1].get_string(cycle_number, 1,  var_assign_count) + ")"
                return temp

            elif self.key == "AND":
                op = "And"
                temp = op + "(" + self.children[0].get_string(cycle_number, 1,  var_assign_count) + "," + self.children[1].get_string(cycle_number, 1,  var_assign_count) + ")"
                return temp

            elif self.key == "NOR":
                op = "Or"
                temp = op + "(" + self.children[0].get_string(cycle_number, 1,  var_assign_count) + "," + self.children[1].get_string(cycle_number, 1,  var_assign_count) + ")"
                return "Not(" + temp + ")"

            else:
                op = "And"
                temp = op + "(" + self.children[0].get_string(cycle_number, 1,  var_assign_count) + "," + self.children[1].get_string(cycle_number, 1,  var_assign_count) + ")"
                return "Not(" + temp + ")"

        if self.key not in comparators and level == 0:
            append_flag = True

        if self.key in transform:
            if self.key == "ASSIGNDLY":
                assign_dly = True

            elif self.key in assigns_blocking:
                blocking_assign_operator = True

            if self.key in assigns:
                assign_operator = True

            key = transform[self.key]

        else:
            key = self.key

        if len(self.children) == 2:

            if assign_operator:
                # assert self.children[0].key in variables
                if blocking_assign_operator:
                    right = self.children[1].get_string(cycle_number, 1,  var_assign_count) + ")"

                    if self.children[0].key not in var_assign_count:
                        var_assign_count[self.children[0].key] = 0

                    var_assign_count[self.children[0].key] += 1
                    # add here the count information to the constrain
                    ret = ret + "(" + self.children[0].get_string(cycle_number, 1, var_assign_count) + " " + key + " " + right

                elif assign_dly:
                    temp = {}
                    temp[self.children[0].key] = 0
                    ret = ret + "(" + self.children[0].get_string(cycle_number + 1, 1, temp) + " " + key + " " + \
                          self.children[1].get_string(cycle_number, 1,  var_assign_count) + ")"

                else:
                    assert False

            else:
                ret = ret + "(" + self.children[0].get_string(cycle_number, 1,  var_assign_count) + " " + key + " " + \
                      self.children[1].get_string(cycle_number, 1,  var_assign_count) + ")"

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

                if self.children[0].key not in var_assign_count:
                    var_assign_count[self.children[0].key] = 0

                ret = ret + "(" + self.children[0].key + "_" + str(cycle_number) + "_" + str(var_assign_count[self.children[0].key]) + ")"

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
                if key not in var_assign_count:
                    var_assign_count[key] = 0
                    return key + "_" + str(cycle_number) + "_" + str(var_assign_count[key]) + " != 0"

                else:
                    return key + "_" + str(cycle_number) + "_" + str(var_assign_count[key]) + " != 0"

            else:
                if key not in var_assign_count:
                    var_assign_count[key] = 0
                    return key + "_" + str(cycle_number) + "_" + str(var_assign_count[key])

                else:
                    return key + "_" + str(cycle_number) + "_" + str(var_assign_count[key])

        else:
            assert False
    #
    # def generate_Z3_constrain(self):
    #     # accept a dict var count which keeps track of blocking assigns to the var for one cycle for use define purpose
    #     # use new dict evey cycle
    #     # if two non blocking assings only the last one matters, this can be done when post processing
    #     assert isinstance(self, assign_tree)
    #     print(self)
    #     count = 0
    #     assign_dly = False
    #     blocking_assign_operator = False
    #     assign_operator = False
    #     ret = ""
    #     append_flag = False
    #     if var_assign_count is None:
    #         var_assign_count = {}
    #
    #     if ((self.key == "OR" or self.key =="AND") and self.is_bool()) or self.key == "NOR" or self.key == "NAND":
    #
    #         if self.key == "OR":
    #             op = "Or"
    #             temp = op + "(" + self.children[0].get_string(cycle_number, 1,  var_assign_count) + "," + self.children[1].get_string(cycle_number, 1,  var_assign_count) + ")"
    #             return temp
    #
    #         elif self.key == "AND":
    #             op = "And"
    #             temp = op + "(" + self.children[0].get_string(cycle_number, 1,  var_assign_count) + "," + self.children[1].get_string(cycle_number, 1,  var_assign_count) + ")"
    #             return temp
    #
    #         elif self.key == "NOR":
    #             op = "Or"
    #             temp = op + "(" + self.children[0].get_string(cycle_number, 1,  var_assign_count) + "," + self.children[1].get_string(cycle_number, 1,  var_assign_count) + ")"
    #             return "Not(" + temp + ")"
    #
    #         else:
    #             op = "And"
    #             temp = op + "(" + self.children[0].get_string(cycle_number, 1,  var_assign_count) + "," + self.children[1].get_string(cycle_number, 1,  var_assign_count) + ")"
    #             return "Not(" + temp + ")"
    #
    #     if self.key not in comparators and level == 0:
    #         append_flag = True
    #
    #     if self.key in transform:
    #         if self.key == "ASSIGNDLY":
    #             assign_dly = True
    #
    #         elif self.key in assigns_blocking:
    #             blocking_assign_operator = True
    #
    #         if self.key in assigns:
    #             assign_operator = True
    #
    #         key = transform[self.key]
    #
    #     else:
    #         key = self.key
    #
    #     if len(self.children) == 2:
    #
    #         if assign_operator:
    #             # assert self.children[0].key in variables
    #             if blocking_assign_operator:
    #                 right = self.children[1].get_string(cycle_number, 1,  var_assign_count) + ")"
    #
    #                 if self.children[0].key not in var_assign_count:
    #                     var_assign_count[self.children[0].key] = 0
    #
    #                 var_assign_count[self.children[0].key] += 1
    #                 # add here the count information to the constrain
    #                 ret = ret + "(" + self.children[0].get_string(cycle_number, 1, var_assign_count) + " " + key + " " + right
    #
    #             elif assign_dly:
    #                 temp = {}
    #                 temp[self.children[0].key] = 0
    #                 ret = ret + "(" + self.children[0].get_string(cycle_number + 1, 1, temp) + " " + key + " " + \
    #                       self.children[1].get_string(cycle_number, 1,  var_assign_count) + ")"
    #
    #             else:
    #                 assert False
    #
    #         else:
    #             ret = ret + "(" + self.children[0].get_string(cycle_number, 1,  var_assign_count) + " " + key + " " + \
    #                   self.children[1].get_string(cycle_number, 1,  var_assign_count) + ")"
    #
    #         if append_flag:
    #             ret = ret + " != 0"
    #
    #         return ret
    #
    #     elif len(self.children) == 1:
    #
    #         if key == "CCAST":
    #             if "\n" in self.children[0].key:
    #                 temp = self.children[0].key[:-1]
    #                 a, b = temp.split("h")
    #                 temp = str(int(b, 16))
    #                 ret = ret + "(" + temp + ")"
    #                 return ret
    #
    #             if self.children[0].key not in var_assign_count:
    #                 var_assign_count[self.children[0].key] = 0
    #
    #             ret = ret + "(" + self.children[0].key + "_" + str(cycle_number) + "_" + str(var_assign_count[self.children[0].key]) + ")"
    #
    #             if append_flag:
    #                 ret = ret + " != 0"
    #             return ret
    #
    #         else:
    #             ret = ret + "(" + key + "(" + self.children[0].get_string(cycle_number, 1) + "))"
    #             if append_flag:
    #                 ret = ret + " != 0"
    #             return ret
    #
    #     elif len(self.children) == 0:
    #         if "\n" in key:
    #             key = key[:-1]
    #             a, b = key.split("h")
    #             key = str(int(b, 16))
    #
    #             return key
    #
    #         if append_flag:
    #             if key not in var_assign_count:
    #                 var_assign_count[key] = 0
    #                 return key + "_" + str(cycle_number) + "_" + str(var_assign_count[key]) + " != 0"
    #
    #             else:
    #                 return key + "_" + str(cycle_number) + "_" + str(var_assign_count[key]) + " != 0"
    #
    #         else:
    #             if key not in var_assign_count:
    #                 var_assign_count[key] = 0
    #                 return key + "_" + str(cycle_number) + "_" + str(var_assign_count[key])
    #
    #             else:
    #                 return key + "_" + str(cycle_number) + "_" + str(var_assign_count[key])
    #
    #     else:
    #         assert False
    #
    # def get_predicate(self):
    #     return
    #

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
        self.opposite_id = None
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

    def get_nodeid_node_map(self, mapping):
        mapping[self.cov_id] = self
        for children in self.children:
            children.get_nodeid_node_map(mapping)


def swap_operator(ast_tree):
    assert isinstance(ast_tree, assign_tree)
    # print(ast_tree)

    if ast_tree.key in inversions:
        ast_tree.key = invert[ast_tree.key]

    else:
        if(ast_tree.key == "OR" or ast_tree.key =="AND") and ast_tree.is_bool():
            if ast_tree.key == "OR":
                ast_tree.key = "NOR"
                return

            else:
                ast_tree.key = "NAND"
                return

        new_node = assign_tree(ast_tree.key, ast_tree.children)
        new_node_2 = assign_tree("1'h0\n")
        ast_tree.key = "EQ"
        ast_tree.children = [new_node, new_node_2]


# TODO create variable object to hold variable, cycle and use define id, make it easier to check for conflict
# TODO in constrain
# TODO write constraint analyzer by checking assigns for variables which are on conflict
# TODO Have a dict for variables for easy look up ?
# TODO Move down constrain stack
# TODO post and pre assign buffer variables to be resolved
# TODO order of functions executed in _eval
# TODO Extent bit vec to make z3 happy
