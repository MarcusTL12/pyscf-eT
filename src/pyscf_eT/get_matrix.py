import re
import numpy as np


def make_find_matrix_reg(name: str):
    name = name.replace('(', '\\(')
    name = name.replace(')', '\\)')
    return re.compile(f"{name}\\n  =+\\n(.+?)=+", re.S)


def get_matrix_string(name, outfile):
    with open(outfile, "r") as f:
        s = f.read()

    return re.search(make_find_matrix_reg(name), s).group(1)


block_reg = re.compile("(?: +\d+)+\n((?:.+\n)+)")
index_reg = re.compile(" (\d+) ")
num_reg = re.compile("-?\d+\.\d+")


def parse_matrix(matstring):
    h = 0
    mat = []

    for m in re.finditer(block_reg, matstring):
        blockstring = m.group(1)
        if h == 0:
            *_, mi = re.finditer(index_reg, blockstring)
            h = int(mi.group(1))

        numbers = np.array([float(m.group(0))
                   for m in re.finditer(num_reg, blockstring)])

        l = len(numbers)

        numbers = numbers.reshape((h, l // h))

        mat.extend(numbers.T.reshape(l))

    w = len(mat) // h

    return np.array(mat).reshape((w, h)).T


def get_matrix(name, outfile):
    return parse_matrix(get_matrix_string(name, outfile))
