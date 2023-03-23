import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

table1 = pd.read_csv("./data/table1.csv")
table2 = pd.read_csv("./data/table2.csv")

i_arr = list(table1.I.array)
t0_arr = list(table1.T0.array)
m_arr = list(table1.m.array)
t_arr = list(table2.TK.array)
sigma_arr = list(table2.Delta.array)

R = 0.35
l_e = 12
L_k = 187 * (10**(-6))
C_k = 268 * (10**(-6))
R_k = 0.25 # 200 0.02
U_co = 1400
i_0 = 3 #0.3
T_w = 2000
H = 1e-5#1e-5 # 1e-6 1e-4
H_1 = 1e-4
STEP = 1e-3
MAX_WITHOUT_R = 0.005 #819 * 1e-6
# MAX = 0.005
# MAX = 2e-5
MAX = 600e-6

t_res = []

def print_menu():
    print("1 - Euler")
    print("2 - Runge 2nd order")
    print("3 - Runge 4th order")
    print("4 - Runge 4th order, Rk+Rp=0")
    print("5 - Runge 4th order, Rk=200")
    print("0 - Everyting!")

def linear_interpolation_t0_m(i, i_arr, to_arr, m_arr):
    n = len(i_arr)
    j = 0

    if i < i_arr[0]:
        m = m_arr[0]
        to = to_arr[0]
        return to, m
    #elif i > i_arr[n - 1]:
    #    m = m_arr[n - 1]
    #    to = to_arr[n - 1]
    #    return to, m

    while True:
        if i_arr[j] > i or j == n - 2:
            break
        j += 1
    j -= 1

    if j < n - 1:
        dx = i_arr[j + 1] - i_arr[j]
        di = i - i_arr[j]
        to = to_arr[j] + ((to_arr[j + 1] - to_arr[j]) * di / dx)
        m = m_arr[j] + ((m_arr[j + 1] - m_arr[j]) * di / dx)
        # print(j, i, i_arr[j+1], i_arr[j])
    else:
        dx = i_arr[n - 1] - i_arr[n - 2]
        di = i - i_arr[n - 1]
        to = to_arr[n - 2] + ((to_arr[n - 1] - to_arr[n - 2]) * di / dx)
        m = m_arr[n - 1]

    if m < 0:
        print(i_arr[-1])
        # print(m, i, fl)
    return to, m


def find_sigma(t, t_arr, sigma_arr):
    n = len(t_arr)
    j = 0
    if t < t_arr[0]:
        sigma = sigma_arr[0]
        return sigma

    elif t > t_arr[n - 1]:
        sigma = sigma_arr[n]
        return sigma

    while True:
        if t_arr[j] > t or j == n - 2:
            break
        j += 1
    j -= 1

    # while j < n - 1 and t_arr[j] > t:
    #   j += 1

    if j < n - 1:
        dx = t_arr[j+1] - t_arr[j]
        di = t - t_arr[j]
        sigma = sigma_arr[j] + ((sigma_arr[j + 1] - sigma_arr[j]) * di / dx)
        # print(t, t_arr[j+1], t_arr[j])
    else:
        dx = t_arr[n - 1] - t_arr[n - 2]
        di = t - t_arr[n - 1]
        sigma = sigma_arr[n - 2] + ((sigma_arr[n - 1] - sigma_arr[n - 2]) * di / dx)

    return sigma

def di_dt(i: float, u: float, r_res: float, r_k=R_k):
    return (u - (r_k + r_res) * i) / L_k

def di_dt_without_r(i: float, u: float, r_res: float):
    return u / L_k

def phi(i: float):
    return -(i / C_k)

def t_func(t0: float, z: float, m: float):
    return t0 + (T_w - t0) * np.power(z, m)

def r_func(s):
    return l_e / (2 * np.pi * R * R * s)

def integral(arr1, arr2):
    l = len(arr1)
    s = 0
    for i in range(l - 1):
        s += ((arr2[i] + arr2[i + 1]) / 2) * (arr1[i + 1] - arr1[i])
    return s

