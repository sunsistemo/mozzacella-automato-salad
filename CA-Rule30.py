import random
import os
import sys
from time import sleep
from tqdm import trange

import numpy as np
import matplotlib.pyplot as plt


STATE = None

def seed_gen(n=261):
    global STATE
    STATE = list(bin(int.from_bytes(os.urandom(33), byteorder="little"))[2:][:n])

def step(a, b, c):
    return int(a) ^ (int(b) or int(c))

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

def plot_uniform():
    n = int(1E4)
    b = 32
    nums = np.zeros(n)
    for i in trange(n):
        nums[i] = randint(0, b)
    plt.hist(nums, bins=b)
    plt.show()

if __name__ == "__main__":
    seed_gen()
    plot_uniform()
