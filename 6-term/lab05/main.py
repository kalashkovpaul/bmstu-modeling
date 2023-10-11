from math import *
from interpolation import *
from numpy import arange
from coefs import *


SAVEFILE = "14.txt"


def lambda_nm(y_nm):
    # return lambda_const
    return a1 * (b1 + c1 * y_nm ** m1)


def lambda_streak_nm(y_nm):
    # return 0
    return a1 * c1 * m1 * y_nm ** (m1 - 1)


def u_streak_x_nm(n, m, y, h_x):
    return (y[n + 1][m] - y[n][m]) / h_x


def u_streak_z_nm(n, m, y, h_z):
    return (y[n][m + 1] - y[n][m]) / h_z


def f1(n, m, y, h_x):
    return lambda_streak_nm(y[n][m]) * u_streak_x_nm(n, m, y, h_x) ** 2


def f2(n, m, y, h_z):
    return lambda_streak_nm(y[n][m]) * u_streak_x_nm(n, m, y, h_z) ** 2


def f(n, m, h_x, h_z):
    return f0 * exp(-beta * ((n * h_x - x0) ** 2 + (m * h_z - z0) ** 2))


def F(n, m, y, h_x, h_z):
    return f1(n, m, y, h_x) + f2(n, m, y, h_z) + f(n, m, h_x, h_z)


def get_A_line(h_x, h_z, last_matrix, m, current_vector):
    A = [0] * (N + 1)
    for n in range(N):
        A[n] = lambda_nm(current_vector[n]) / (h_x ** 2)
    A[N] = lambda_nm(current_vector[N]) / h_x
    return A


def get_B_line(h_x, h_z, last_matrix, m, current_vector):
    B = [0] * (N + 1)
    B[0] = -lambda_nm(current_vector[0]) / h_x
    for n in range(N):
        B[n] = 1 / (0.5 * tau) + 2 * lambda_nm(current_vector[n]) / (h_x ** 2)
    B[N] = alpha2 + lambda_nm(current_vector[N]) / h_x
    return B


def get_C_line(h_x, h_z, last_matrix, m, current_vector):
    C = [0] * (N + 1)
    C[0] = -lambda_nm(current_vector[0]) / h_x
    for n in range(N):
        C[n] = lambda_nm(current_vector[n]) / (h_x ** 2)
    return C


def get_D_line(h_x, h_z, last_matrix, m, current_vector):
    D = [0] * (N + 1)
    D[0] = -F0
    for n in range(N):
        D[n] = F(n, m, last_matrix, h_x, h_z) + last_matrix[n][m] / (0.5 * tau) + lambda_nm(current_vector[n]) / (h_z ** 2) * (last_matrix[n][m - 1] - 2 * last_matrix[n][m] + last_matrix[n][m + 1])
    D[N] = alpha2 * u0
    return D


def get_A_hat(h_x, h_z, last_matrix, n, current_vector):
    A = [0] * (M + 1)
    for m in range(M):
        A[m] = lambda_nm(current_vector[m]) / (h_z ** 2)
    A[m] = lambda_nm(current_vector[M]) / h_z
    return A


def get_B_hat(h_x, h_z, last_matrix, n, current_vector):
    B = [0] * (M + 1)
    B[0] = -(lambda_nm(current_vector[0]) / h_z + alpha3)
    for m in range(M):
        B[m] = 1 / (0.5 * tau) + 2 * lambda_nm(current_vector[m]) / (h_z ** 2)
    B[M] = alpha4 + lambda_nm(current_vector[M]) / h_z
    return B


def get_C_hat(h_x, h_z, last_matrix, n, current_vector):
    C = [0] * (M + 1)
    C[0] = -lambda_nm(current_vector[0]) / h_z
    for m in range(M):
        C[m] = lambda_nm(current_vector[m]) / (h_z ** 2)
    return C


def get_D_hat(h_x, h_z, last_matrix, n, current_vector):
    D = [0] * (M + 1)
    D[0] = alpha3 * u0
    for m in range(M):
        D[m] = F(n, m, last_matrix, h_x, h_z) + last_matrix[n][m] / (0.5 * tau) + lambda_nm(current_vector[m]) / (h_x ** 2) * (last_matrix[n - 1][m] - 2 * last_matrix[n][m] + last_matrix[n + 1][m])
    D[M] = alpha4 * u0
    return D


