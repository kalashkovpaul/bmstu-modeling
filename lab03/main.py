from math import *
from util import *
from numpy import arange
import pandas as pd
import prettytable
import matplotlib.pyplot as plt

step = 1e-6


def show_graph(plot, name):
    plot.legend()
    plot.grid()
    plt.ylabel(name)
    plt.xlabel("z, б/р")

    plt.show()

def graph():
    fig = plt.figure(figsize=(10, 7))
    plot = fig.add_subplot()
    plot.plot(z_sp, T_sp,  label = "T", c = 'r')
    show_graph(plot, "Температура T, K")
    return

def main():
    graph()

main()