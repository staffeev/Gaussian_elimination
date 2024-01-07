import numpy as np


if __name__ == "__main__":
    n, m = map(int, input("Введите количество уравнений и переменных через пробел: ").split())
    a = []
    b = []
    print("Вводите уравнения в формате 'a1 a2 ... am | b1', где ai - коэффициенты при переменных, bj - свободные члены")
    for i in range(n):
        *ai, _, bi = list(map(float, input().split()))
        a.append(ai)
        b.append([bi])
    A = np.array(a)
    b = np.array(b)
    print()
    debug_flag = 0 if input("Выводить решение? (1-да, 0-нет): ") == "0" else 1
    print()