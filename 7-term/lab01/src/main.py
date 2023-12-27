import matplotlib.pyplot as plt
import numpy as np
from math import factorial, exp


def even_distribution(a, b, x):
    if a <= x < b:
        return (x - a) / (b - a)
    elif x < a:
        return 0
    else:
        return 1


def even_density(a, b, x):
    if a <= x <= b:
        return 1 / (b - a)
    else:
        return 0


def erlang_density(l, k, x):
    if x < 0:
        return 0
    return ((l ** k) * (x ** (k - 1)) * exp(-l * x)) / factorial(k - 1)


def erlang_distribution(l, k, x):
    if x < 0:
        return 0
    sum = 0
    for i in range(0, int(k)):
        sum += (exp(-l * x) * ((l * x) ** i)) / factorial(i)
    return 1 - sum


def erlang_second_bound(l, k):
    second_bound = 0
    while erlang_distribution(l, k, second_bound) < 0.999:
        second_bound += 1
    return second_bound + 1

def equal(a, b, step):
    diff = b - a
    val1 = a - diff / 2
    val2 = b + diff / 2

    even_x = np.arange(-15, 15, step)
    even_data_distribution = [even_distribution(a, b, val) for val in even_x]
    even_data_density = [even_density(a, b, val) for val in even_x]

    return even_x, even_data_distribution, even_data_density

def erlang(l, k, step):
    second_bound = erlang_second_bound(l, k)

    erlang_x = np.arange(0, second_bound, step)
    erlang_data_distribution = [erlang_distribution(l, k, val) for val in erlang_x]
    erlang_data_density = [erlang_density(l, k, val) for val in erlang_x]

    return erlang_x, erlang_data_distribution, erlang_data_density

if __name__ == "__main__":
    x0, dist0, dens0 = equal(0, 3, 1e-3)
    x1, dist1, dens1 = equal(-5, 5, 1e-3)
    x2, dist2, dens2 = equal(-10, 10, 1e-3)

    plt.figure(figsize=(14, 5))
    plt.subplot(121)
    plt.plot(x0, dist0, color="green", label='a = 0, b = 5')
    plt.plot(x1, dist1, color="red", label='a = -5, b = 5')
    plt.plot(x2, dist2, color="blue", label='a = -10, b = 10')
    plt.title('График функции распределения для \nравномерного распределения')
    plt.xlabel('x')
    plt.ylabel('F(x)')
    plt.grid(True)
    plt.legend()

    plt.subplot(122)
    plt.plot(x0, dens0, color="green", label='a = 0, b = 5')
    plt.plot(x1, dens1, color="red", label='a = -5, b = 5')
    plt.plot(x2, dens2, color="blue", label='a = -10, b = 10')
    plt.title('График функции плотности распределения для \nравномерного распределения')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)

    plt.legend()
    plt.show()

    x0, dist0, dens0 = erlang(3, 3, 1e-3)
    x1, dist1, dens1 = erlang(3, 4, 1e-3)
    x2, dist2, dens2 = erlang(4, 10, 1e-3)

    plt.figure(figsize=(14,5))
    plt.subplot(121)
    plt.plot(x0, dist0, color="green", label='lambda = 3, k = 3')
    plt.plot(x1, dist1, color="red", label='lambda = 3, k = 4')
    plt.plot(x2, dist2, color="blue", label='lambda = 4, k = 10')
    plt.title('График функции распределения\n для распределения Эрланга')
    plt.xlabel('x')
    plt.ylabel('F(x)')
    plt.grid(True)
    plt.legend()

    plt.subplot(122)
    plt.plot(x0, dens0, color="green", label='lambda = 3, k = 3')
    plt.plot(x1, dens1, color="red", label='lambda = 3, k = 4')
    plt.plot(x2, dens2, color="blue", label='lambda = 4, k = 10')
    plt.title('График функции плотности распределения\n для распределения Эрланга')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid(True)
    plt.legend()

    plt.show()