def find_r(i: float):

    to, m = linear_interpolation_t0_m(i, i_arr, t0_arr, m_arr)
    t_arr2 = []
    sigma_arr2 = []
    z_arr = []
    z_value_arr = []
    h = STEP
    z = 0
    z_max = 1
    while z < z_max + h:
        t = t_func(to, z, m)
        sigma = find_sigma(t, t_arr, sigma_arr)
        t_arr2.append(t)
        sigma_arr2.append(sigma)
        z_arr.append(z)
        z_value_arr.append(sigma * z)
        z = z + h
    # s = integral(t_arr2, sigma_arr2)
    s = integral(z_arr, z_value_arr)
    r = r_func(s)
    return r

def euler(t0=0, t_max=0.01, step=H, r_k=R_k):
    i_n = i_0
    u_n = U_co
    t_n = t0

    t_res = [t0]
    i_res = [i_n]
    u_res = [u_n]
    r0 = find_r(i_n)
    t0, m = linear_interpolation_t0_m(i_n, i_arr, t0_arr, m_arr)
    r_res = [r0]
    t0_res = [t0]

    while t_n < t_max:
        k1 = step * di_dt(i_n, u_n, find_r(i_n), r_k=r_k)
        q1 = step * phi(i_n)

        t_n = t_n + step
        i_n = i_n + k1
        u_n = u_n + q1

        r_p = find_r(i_n)
        t0, m = linear_interpolation_t0_m(i_n, i_arr, t0_arr, m_arr)
        t_res.append(t_n)
        i_res.append(i_n)
        u_res.append(u_n)
        r_res.append(r_p)
        t0_res.append(t0)

    return t_res, i_res, u_res, r_res, t0_res

def runge_2_order(t0=0, t_max=0.01, beta=1/2, with_r=True, step=H, r_k=R_k):
    i_n = i_0
    u_n = U_co
    t_n = t0

    t_res = [t_n]
    i_res = [i_n]
    u_res = [u_n]
    r0 = find_r(i_n)
    t0, m = linear_interpolation_t0_m(i_n, i_arr, t0_arr, m_arr)
    r_res = [r0]
    t0_res = [t0]

    while t_n < t_max:
        k1 = step * di_dt(i_n, u_n, find_r(i_n), r_k=r_k)
        if not with_r:
            k1 = step * di_dt_without_r(i_n, u_n, find_r(i_n))
        q1 = step * phi(i_n)
        k2 = step * di_dt(i_n + k1 / (2 * beta), u_n + q1 / (2 * beta), find_r(i_n + k1 / (2 * beta)), r_k=r_k)
        if not with_r:
            k2 = step * di_dt_without_r(i_n + k1 / (2 * beta), u_n + q1 / (2 * beta), find_r(i_n + k1 / (2 * beta)))
        q2 = step * phi(i_n + k1 / (2 * beta))

        t_n = t_n + step
        i_n = i_n + (1 - beta) * k1 + beta * k2
        u_n = u_n + (1 - beta) * q1 + beta * q2

        r0 = find_r(i_n)

        t0, m = linear_interpolation_t0_m(i_n, i_arr, t0_arr, m_arr)

        t_res.append(t_n)
        i_res.append(i_n)
        u_res.append(u_n)
        r_res.append(r0)
        t0_res.append(t0)

    return t_res, i_res, u_res, r_res, t0_res

