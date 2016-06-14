import numpy as np
from random import random, choice, randint
from gmpy2 import digits
from time import sleep


latSize = 16
steps = 200
evoLat = np.zeros((latSize,steps))
init = np.zeros(latSize)

def gen_rule(r, k, ruleNum):
    rule = {}
    bruleNum = digits(ruleNum,k).zfill(k**(2*r + 1))[::-1]
    for s in range(k**(2*r + 1)):
        rule[digits(s,k).zfill(2*r + 1)] = int(bruleNum[s])
    return rule

def CA_step(oldState, rule):
    newState = ["0"] * len(oldState)
    newState[0] = str(rule[oldState[-1] + oldState[:2]])
    for i in range(1,len(oldState)-1):
        newState[i] = str(rule[oldState[i-1:i+2]])
    newState[-1] = str(rule[oldState[-2:] + oldState[0]])
    return "".join(newState)

def random_state(n,k):
    k = "".join(map(str, range(k)))
    return "".join([choice(k) for _ in range(n)])

def make_colormap(k):
    return {str(i): "\033[3%dm%d\033[0m" % (1 + i, i) for i in range(k)}

if __name__ == "__main__":
    k = 6
    r = 1
    rule_number = randint(0, k**(k**(2*r + 1)))
    rule = gen_rule(1, k, rule_number)
    state = random_state(150, 2)
    colormap = make_colormap(k)
    try:
        while True:
            pstate = "".join([colormap[c] for c in state])
            print(pstate)
            sleep(.1)
            state = CA_step(state, rule)
    except KeyboardInterrupt:
        print("Rule number: %d" % rule_number)
