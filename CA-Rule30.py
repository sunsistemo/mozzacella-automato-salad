import random
import os
import sys
from time import sleep
from tqdm import trange
from optparse import OptionParser

import numpy as np
import matplotlib.pyplot as plt


STATE = None

def seed_gen(n=261):
    global STATE
    STATE = list(map(int, bin(int.from_bytes(os.urandom(n // 8 + 1), byteorder="little"))[2:][:n]))

def step(a, b, c):
    return a ^ (b or c)

def evolve_state():
    global STATE
    state = STATE
    newstate = [0] * len(state)
    newstate[0] = step(state[-1], state[0], state[1])
    for i in range(1, len(state) - 1):
        newstate[i] = step(state[i - 1], state[i], state[i + 1])
    newstate[-1] = step(state[-2], state[-1], state[0])
    STATE = newstate

def print_ca():
    global STATE
    seed_gen()
    for i in range(t):
        STATE = evolve_state()
        print("".join([str(i) for i in STATE]))
        sleep(0.2)

def randbit():
    global STATE
    evolve_state()
    return STATE[0]

def randint(a, b):
    """a and b are ints such that a < b."""
    interval = b - a
    is_power_of_two = sum(int(i) for i in bin(interval)[2:]) == 1
    if not is_power_of_two:
        print("So long sucker!")
        random_backup()
        sys.exit()
    num_bits = len(bin(interval)[2:]) - 1
    bits = [0] * num_bits
    for i in range(num_bits):
        bits[i] = randbit()
    return a + int("".join(map(str, bits)), 2)

def random_backup():
    import webbrowser
    webbrowser.open("http://random.org")

def generate_nums(n=int(1E4),b=32):
    nums = np.zeros(n)
    for i in trange(n):
        nums[i] = randint(0, b)
    return nums

def plot_uniform(nums, b):
    plt.hist(nums, bins=b)
    plt.show()

def frequency_test(nums, b):
    bin_nums = [x[2:].zfill(int.bit_length(b-1)) for x in list(map(bin,map(int,nums)))] # 
    num_ones  = 0
    num_zeros = 0
    for b in bin_nums:
        num_ones  += b.count("1")
        num_zeros += b.count("0")
    print("Frequency Test: [#0: %d], [#1: %d]" % (num_zeros, num_ones))
    
if __name__ == "__main__":
    parser = OptionParser()
    parser.set_defaults(num_gens=int(1E4))
    parser.add_option('-n', dest='num_gens',
                  help='Number of random numbers to generate')
    (options, args) = parser.parse_args()
        
    seed_gen()
    n = int(options.num_gens)
    b = 32
    nums = generate_nums(n, b)
    plot_uniform(nums, b)
    frequency_test(nums, b)
