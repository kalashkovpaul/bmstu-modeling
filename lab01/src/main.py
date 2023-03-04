import math


MAX_X = 2.003
STEP  = 1e-4

def f_1(x, u):
	return x + u**2

def f_2(x, u):
    return u**2 + 2*u*x

def f_3(x, u):
	return x**2 + u**2

def analytical_solution_1(u):
    return 3*math.exp(u) - u**2 - 2*u - 2

def analytical_solution_2(u):
    return (u**2 + 1) / 2

# f_3 has no analytical solution :(

def picar_approx_1_1(u):
    return 1 + u + u**3 / 3

def picar_approx_1_2(u):
    return picar_approx_1_1(u) + u**2 / 2 + u**4 / 12

def picar_approx_1_3(u):
    return picar_approx_1_2(u) + u**3 / 6 + u**5 / 60

def picar_approx_1_4(u):
    return picar_approx_1_3(u) + u**4 / 24 + u**6 / 360


def picar_approx_2_1(u):
    return 0.5 + u**2 / 2 + u**4 / 4

def picar_approx_2_2(u):
    return picar_approx_2_1(u) + u**4 / 4 + u**6 / 12

def picar_approx_2_3(u):
    return picar_approx_2_2(u) + u**6 / 12 + u**8 / 48

def picar_approx_2_4(u):
    return picar_approx_2_3(u) + u**8 / 48 + u**10 / 240


def picar_approx_3_1(u):
	return u**3 / 3

def picar_approx_3_2(u):
	return picar_approx_3_1(u) + u**7 / 63

def picar_approx_3_3(u):
	return picar_approx_3_2(u) + 2*u**11 / 2079 + u**15 / 59535

def picar_approx_3_4(u):
    return picar_approx_3_3(u) + (2 / 93555)*u**15 + (2 / 3393495)*u**19 + \
        (2 / 2488563)*u** 19 + (2 / 86266215)*u**23 + (1 / 99411543)*u**23 + \
        (2 / 3341878155)*u**27 + (1 / 109876902975)*u**31


def picar(x_max, h, approx_fun):
	result = []
	x, u = 0, 0
	while abs(x) < abs(x_max):
		result.append(u)
		x += h
		u = approx_fun(x)
	return result


def euler(n, h, x, y, function):
    answer = []

    for i in range(n):
        try:
            y += h * function(x, y)
            answer.append(y)
            x += h
        except OverflowError:
            answer.append("Over")

    return answer

def format(number):
    if type(number) == float:
        if number > 1000000:
            return '{:.4e}'.format(number)
        return '{:.4f}'.format(number)

    elif type(number) == int:
        return str(number)
    else:
        return number

def task_1():
    x_start = 0
    x_end = 0.93
    h = 1e-6

    n = math.ceil(abs(x_end - x_start) / h) + 1
    output_step = int(n / 200)

    answer_euler = euler(n, h, 0, 1, f_1)
    print(
        "                                               Задание 1: таблица                                        ")
    print(
        "---------------------------------------------------------------------------------------------------------")
    print(
        "|         |    Метод     |     Метод     |__________________________Метод Пикара_________________________|")
    print(
        "|    x    |    Эйлера    |     Аналит    |               |               |               |               |")
    print(
        "|         |    явный     |               |   1-е прибл.  |   2-е прибл.  |   3-е прибл.  |   4-е прибл.  |")
    print(
        "---------------------------------------------------------------------------------------------------------")

    for i in range(0, n, output_step):
        print("|{:^9.2f}|{:^14s}|{:^15.5f}|{:^15.5f}|{:^15.5f}|{:^15.5f}|{:^15.5f}|".format(x_start,
            format(answer_euler[i]),
            analytical_solution_1(x_start),
            picar_approx_1_1(x_start),
            picar_approx_1_2(x_start),
            picar_approx_1_3(x_start),
            picar_approx_1_4(x_start)
        ))
        x_start += h * output_step
    print()

def task_2():
    x_start = 0
    x_end = 0.93
    h = 1e-6

    n = math.ceil(abs(x_end - x_start) / h) + 1
    output_step = int(n / 200)

    answer_euler = euler(n, h, 0, 0.5, f_2)
    print(
        "                                               Задание 2: таблица                                        ")
    print(
        "---------------------------------------------------------------------------------------------------------")
    print(
        "|         |    Метод     |     Метод     |__________________________Метод Пикара_________________________|")
    print(
        "|    x    |    Эйлера    |     Аналит    |               |               |               |               |")
    print(
        "|         |    явный     |               |   1-е прибл.  |   2-е прибл.  |   3-е прибл.  |   4-е прибл.  |")
    print(
        "---------------------------------------------------------------------------------------------------------")

    for i in range(0, n, output_step):
        print("|{:^9.2f}|{:^14s}|{:^15.5f}|{:^15.5f}|{:^15.5f}|{:^15.5f}|{:^15.5f}|".format(x_start,
            format(answer_euler[i]),
            analytical_solution_2(x_start),
            picar_approx_2_1(x_start),
            picar_approx_2_2(x_start),
            picar_approx_2_3(x_start),
            picar_approx_2_4(x_start)
        ))
        x_start += h * output_step
    print()

def task_3():
    x_start = 0
    x_end = 0.93
    h = 1e-6

    n = math.ceil(abs(x_end - x_start) / h) + 1
    output_step = int(n / 200)

    answer_euler = euler(n, h, 0, 0, f_3)
    print(
        "                                               Задание 3: таблица                                        ")
    print(
        "---------------------------------------------------------------------------------------------------------")
    print(
        "|         |    Метод     |     Метод     |__________________________Метод Пикара_________________________|")
    print(
        "|    x    |    Эйлера    |     Аналит    |               |               |               |               |")
    print(
        "|         |    явный     |               |   1-е прибл.  |   2-е прибл.  |   3-е прибл.  |   4-е прибл.  |")
    print(
        "---------------------------------------------------------------------------------------------------------")

    for i in range(0, n, output_step):
        print("|{:^9.2f}|{:^14s}|{:^15.5s}|{:^15.5f}|{:^15.5f}|{:^15.5f}|{:^15.5f}|".format(x_start,
            format(answer_euler[i]),
            "----",
            picar_approx_3_1(x_start),
            picar_approx_3_2(x_start),
            picar_approx_3_3(x_start),
            picar_approx_3_4(x_start)
        ))
        x_start += h * output_step
    print()


def main():
    try:
        task_num = int(input("Введите номер задания: "))
        if task_num == 1:
            task_1()
        elif task_num == 2:
            task_2()
        elif task_num == 3:
            task_3()
        else:
            raise Exception
    except:
        print("Зачем же вы такое вводите...")


if __name__ == "__main__":
	main()