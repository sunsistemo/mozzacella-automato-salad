import multiprocessing
import subprocess
import json


def cook(r):
    num_bytes = 50
    command = "python3 salad.py --bytestream -r %d | pv -S -s %d | ent -t" % (r, num_bytes)
    output = subprocess.check_output(command, shell=True)
    output = output.decode("utf-8")
    output = output.split('\n')[:-1]
    headers, values = [d.split(',')[1:] for d in output]
    values = map(float, values)
    return {k: v for k, v in zip(headers, values)}

def main():
    data = {}
    p = multiprocessing.Pool()
    rules = range(256)
    output = p.map(cook, rules)
    for i, d in enumerate(output):
        data[i] = d
    with open("results.json", "w") as f:
        json.dump(data, f)


if __name__ == "__main__":
    main()
