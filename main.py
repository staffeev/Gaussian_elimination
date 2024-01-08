import numpy as np
from solver_with_prints import *


if __name__ == "__main__":
    n, m = map(int, input("Введите количество уравнений и переменных через пробел: ").split())
    a = []
    b = []
    print("Вводите уравнения в формате 'a1 a2 ... am | b1', где ai - коэффициенты при переменных, bj - свободные члены")
    for i in range(n):
        *ai, _, bi = list(input().split())
        a.append(list(map(int, ai)))
        b.append([int(bi)])
    A = np.array(a, dtype=np.int64)
    b = np.array(b, dtype=np.int64)
    gaussian_elimination(A, b)
    exit = input("Нажмите Enter, чтобы закрыть программу")