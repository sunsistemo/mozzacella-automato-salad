import multiprocessing
import subprocess
from functools import partial
import random
import os
import sys
from time import time

import json
from optparse import OptionParser

from compare import python_random


def cook(num_bytes, num_colors, rule, command=None):
    if command is None:
        command = "python3 salad.py --bytestream -r %d -c %d | pv -S -s %d | ent -t" % (rule, num_colors, num_bytes)
    try:
        output = subprocess.check_output(command, shell=True)
    except (BrokenPipeError, IOError):
        pass
    output = output.decode("utf-8")
    output = output.split('\n')[:-1]
    headers, values = [d.split(',')[1:] for d in output]
    headers.insert(0, 'Rule')
    values.insert(0, rule)
    values = map(float, values)
    return {k: v for k, v in zip(headers, values)}

def main():
    parser = OptionParser()
    parser.set_defaults(num_bytes='500000', num_colors='2', sample_size='100')
    parser.add_option('-n', '--nbytes', dest='num_bytes',
                help='Number of bytes to stream to ent')
    parser.add_option('-c', '--color', dest='num_colors',
                help='Number of colors')
    parser.add_option('-s', '--sample-size', dest='sample_size',
                help='Number of rules to sample')
    parser.add_option('-p', '--python', dest='python', action="store_true",
                      help="Test Python's RNG.")
    parser.add_option('-u', '--urandom', dest='urandom', action="store_true",
                      help="Test the linux /dev/urandom RNG.")
    (options, args) = parser.parse_args()

    k = int(options.num_colors)
    num_bytes = int(options.num_bytes)

    if options.python:
        command = "python3 compare.py | pv -S -s %d | ent -t" % num_bytes
        data = cook(0, 0, 0, command=command)
        return write_data(data, "python_%d.json" % time())
    elif options.urandom:
        command = "cat /dev/urandom | pv -S -s %d | ent -t" % num_bytes
        data = cook(0, 0, 0, command=command)
        return write_data(data, "urandom_%d.json" % time())

    sample_size = int(options.sample_size)
    max_rule = (k ** (k ** 3)) - 1
    print("maxrule: %d" % max_rule)
    sample_rules = [random.randint(0, max_rule) for x in range(sample_size)]
    print(sample_rules)
    rands = [161, 225, 195, 101, 102, 135, 165, 105, 106, 75, 169, 45, 149, 86, 150, 120, 153, 90, 122, 60, 30]
    rands_paper = list(set([15, 30, 75, 90, 60, 105, 120, 150, 210, 240, 85, 149, 101, 165, 153, 105, 169, 150, 166, 170, 15, 135, 45, 165, 195, 105, 225, 150, 180, 240, 85, 86, 89, 90, 102, 105, 106, 150, 154, 170]))

    data = {}
    p = multiprocessing.Pool(os.cpu_count() // 2)
    rules = sample_rules
    func = partial(cook, num_bytes, k)
    output = p.map(func, rules)
    for i, d in enumerate(output):
        data[i] = d
    write_data(data, "results_%d.json" % time())


def write_data(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()
