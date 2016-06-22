import multiprocessing
import subprocess
from functools import partial

import json
from optparse import OptionParser

def cook(num_bytes, r):
    #print("r: %d, num_bytes: %d" % (r, num_bytes))
    command = "python3 salad.py --bytestream -r %d | pv -S -s %d | ent -t" % (r, num_bytes)
    try:
        output = subprocess.check_output(command, shell=True)
    except (CalledProcessError, BrokenPipeError, IOError):
        pass
    output = output.decode("utf-8")
    output = output.split('\n')[:-1]
    headers, values = [d.split(',')[1:] for d in output]
    headers.insert(0, 'Rule')
    values.insert(0, r)
    values = map(float, values)
    return {k: v for k, v in zip(headers, values)}

def main():
    parser = OptionParser()
    parser.set_defaults(num_bytes='500000')
    parser.add_option('-n', '--nbytes', dest='num_bytes',
                help='Number of bytes to stream to ent')
    (options, args) = parser.parse_args()
    
    rands = set([161, 225, 195, 101, 102, 135, 165, 105, 106, 75, 169, 45, 149, 86, 150, 120, 153, 90, 122, 60, 30])
        
    data = {}
    p = multiprocessing.Pool(4)
    #rules = range(256)
    rules = list(rands)
    func = partial(cook, int(options.num_bytes))
    output = p.map(func, rules)
    for i, d in enumerate(output):
        data[i] = d
    with open("results.json", "w") as f:
        json.dump(data, f)        

if __name__ == "__main__":
    main()
