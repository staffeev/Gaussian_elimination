import numpy as np
from solver_with_prints import *


if __name__ == "__main__":
    n, m = map(int, input("Введите количество уравнений и переменных через пробел: ").split())
    a = []
    b = []
    print("Вводите уравнения в формате 'a1 a2 ... am | b1', где ai - коэффициенты при переменных, bj - свободные члены")
    for i in range(n):
        *ai, _, bi = list(input().split())
        a.append(list(map(float, ai)))
        b.append([float(bi)])
    A = np.array(a)
    b = np.array(b)
    gaussian_elimination(A, b)