import multiprocessing
import subprocess
from functools import partial

import json
from optparse import OptionParser

def cook(num_bytes, num_colors, rule):
    command = "python3 salad.py --bytestream -r %d -c %d | pv -S -s %d | ent -t" % (rule, num_colors, num_bytes)
    try:
        output = subprocess.check_output(command, shell=True)
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
    parser.set_defaults(num_bytes='500000', num_colors='2')
    parser.add_option('-n', '--nbytes', dest='num_bytes',
                help='Number of bytes to stream to ent')
    parser.add_option('-c', '--color', dest='num_colors',
                help='Number of colors')
    (options, args) = parser.parse_args()
    
    rands = [161, 225, 195, 101, 102, 135, 165, 105, 106, 75, 169, 45, 149, 86, 150, 120, 153, 90, 122, 60, 30]
    rands_paper = list(set([15, 30, 75, 90, 60, 105, 120, 150, 210, 240, 85, 149, 101, 165, 153, 105, 169, 150, 166, 170, 15, 135, 45, 165, 195, 105, 225, 150, 180, 240, 85, 86, 89, 90, 102, 105, 106, 150, 154, 170]))
    
    data = {}
    p = multiprocessing.Pool(4)
    rules = rands
    func = partial(cook, int(options.num_bytes), int(options.num_colors))
    output = p.map(func, rules)
    for i, d in enumerate(output):
        data[i] = d
    with open("results.json", "w") as f:
        json.dump(data, f)        

if __name__ == "__main__":
    main()
