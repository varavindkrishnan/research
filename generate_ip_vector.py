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


