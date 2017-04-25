from random import randrange

values = []


def generate_random_ip_vector(variables_width, inputs, cycles = 100):
    for i in range(cycles):
        values.append({})
        for var in inputs:
            this_width = variables_width[var]
            values[i][var] = randrange(0, 2**this_width)

    return values


def write_vector_to_file(values, name, variables_width, inputs):
    f = open(name, 'w')
    for i in range(len(values)):
        line = ""
        for var in inputs:
            string = ""
            temp = values[i][var]
            width = variables_width[var]
            while temp > 0:
                if temp % 2 == 1:
                    string = "1" + string

                else:
                    string = "0" + string

                temp /= 2

            while len(string) < width:
                string = "0" + string

            line = line + string

        line += "\n"
        f.write(line)

    return


def read_coverage_pt_toggles(name, cycles, leaves_dict):
    f = open(name, 'r')
    lines = f.readlines()
    assert len(lines) == cycles

    leaves_cycle = []
    for i in range(cycles):
        leaves_cycle.append([])
        toggles = lines[i].split(',')
        for keys in leaves_dict:
            if toggles[keys] == 1:
                leaves_cycle[-1].append(keys)

    return leaves_cycles