def runge_4_order(to=0, t_max=0.01, step=H, r_k=R_k):
    i_n = i_0
    u_n = U_co
    t_n = to

    t_res = [to]
    i_res = [i_n]
    u_res = [u_n]
    r0 = find_r(i_0)
    to, m = linear_interpolation_t0_m(i_0, i_arr, t0_arr, m_arr)
    r_res = [r0]
    to_res = [to]

    while t_n < t_max:
        r_1 = find_r(i_n)
        k1 = step * di_dt(i_n, u_n, r_1, r_k=r_k)
        q1 = step * phi(i_n)

        k2 = step * di_dt(i_n + k1 / 2, u_n + q1 / 2, find_r(i_n + k1 / 2), r_k=r_k)
        q2 = step * phi(i_n + k1 / 2)

        k3 = step * di_dt(i_n + k2 / 2, u_n + q2 / 2, find_r(i_n + k1 / 2), r_k=r_k)
        q3 = step * phi(i_n + k2 / 2)

        k4 = step * di_dt(i_n + k3, u_n + q3, find_r(i_n + k3), r_k=r_k)
        q4 = step * phi(i_n + k3)

        t_n = t_n + step
        i_n = i_n + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        u_n = u_n + (q1 + 2 * q2 + 2 * q3 + q4) / 6

        r_p = find_r(i_n)
        to, m = linear_interpolation_t0_m(i_n, i_arr, t0_arr, m_arr)

        t_res.append(t_n)
        i_res.append(i_n)
        u_res.append(u_n)
        r_res.append(r_p)
        to_res.append(to)

    return t_res, i_res, u_res, r_res, to_res


