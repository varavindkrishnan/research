from random import randrange
from subprocess import call
from known_signals import *
values = []


def vector_resize(values, cycles, inputs, variables_width):
    start_len = len(values)
    while len(values) < cycles:
        values.append({})


    for i in range(start_len, cycles):
        for var in inputs:
            this_width = variables_width[var]
            values[i][var] = randrange(0, 2**this_width)
            if var in resets:

                # if i == 0 or i == cycles - 1:
                if i == 0:
                    values[i][var] = 2**this_width - 1

                else:
                    values[i][var] = 0

    return


def generate_random_ip_vector(variables_width, inputs, cycles = 100):
    for i in range(cycles):
        values.append({})
        for var in inputs:
            this_width = variables_width[var]
            values[i][var] = randrange(0, 2**this_width)

            if var in resets:

                # if i == 0 or i == cycles - 1:
                if i == 0:
                    values[i][var] = 2**this_width - 1

                else:
                    values[i][var] = 0

    return values


def write_vector_to_file(values, variables_width, inputs):
    f = open("./bench/lev_vec.vec", 'w')
    total_width = 0
    for keys in inputs:
        if keys not in clocks:
            total_width += variables_width[keys]

    # print("Total width is : ", total_width)
    f.write(str(total_width) + "\n")

    for i in range(len(values)):
        line = ""
        for var in inputs:
            if var not in resets_and_clocks:
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

        for var in resets:
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

    f.write("END")
    return


def read_coverage_pt_toggles(cycles, leaves_dict, current_coverage):
    f = open("./bench/coverage_cycle.trace", 'r')
    lines = f.readlines()
    assert len(lines) == cycles

    leaves_cycle = []
    for i in range(cycles):
        leaves_cycle.append([])
        toggles = lines[i][:-2].split(',')

        for q in range(len(toggles)):
            toggles[q] = int(toggles[q])
            current_coverage[toggles[q]] = 1

        for keys in leaves_dict:
            if keys in toggles:
                leaves_cycle[-1].append(keys)

    return leaves_cycle


def run_sim():
    call(["./bench/get_sim_trace.o", "-libpath", "./bench/b11.so"])


def write_new_inputs(values, variables_width):
    inputs = input_order[:]
    f = open("./bench/lev_vec.vec", 'w')
    total_width = 0
    for keys in inputs:
        if keys not in clocks:
            total_width += variables_width[keys]

    # print("Total width is : ", total_width)
    f.write(str(total_width) + "\n")

    for i in range(len(values)):
        line = ""
        for var in inputs:
            if var not in clocks:
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

    f.write("END")
    return