def calc_slae(A, B, C, D):
    size = len(A) - 1
    ksi = [0] * (size + 1)
    eta = [0] * (size + 1)
    ys1 = [0] * (size + 1)
    for n in range(size):
        low = B[n] - A[n] * ksi[n]
        ksi[n + 1] = C[n] / low
        eta[n + 1] = (D[n] + A[n] * eta[n]) / low
    ys1[size] = (A[size] * eta[size] + D[size]) / (B[size] - A[size] * ksi[size])
    for n in range(size, 0, -1):
        ys1[n - 1] = ksi[n] * ys1[n] + eta[n]
    return ys1


# def integration(ys, z):
#     s = 0.5 * (k_t(ys[0]) * z[0] * (ys[0] ** 4 - T0 ** 4) + k_t(ys[N]) * z[N] * (ys[N] ** 4 - T0 ** 4))
#     for n, z_n in enumerate(z[1:N]):
#         s += z_n * k_t(ys[n]) * (ys[n] ** 4 - T0 ** 4)
#     return (z[1] - z[0]) * s


def check_vector(last, result):
    n = 0
    fl = True
    while n < len(last) and fl:
        fl = abs((result[n] - last[n]) / last[n]) < EPS1
        n += 1
    if fl:
        # f1 = r0 * F0 - R * alpha * (ys[N] - T0)
        # f2 = 4 * np ** 2 * sigma * R ** 2 * integration(ys, z)
        # if f1 == 0 or abs((f1 - f2) / f1) < EPS2:
            # print(f'f1={f1}\nf2={f2}')
        return True
    return False

def check_matrix(last, result):
    n = 0
    m = 0
    fl = True
    # while n < len(last) and fl:
    summarize = 0
    while n < len(last):
        m = 0
        # while m < len(last[0]) and fl:
        while m < len(last[0]):
            fl = fl and abs((result[n][m] - last[n][m]) / last[n][m]) < EPS1
            if abs((result[n][m] - last[n][m]) / last[n][m]) > EPS1:
                # print(n, m)
                summarize += 1
            m += 1
        n += 1
    print(f'Сумма {summarize} {100 * summarize / ((N + 1) * (M + 1)):2.2f}%')
    if fl:
        # f1 = r0 * F0 - R * alpha * (ys[N] - T0)
        # f2 = 4 * np ** 2 * sigma * R ** 2 * integration(ys, z)
        # if f1 == 0 or abs((f1 - f2) / f1) < EPS2:
            # print(f'f1={f1}\nf2={f2}')
        return True
    return False


def save(matrix, filename):
    f = open(filename, "w")
    f.write(f'{x0} {z0} {a} {b} {beta} {N} {M} {tau}\n')
    for string in matrix:
        for elem in string:
            f.write(f'{elem} ')
        f.write('\n')
    f.close()


#++ инициализация сеточной функции
h_x = a / N
h_z = b / M
x = [i * h_x for i in range(N + 1)]
z = [i * h_z for i in range(M + 1)]

#++ инициализация значений сеточной функции
result_matrix = [0] * (N + 1) ## новый слой
last_matrix = [0] * (N + 1) ## старый слой
tmp_matrix = [0] * (N + 1) ## промежуточный слой
for n in range(N + 1):
    result_matrix[n] = [u0] * (M + 1)
    last_matrix[n] = [u0 - 1] * (M + 1)
    tmp_matrix[n] = [u0] * (M + 1)
#-- инициализация значений сеточной функции
#-- инициализация сеточной функции

