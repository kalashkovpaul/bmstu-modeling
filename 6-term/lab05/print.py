import matplotlib.pyplot as plt
# from coefs import *
import numpy

READFILE = "14.txt"


def readfile(filename):
    f = open(filename, 'r')
    x0, z0, a, b, beta, N, M, tau = list(map(float, f.readline().split()))
    matrix = []
    for line in f.readlines():
        s = list(map(float, line.split()))
        matrix.append(s)
    f.close()
    return x0, z0, a, b, beta, N, M, tau, matrix



x0, z0, a, b, beta, N, M, tau, matrix = readfile(READFILE)
M = int(M)
N = int(N)
h_x = a / N
h_z = b / M
x = [i * h_x for i in range(int(N) + 1)]
z = [i * h_z for i in range(int(M) + 1)]
X, Z = numpy.meshgrid(x, z)
Y = numpy.array(numpy.matrix(matrix))
ax = plt.axes(projection='3d')
ax.plot_surface(Z, X, Y, color='red')
ax.set_xlabel('X')
ax.set_ylabel('Z')
ax.set_zlabel('Y(x, z)')
plt.show()

while True:
    n = int(input(f'Введите относительную целочисленную координату x от 0 до {N} (0 - {0}см, {N} - {x0}см) для среза (-1 - выход): '))
    if n == -1:
        break
    plt.plot(z, matrix[n])
    plt.ylabel(f'Y({n / N * x0:2.2f}, z)')
    plt.xlabel('z')
    plt.show()


while True:
    m = int(input(f'Введите относительную целочисленную координату z от 0 до {M} (0 - {0}см, {M} - {z0}см) для среза (-1 - выход): '))
    if m == -1:
        break
    plt.plot(x, [line[m] for line in matrix])
    plt.ylabel(f'Y(x, {m / M * z0})')
    plt.xlabel('x')
    plt.show()