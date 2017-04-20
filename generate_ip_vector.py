from cfg import variables_width, inputs
from random import randrange

values = []


def generate_random_ip_vector(cycles = 100):
    for i in range(cycles):
        values.append({})
        for vars in inputs:
            this_width = variables_width[vars]
            values[i][vars] = randrange(0, 2**this_width)

    return values


def extract_relevant_constraints(constraint_stack):
    # get all variables in the candidate constrain which is going to be inverted
    # use DDG plus branch ids, remove those variables that are not involved
    # if not input in the final list, cant really solve
    # Check for conflicts, ie, variable in the candidate constraint assigned values guarenteed not to satisfy
    # some values can be extracted directly from the simulator
    return