def main():
    print_menu()
    choice = int(input())
    if (choice == 0):
        x_res_euler, y_res_euler, z_res_euler, r_res_euler, t_res_euler = euler(0, MAX)
        ir_res_euler = [y_res_euler[i] * r_res_euler[i] for i in range(len(y_res_euler))]

        x_res_runge2, y_res_runge2, z_res_runge2, r_res_runge2, t_res_runge2 = runge_2_order(0, MAX)
        ir_res_runge2 = [y_res_runge2[i] * r_res_runge2[i] for i in range(len(y_res_runge2))]

        x_res_runge4, y_res_runge4, z_res_runge4, r_res_runge4, t_res_runge4 = runge_4_order(0, MAX)
        ir_res_runge4 = [y_res_runge4[i] * r_res_runge4[i] for i in range(len(y_res_runge4))]


        plt.plot(x_res_euler, y_res_euler, "green", label="Euler")
        plt.plot(x_res_runge2, y_res_runge2, "red", label="Runge 2nd order")
        plt.plot(x_res_runge4, y_res_runge4, "blue", label="Runge 4nd order")
        plt.legend(loc='best')
        plt.title("I(t)")
        plt.show()

        plt.plot(x_res_euler, z_res_euler, "green", label="Euler")
        plt.plot(x_res_runge2, z_res_runge2, "red", label="Runge 2nd order")
        plt.plot(x_res_runge4, z_res_runge4, "blue", label="Runge 4nd order")
        plt.legend(loc='best')
        plt.title("U(t)")
        plt.show()

        plt.plot(x_res_euler, r_res_euler, "green", label="Euler")
        plt.plot(x_res_runge2, r_res_runge2, "red", label="Runge 2nd order")
        plt.plot(x_res_runge4, r_res_runge4, "blue", label="Runge 4nd order")
        plt.legend(loc='best')
        plt.title("R_p(t)")
        plt.show()

        plt.plot(x_res_euler, ir_res_euler, "green", label="Euler")
        plt.plot(x_res_runge2, ir_res_runge2, "red", label="Runge 2nd order")
        plt.plot(x_res_runge4, ir_res_runge4, "blue", label="Runge 4nd order")
        plt.legend(loc='best')
        plt.title("I(t) * R_p(t)")
        plt.show()

        plt.plot(x_res_euler, t_res_euler, "green", label="Euler")
        plt.plot(x_res_runge2, t_res_runge2, "red", label="Runge 2nd order")
        plt.plot(x_res_runge4, t_res_runge4, "blue", label="Runge 4nd order")
        plt.legend(loc='best')
        plt.title("T(t)")
        plt.show()
    elif choice == 1:
        fig, axes = plt.subplots(nrows=2, ncols=3, sharex=False, sharey=False, figsize=(10, 10))
        ax1, ax2, ax3, ax4, ax5, ax6 = axes.flatten()

        x_res_euler, y_res_euler, z_res_euler, r_res_euler, t_res_euler = euler(0, MAX)
        ir_res_euler = [y_res_euler[i] * r_res_euler[i] for i in range(len(y_res_euler))]

        ax1.set_title("I(t)")
        ax1.plot(x_res_euler, y_res_euler, "green")
        ax2.set_title("U(t) RK1")
        ax2.plot(x_res_euler, z_res_euler, "red")
        ax3.set_title("Rp(t) RK1")
        ax3.plot(x_res_euler, r_res_euler, "blue")
        ax4.set_title("I(t) * Rp(t) RK1")
        ax4.plot(x_res_euler, ir_res_euler, "purple")
        ax5.set_title("T0(t) RK1")
        ax5.plot(x_res_euler, t_res_euler, "grey")
        plt.show()
    elif choice == 2:
        fig, axes = plt.subplots(nrows=2, ncols=3, sharex=False, sharey=False, figsize=(10, 10))
        ax1, ax2, ax3, ax4, ax5, ax6 = axes.flatten()

        x_res, y_res, z_res, r_res, t_res = runge_2_order(0, MAX)
        ir_res = [y_res[i] * r_res[i] for i in range(len(y_res))]

        ax1.set_title("I(t)")
        ax1.plot(x_res, y_res, "green")
        ax2.set_title("U(t) RK1")
        ax2.plot(x_res, z_res, "red")
        ax3.set_title("Rp(t) RK1")
        ax3.plot(x_res, r_res, "blue")
        ax4.set_title("I(t) * Rp(t) RK1")
        ax4.plot(x_res, ir_res, "purple")
        ax5.set_title("T0(t) RK1")
        ax5.plot(x_res, t_res, "grey")
        plt.show()

    elif choice == 3:
        fig, axes = plt.subplots(nrows=2, ncols=3, sharex=False, sharey=False, figsize=(10, 10))
        ax1, ax2, ax3, ax4, ax5, ax6 = axes.flatten()

        x_res, y_res, z_res, r_res, t_res = runge_4_order(0, MAX)
        ir_res = [y_res[i] * r_res[i] for i in range(len(y_res))]

        ax1.set_title("I(t)")
        ax1.plot(x_res, y_res, "green")
        ax2.set_title("U(t) RK1")
        ax2.plot(x_res, z_res, "red")
        ax3.set_title("Rp(t) RK1")
        ax3.plot(x_res, r_res, "blue")
        ax4.set_title("I(t) * Rp(t) RK1")
        ax4.plot(x_res, ir_res, "purple")
        ax5.set_title("T0(t) RK1")
        ax5.plot(x_res, t_res, "grey")
        plt.show()

    elif choice == 4:
        x_res_runge2, y_res_runge2, z_res_runge2, r_res_runge2, t_res_runge2 = runge_2_order(0, MAX_WITHOUT_R, with_r=False)
        ir_res_runge2 = [y_res_runge2[i] * r_res_runge2[i] for i in range(len(y_res_runge2))]

        plt.plot(x_res_runge2, y_res_runge2, "red", label="Runge 2nd order")
        plt.legend(loc='best')
        plt.title("I(t)")
        plt.show()

    elif choice == 5:
        x_res_euler, y_res_euler, z_res_euler, r_res_euler, t_res_euler = euler(0, 2e-5, step=1e-7, r_k=200)
        ir_res_euler = [y_res_euler[i] * r_res_euler[i] for i in range(len(y_res_euler))]

        x_res_runge2, y_res_runge2, z_res_runge2, r_res_runge2, t_res_runge2 = runge_2_order(0, 2e-5, step=1e-7, r_k=200)
        ir_res_runge2 = [y_res_runge2[i] * r_res_runge2[i] for i in range(len(y_res_runge2))]

        x_res_runge4, y_res_runge4, z_res_runge4, r_res_runge4, t_res_runge4 = runge_4_order(0, 2e-5, step=1e-7, r_k=200)
        ir_res_runge4 = [y_res_runge4[i] * r_res_runge4[i] for i in range(len(y_res_runge4))]


        plt.plot(x_res_euler, y_res_euler, "green", label="Euler")
        plt.plot(x_res_runge2, y_res_runge2, "red", label="Runge 2nd order")
        plt.plot(x_res_runge4, y_res_runge4, "blue", label="Runge 4nd order")
        plt.legend(loc='best')
        plt.title("I(t)")
        plt.show()









if __name__ == "__main__":
    main()