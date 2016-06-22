import multiprocessing
import subprocess
import json


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
from scipy.stats import chisqprob
from gmpy2 import digits


def cook(r):
    num_bytes = 500000
    command = "python3 salad.py --bytestream -r %d | pv -S -s %d | ent -t" % (r, num_bytes)
    try:
        output = subprocess.check_output(command, shell=True)
    except (CalledProcessError, BrokenPipeError, IOError):
        pass
    output = output.decode("utf-8")
    output = output.split('\n')[:-1]
    headers, values = [d.split(',')[1:] for d in output]
    values = map(float, values)
    return {k: v for k, v in zip(headers, values)}

def main():
    data = {}
    p = multiprocessing.Pool(4)
    rules = range(256)
    output = p.map(cook, rules)
    for i, d in enumerate(output):
        data[i] = d
    with open("results.json", "w") as f:
        json.dump(data, f)


def read_results(filename):
    results = (File_bytes, Entropy, Chi_square, Mean, Monte_Carlo_Pi, Serial_Correlation) = [[] for _ in range(6)]
    with open(filename) as f:
        data = json.load(f)
    variables = {"File-bytes": File_bytes, "Entropy": Entropy, "Chi-square": Chi_square, "Mean": Mean,
                 "Monte-Carlo-Pi": Monte_Carlo_Pi, "Serial-Correlation": Serial_Correlation}
    for i in range(256):
        for k, v in variables.items():
            v.append(data[str(i)][k])
    results = np.array([np.array(r) for r in results]).T
    headers = ["File-bytes", "Entropy", "Chi-square",  "Mean", "Monte-Carlo-Pi", "Serial-Correlation"]
    return pd.DataFrame(results, columns=headers)

two = read_results("results-200ksamples.json")
five = read_results("results-500ksamples.json")

for d in (two, five):
    d["pi_deviation"] = np.abs(d["Monte-Carlo-Pi"] - np.pi)
    d["mean_deviation"] = np.abs(d["Mean"] - 255 / 2)
    d["p-value"] = chisqprob(d["Chi-square"], 255)
    d["rule"] = range(256)
    d["langton"] = [sum([int(b) for b in bin(v)[2:].zfill(8)])/8 for v in d["rule"]]

randp2 = two[(two["p-value"] > 0.1) &
             (two["p-value"] < 0.9 )]

randp5 = five[(five["p-value"] > 0.1) &
             (five["p-value"] < 0.9 )]

randchi2 = two[(two["Chi-square"] < 10**5 )]

randchi5 = five[(five["Chi-square"] < 10**5 )]
# Plot Entropy of all rules against the langton parameter
# ax1 = plt.gca()
# five.plot("langton", "Entropy", ax=ax1, kind="scatter", marker='o', alpha=.5, s=40)
# randp5.plot("langton", "Entropy", ax=ax1, kind="scatter", color="r", marker='o', alpha=.5, s=40)

print(set(randchi2.rule) - set(randp2.rule))
print(set(randchi5.rule) - set(randp5.rule))
print(set(randchi5.rule) - set(randchi2.rule))


ax2 = plt.gca()
randchi2.plot("langton", "Chi-square", ax=ax2, logy=True, kind="scatter", marker='o', alpha=.5, s=40)
randp2.plot("langton", "Chi-square", ax=ax2, logy=True, kind="scatter", color="r", marker='o', alpha=.5, s=40)

# plt.semilogy(x, Serial_Correlation)
# plt.plot(x, Serial_Correlation)
plt.show()

# The 1D CA rules that are random according to the paper
# "When are cellular automata random?" (http://stacks.iop.org/0295-5075/84/i=5/a=50005)
rands_paper = set([15, 30, 75, 90, 60, 105, 120, 150, 210, 240, 85, 149, 101, 165, 153, 105, 169, 150, 166, 170, 15, 135, 45, 165, 195, 105, 225, 150, 180, 240, 85, 86, 89, 90, 102, 105, 106, 150, 154, 170])

if __name__ == "__main__":
    main()
