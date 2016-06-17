import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from random import random, choice, randint
from gmpy2 import digits
from time import sleep
from optparse import OptionParser

latSize = 16
steps = 200
evoLat = np.zeros((latSize, steps))
init = np.zeros(latSize)

def gen_rule(r, k, ruleNum):
    rule = {}
    bruleNum = digits(ruleNum, k).zfill(k ** (2 * r + 1))[::-1]
    for s in range(k ** (2 * r + 1)):
        rule[digits(s, k).zfill(2 * r + 1)] = int(bruleNum[s])
    return rule

def CA_step(oldState, rule, r):
    newState = ["0"] * len(oldState)
    for n in range(r):
        newState[n] = str(rule[oldState[-r+n:] + oldState[:r+n+1]])
    for i in range(r, len(oldState) -  r):
        newState[i] = str(rule[oldState[i-r:i+r+1]])
    for m in range(1, r + 1):
        newState[-m] = str(rule[oldState[-r-m:] + oldState[:-m+r+1]])
    return "".join(newState)

def random_state(n, k):
    k = "".join(map(str, range(k)))
    return "".join([choice(k) for _ in range(n)])

def make_colormap(k):
    return {str(i): "\033[3%dm%d\033[0m" % (1 + i, i) for i in range(k)}

def CA_print(r=1, k=2, rule_number=-1, size=150):
    rule = gen_rule(r, k, rule_number)
    # print(rule)
    state = random_state(size, k)
    colormap = make_colormap(k)
    try:
        while True:
            pstate = "".join([colormap[c] for c in state])
            print(pstate)
            sleep(.1)
            state = CA_step(state, rule, r)
    except KeyboardInterrupt:
        print("Rule number: %d" % rule_number)

def init():
    ca_im.set_array(np.ma.array(window))
    return ca_im


def animate(frame_number):
    window[:-1] = window[1:]
    window[-1] = CA_step(state, rule, r)
    ca_im.set_array(window)
    return ca_im

def start_animation():
    ani = animation.FuncAnimation(fig, animate, None, init_func=init, interval=10, blit=True)
    plt.show()

def CA_show(r=1, k=2, rule_number=-1, size=150):
    global ca_im, window, ax, ax2, fig
    window = np.zeros((150, size))
    fig, (ax,ax2) = plt.subplots(1, 2)
    ca_im = ax.imshow(window)

    if rule_number < 0 or rule_number >= k**(k**(2*r + 1)):
        print("No proper rule number given for this CA setting, generating random rule...")
        sleep(2.5)
        rule_number = randint(0, k**(k**(2*r + 1)))
    rule = gen_rule(r, k, rule_number)
    state = random_state(size, k)
    try:
        start_animation()
    except KeyboardInterrupt:
        print("Rule number: %d" % rule_number)



if __name__ == "__main__":
    parser = OptionParser()
    parser.set_defaults(rule_number='30', num_neighbour='1', num_colors='2')
    parser.add_option('-r', '--rule', dest='rule_number',
                  help='Rule number to generate random number')
    parser.add_option('-n', '--neighbour', dest='num_neighbour',
                  help='Radius of neighbours')
    parser.add_option('-c', '--color', dest='num_colors',
                  help='Number of colors')
    (options, args) = parser.parse_args()

    rule_number = int(options.rule_number)
    r = int(options.num_neighbour)
    k = int(options.num_colors)

    if rule_number < 0 or rule_number >= k**(k**(2*r + 1)):
        print("No proper rule number given for this CA setting, generating random rule...")
        sleep(3)
        rule_number = randint(0, k**(k**(2*r + 1)))
    CA_print(r, k, rule_number)
