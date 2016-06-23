import multiprocessing
import subprocess
from subprocess import CalledProcessError
from functools import partial
import random
import sys

import json
from optparse import OptionParser

from salad import StableError


def cook(num_bytes, num_colors, rule):
    command = "python3 salad.py --bytestream -r %d -c %d | pv -S -s %d | ent -t" % (rule, num_colors, num_bytes)
    try:
        output = subprocess.check_output(command, shell=True)
    except StableError:
        return None
    except (CalledProcessError, BrokenPipeError, IOError):
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
    (options, args) = parser.parse_args()

    k = int(options.num_colors)
    num_bytes = int(options.num_bytes)

    sample_size = int(options.sample_size)
    max_rule = (k**(k**3))-1
    print("maxrule: %d" % max_rule)
    sample_rules = [random.randint(0, max_rule) for x in range(sample_size)]
    #print(sample_rules[x if x>max_rule for x in sample_rules])
    print(sample_rules)
    #sys.exit()
    rands = [161, 225, 195, 101, 102, 135, 165, 105, 106, 75, 169, 45, 149, 86, 150, 120, 153, 90, 122, 60, 30]
    rands_paper = list(set([15, 30, 75, 90, 60, 105, 120, 150, 210, 240, 85, 149, 101, 165, 153, 105, 169, 150, 166, 170, 15, 135, 45, 165, 195, 105, 225, 150, 180, 240, 85, 86, 89, 90, 102, 105, 106, 150, 154, 170]))

    data = {}
    p = multiprocessing.Pool(4)
    rules = sample_rules
    func = partial(cook, num_bytes, k)
    output = p.map(func, rules)
    stable = 0                  # number of stable states found
    for i, d in enumerate(output):
        if d is not None:
            data[i] = d
        else:
            stable += 1
    data["stable_states"] = stable
    with open("results.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    main()
