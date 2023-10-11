from math import *
from prettytable import PrettyTable
import matplotlib.pyplot as plt

EPS = 1e-9

def read_table(filename):
    f = open(filename, "r")
    string = f.readline()
    lst = [[float(i)] for i in string[:-1].split()]
    string = f.readline()
    while string:
        columns = string[:-1].split()
        for i, column in enumerate(columns):
            lst[i].append(float(column))
        string = f.readline()
    f.close()
    return lst


def get_diff(table):
    if (len(table[0])) == 1:
        return table[1][0]
    else:
        return (get_diff([table[0][:-1], table[1][:-1]]) - get_diff([table[0][1:], table[1][1:]])) / (table[0][0] - table[0][-1])


def newton(x, coeffs, nodes, y0):
    y = y0
    elem = 1
    i = 0
    while i < (len(coeffs) if x > nodes[1] else len(coeffs) - 2) and abs(elem * coeffs[i]) > EPS:
        elem *= (x - nodes[i])
        y += elem * coeffs[i]
        i += 1
    return y


# -------------------------------------------------------------------
def choose_dots(x, dot_list, n):
    if n > len(dot_list):
        return []
    else:
        before = n // 2
        after = n - before
        arr = []
        last = 0
        for i in range(len(dot_list)):
            if dot_list[i][0] < x:
                last = i
            else:
                break


        if (last + 1) < before:
            before = last + 1
            after = n - before           
        elif (len(dot_list) - last - 1) < after:
            after = len(dot_list) - last - 1
            before = n - after

        for i in dot_list[last - before + 1 : last + after + 1]:
            arr.append(i)
        return arr


def newton_polinome(table, x):
    y = 0
    multiplier = 1
    for i in range(1, len(table[0])):
        y += multiplier * table[0][i]
        # print(y) 
        multiplier *= x - table[i - 1][0]
    return y


def newton_interpol(input_list, x, n):
    # sorted_list = sorted(input_list, key = lambda x: x[0])
    arr = choose_dots(x, input_list, n)
    if len(arr) != n:
        return None, None
    newton_table = make_newton_table(arr)

    # print_newt_table(newton_table)
    return newton_polinome(newton_table, x)

def make_newton_table(dot_arr):
    n = len(dot_arr)
    m = len(dot_arr) + 1
    table  = [0] * n
    for i in range(n):
        table[i] = [0] * m
    for i in range(n):
        table[i][0] = dot_arr[i][0]
        table[i][1] = dot_arr[i][1]
    for j in range(2, n + 1):
        for i in range(n - j + 1):
            table[i][j] = (table[i][j - 1] - table[i + 1][j - 1]) / (table[i][0] - table[i + (j - 1)][0])
    return table

def load_dots_from_file(filename, ind = 1):
    try:
        f = open(filename)
    except:
        print("File doesn't exist")
        return []
    dots = []
    line = f.readline()
    if ind == 1:
        while line:
            try:
                x, y = map(float, line.split())
                dots.append([log(x), log(y), x, y])
                # dots.append([x, y, x, y])
            except:
                print("File wasn't properly read")
                break
            line = f.readline()
    f.close()
    return dots





# -------------------------------------------------------------------


def write_coeffs(filename, coeffs):
    f = open(filename, "w")
    for coef in coeffs:
        f.write(f'{coef}\n')
    f.close()


def read_coefs(filename):
    f = open(filename, "r")
    lst = [float(i[:-1]) for i in f.readlines()]
    f.close()
    return lst


def linerial(x, table):
    i = 0
    while table[0][i] > x:
        i += 1
    if i == 0:
        return table[1][0]
    return table[1][i - 1] + (table[1][i] - table[1][i - 1]) / (table[0][i] - table[0][i - 1]) * (x - table[0][i - 1])


# -----------------------------------------------------------------

def main():
    table_1 = read_table("table_1.txt")
    table_2 = read_table("table_2.txt")

    for i in range(len(table_1[0])):
        table_1[0][i] = log(table_1[0][i])
        table_1[1][i] = log(table_1[1][i])

    coeffs = []
    for i in range(1, len(table_1[0])):
        coeffs.append(get_diff([table_1[0][:i + 1], table_1[1][:i + 1]]))
    write_coeffs('coef_1_1.txt', coeffs)


    step = (table_1[0][-1] - table_1[0][0]) / 100
    i = table_1[0][0]
    x = []
    y = []
    while i <= table_1[0][-1]:
        x.append(i)
        y.append(newton(i, coeffs, table_1[0], table_1[1][0]))
        i += step

    for i in range(len(table_1[0])):
        table_1[0][i] = exp(table_1[0][i])
        table_1[1][i] = exp(table_1[1][i])


    for i in range(len(x)):
        x[i] = exp(x[i])
        y[i] = exp(y[i])

    # plt.plot(table_1[0], table_1[1])
    # plt.plot(x, y, color='green')
    # plt.show()



    #######################################################

    for i in range(len(table_2[0])):
        table_2[0][i] = log(table_2[0][i])
        table_2[1][i] = log(table_2[1][i])


    print(table_2[0], '\n', table_2[1])
    coeffs = []
    for i in range(1, len(table_2[0])):
        coeffs.append(get_diff([table_2[0][:i + 1], table_2[1][:i + 1]]))
    write_coeffs('coef_2.txt', coeffs)

    step = (table_2[0][-1] - table_2[0][0]) / 100
    i = table_2[0][0]
    x = []
    y = []
    while i <= table_2[0][-1]:
        x.append(i)
        y.append(newton(i, coeffs, table_2[0], table_2[1][0]))
        i += step
    print(x, '\n', y)

    for i in range(len(table_2[0])):
        table_2[0][i] = exp(table_2[0][i])
        table_2[1][i] = exp(table_2[1][i])


    for i in range(len(x)):
        x[i] = exp(x[i])
        y[i] = exp(y[i])

    plt.plot(table_2[0], table_2[1])
    plt.plot(x, y, color='green')
    plt.show()
    print(table_2[0], '\n', table_2[1])




if __name__ == "__main__":
    main()
