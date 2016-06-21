import multiprocessing
import subprocess
import json


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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
    for d in data:
        for k, v in variables.items():
            v.append(data[d][k])
    results = np.array([np.array(r) for r in results]).T
    headers = ["File-bytes", "Entropy", "Chi-square", "Mean", "Monte-Carlo-Pi", "Serial-Correlation"]
    return pd.DataFrame(results, columns=headers)

two = read_results("results-200ksamples.json")
five = read_results("results-500ksamples.json")

for d in (two, five):
    d["pi_deviation"] = np.abs(d["Monte-Carlo-Pi"] - np.pi)
    d["mean_deviation"] = np.abs(d["Mean"] - 255 / 2)


# plt.semilogy(x, Serial_Correlation)
# plt.plot(x, Serial_Correlation)
# plt.show()

if __name__ == "__main__":
    main()
