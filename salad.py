from time import sleep
from optparse import OptionParser
import sys

import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import random, choice
from gmpy2 import digits

from rule30 import random_backup


latSize = 16
steps = 200
evoLat = np.zeros((latSize, steps))
init = np.zeros(latSize)

STATE = None

def gen_rule(r, k, ruleNum):
    rule = {}
    bruleNum = digits(ruleNum, k).zfill(k ** (2 * r + 1))[::-1]
    for s in range(k ** (2 * r + 1)):
        rule[digits(s, k).zfill(2 * r + 1)] = int(bruleNum[s])
    return rule

def step(rule, r):
    global STATE
    oldState = STATE
    newState = ["0"] * len(oldState)
    for n in range(r):
        newState[n] = str(rule[oldState[-r+n:] + oldState[:r+n+1]])
    for i in range(r, len(oldState) - r):
        newState[i] = str(rule[oldState[i-r:i+r+1]])
    for m in range(1, r + 1):
        newState[-m] = str(rule[oldState[-r-m:] + oldState[:-m+r+1]])
    STATE = "".join(newState)

def random_state(n, k):
    k = "".join(map(str, range(k)))
    return "".join([choice(k) for _ in range(n)])

def make_colormap(k):
    return {str(i): "\033[3%dm%d\033[0m" % (1 + i, i) for i in range(k)}

def CA_print(r=1, k=2, rule_number=-1, size=150):
    global STATE
    rule = gen_rule(r, k, rule_number)
    # print(rule)
    STATE = random_state(size, k)
    colormap = make_colormap(k)
    try:
        while True:
            pstate = "".join([colormap[c] for c in STATE])
            print(pstate)
            sleep(.1)
            step(rule, r)
    except KeyboardInterrupt:
        print("Rule number: %d" % rule_number)

def randbit(rule, r):
    global STATE
    step(rule, r)
    return int(STATE[0])

def randint(a, b, rule, r, num_bits=None):
    """a and b are ints such that a < b."""
    if num_bits is None:
        interval = b - a
        is_power_of_two = sum(int(i) for i in bin(interval)[2:]) == 1
        if not is_power_of_two:
            print("So long sucker!")
            random_backup()
            sys.exit()
        num_bits = len(bin(interval)[2:]) - 1
    bits = [0] * num_bits
    for i in range(num_bits):
        bits[i] = randbit(rule, r)
    return a + int("".join(map(str, bits)), 2)

# Future randint function for any interval (not power of two) and multiple colors
def randintk(a, b, rule, k = 2, r = None, num_bits=None):
    """a and b are ints such that a < b."""
    if num_bits is None:
        interval = b - a
        num_bits = math.ceil(math.log(interval,2))
    bits = [0] * num_bits
    if r is None:
        r = (len(list(rule.keys())[0]) - 1)//2
    rand = interval
    while rand >= interval:
        for i in range(num_bits):
            bits[i] = randbit(rule, r)
        rand = int("".join(map(str, bits)), 2)
    return a + rand

def bitstream(r, k, rule_number):
    rule = gen_rule(r, k, rule_number)
    write = sys.stdout.write
    bitstring = {1: '1', 0: '0'}   # this is 4x faster than str !!!

    while True:
        bits = [bitstring[randbit(rule, r)] for _ in range(1024)]
        write("".join(bits))

def bytestream(r, k, rule_number):
    a, b = 0, 2 ** 8
    num_bits = len(bin(b - a)[2:]) - 1
    num_bytes = num_bits // 8
    assert num_bits == 8 * num_bytes
    rule = gen_rule(r, k, rule_number)
    if sys.version_info.major >= 3:
        write = sys.stdout.buffer.write
    else:
        write = sys.stdout.write

    while True:
        try:
            write(bytearray([randint(a, b, rule, r, num_bits) for _ in range(2 ** 12)]))
        except (BrokenPipeError, IOError):
            sys.stderr.close()
            sys.exit(1)


def main():
    global STATE
    parser = OptionParser()
    parser.set_defaults(rule_number='30', num_neighbour='1', num_colors='2')
    parser.add_option('-r', '--rule', dest='rule_number',
                  help='Rule number to generate random number')
    parser.add_option('-n', '--neighbour', dest='num_neighbour',
                  help='Radius of neighbours')
    parser.add_option('-c', '--color', dest='num_colors',
                  help='Number of colors')
    parser.add_option("-B", "--bytestream", action="store_true")
    parser.add_option("-b", "--bitstream", action="store_true")
    (options, args) = parser.parse_args()

    rule_number = int(options.rule_number)
    r = int(options.num_neighbour)
    k = int(options.num_colors)
    n = 261
    STATE = random_state(n, k)

    if options.bytestream:
        return bytestream(r, k, rule_number)
    elif options.bitstream:
        return bitstream(r, k, rule_number)

    if rule_number < 0 or rule_number >= k**(k**(2*r + 1)):
        print("No proper rule number given for this CA setting, generating random rule...")
        sleep(3)
        rule_number = randint(0, k**(k**(2*r + 1)))
    CA_print(r, k, rule_number)

if __name__ == "__main__":
    main()