t = 0
while not check_matrix(last_matrix, result_matrix):
    #++ копирование старых значений функции
    for n in range(N + 1):
        for m in range(M + 1):
            # result_matrix[n][m] = (last_matrix[n][m] + result_matrix[n][m]) / 2
            last_matrix[n][m] = result_matrix[n][m]
    #-- копирование старых значений функции
    #++ прогонка для m от 1 до M - 1
    for m in range(1, M):
        #++ метод простой итерации
        current_vector = [0] * (N + 1)
        for n in range(N + 1):
            current_vector[n] = last_matrix[n][m]
        while True:
            #++ прогонка для определённого m
            A_line = get_A_line(h_x, h_z, last_matrix, m, current_vector)
            B_line = get_B_line(h_x, h_z, last_matrix, m, current_vector)
            C_line = get_C_line(h_x, h_z, last_matrix, m, current_vector)
            D_line = get_D_line(h_x, h_z, last_matrix, m, current_vector)
            tmp_vector = calc_slae(A_line, B_line, C_line, D_line)
            #-- прогонка для определённого m

            #++ выход из простой итерации
            if check_vector(current_vector, tmp_vector):
                break
            #-- выход из простой итерации

            #++ новое стартовое значение для простой итерации
            for n in range(N + 1):
                current_vector[n] = (tmp_vector[n] + current_vector[n]) / 2
            #-- новое стартовое значение для простой итерации
        for n in range(N + 1):
            tmp_matrix[n][m] = current_vector[n]
        #-- метод простой итерации
    #-- прогонка для m от 1 до M - 1
    #++ расчёт значений при m = 0 через краевое условие
    for n in range(N + 1):
        #++ минипрогонка
        y_current = last_matrix[n][0]
        while True:
            y_tmp = (alpha3 * u0 + lambda_nm(y_current) / h_z * tmp_matrix[n][1]) / (alpha3 + lambda_nm(y_current) / h_z)
            if abs((y_current - y_tmp) / y_current) < EPS1:
                break
            y_current = (y_current + y_tmp) / 2
        #-- минипрогонка
        tmp_matrix[n][0] = y_current
    #-- расчёт значений при m = 0 через краевое условие
    #++ расчёт значений при m = M через краевое условие
    for n in range(N + 1):
        #++ минипрогонка
        y_current = last_matrix[n][M]
        while True:
            y_tmp = (alpha4 * u0 + lambda_nm(y_current) / h_z * tmp_matrix[n][M - 1]) / (alpha4 + lambda_nm(y_current) / h_z)
            if abs((y_current - y_tmp) / y_current) < EPS1:
                break
            y_current = (y_current + y_tmp) / 2
        #-- минипрогонка
        tmp_matrix[n][M] = y_current
    #-- расчёт значений при m = M через краевое условие


    #++ прогонка для n от 1 до N - 1
    for n in range(1, N):
        #++ метод простой итерации
        current_vector = [0] * (M + 1)
        for m in range(M + 1):
            current_vector[m] = last_matrix[n][m]
        while True:
            #++ прогонка для определённого n
            A_hat = get_A_hat(h_x, h_z, tmp_matrix, n, current_vector)
            B_hat = get_B_hat(h_x, h_z, tmp_matrix, n, current_vector)
            C_hat = get_C_hat(h_x, h_z, tmp_matrix, n, current_vector)
            D_hat = get_D_hat(h_x, h_z, tmp_matrix, n, current_vector)
            tmp_vector = calc_slae(A_hat, B_hat, C_hat, D_hat)
            #-- прогонка для определённого n

            #++ выход из простой итерации
            if check_vector(current_vector, tmp_vector):
                break
            #-- выход из простой итерации

            #++ новое стартовое значение для простой итерации
            for m in range(M + 1):
                current_vector[m] = (tmp_vector[m] + current_vector[m]) / 2
            #-- новое стартовое значение для простой итерации
        for m in range(M + 1):
            result_matrix[n][m] = current_vector[m]
        #-- метод простой итерации
    #-- прогонка для n от 1 до N - 1
    #++ расчёт значений при n = 0 через краевое условие
    for m in range(M + 1):
        #++ минипрогонка
        y_current = tmp_matrix[0][m]
        while True:
            y_tmp = (F0 + lambda_nm(y_current) / h_x * result_matrix[1][m]) / (lambda_nm(y_current) / h_x)
            if abs((y_current - y_tmp) / y_current) < EPS1:
                break
            y_current = (y_current + y_tmp) / 2
        #-- минипрогонка
        result_matrix[0][m] = y_current
    #-- расчёт значений при n = 0 через краевое условие
    #++ расчёт значений при n = N через краевое условие
    for m in range(M + 1):
        #++ минипрогонка
        y_current = tmp_matrix[N][m]
        while True:
            y_tmp = (alpha2 * u0 + lambda_nm(y_current) / h_x * result_matrix[N - 1][m]) / (alpha2 + lambda_nm(y_current) / h_x)
            if abs((y_current - y_tmp) / y_current) < EPS1:
                break
            y_current = (y_current + y_tmp) / 2
        #-- минипрогонка
        result_matrix[N][m] = y_current
    #-- расчёт значений при n = N через краевое условие

    print(t)
    #++ шаг по времени
    t += tau
    #-- шаг по времени
save(result_matrix, SAVEFILE)