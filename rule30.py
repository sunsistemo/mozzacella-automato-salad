import os
import sys
from time import sleep
from optparse import OptionParser


from builtins import int
try:
    from tqdm import trange
    import numpy as np
    import matplotlib.pyplot as plt
except ImportError:
    pass


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

def print_ca(size=100):
    global STATE
    seed_gen(size)
    while True:
        evolve_state()
        print("".join([str(i) for i in STATE]))
        sleep(0.02)

def randbit():
    global STATE
    evolve_state()
    return STATE[0]

def randint(a, b, num_bits=None):
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
        bits[i] = randbit()
    return a + int("".join(map(str, bits)), 2)

def random_backup():
    import webbrowser
    webbrowser.open("http://random.org")

def generate_nums(n=int(1E4), b=32):
    nums = [0] * n
    for i in trange(n):
        nums[i] = randint(0, b)
    return nums

def bytestream(a, b):
    num_bits = len(bin(b - a)[2:]) - 1
    num_bytes = num_bits // 8
    assert num_bits == 8 * num_bytes
    if sys.version_info.major >= 3:
        write = sys.stdout.buffer.write
    else:
        write = sys.stdout.write
    while True:
        write(randint(a, b, num_bits).to_bytes(num_bytes, byteorder="little"))

def bitstream():
    write = sys.stdout.write
    bitstring = {1: '1', 0: '0'}
    while True:
        bits = [bitstring[randbit()] for _ in range(8192)]
        write("".join(bits))

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

def main():
    parser = OptionParser()
    parser.set_defaults(num_gens=int(1E4))
    parser.add_option('-n', dest='num_gens',
                  help='Number of random numbers to generate')
    parser.add_option("-B", "--bytestream", action="store_true")
    parser.add_option("-b", "--bitstream", action="store_true")
    (options, args) = parser.parse_args()

    seed_gen()
    n = int(options.num_gens)
    b = 32
    if options.bytestream:
        return bytestream(0, 2 ** 8)
    elif options.bitstream:
        return bitstream()
    nums = generate_nums(n, b)
    plot_uniform(nums, b)
    frequency_test(nums, b)


if __name__ == "__main__":
    main()
