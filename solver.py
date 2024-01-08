import numpy as np
from fractions import Fraction


def repr_matrix(matrix, msg=None):
    """Функция для вывода матрицы"""
    if msg is not None:
        print(msg)
        print()
    for i in matrix:
        print(*i, sep="\t")
    print()


def find_non_zero_row(matrix, cur_row, col):
    """Функция для нахождения строки не выше cur_row, где в столбце col 
    содержится ненулевой элемент"""
    for i in range(cur_row, matrix.shape[0]):
        if matrix[i][col] != 0:
            return i
    return -1


def get_row_echelon_form(matrix):
    """Функция для приведения матрицы к ступенчатому виду"""
    n, m = matrix.shape
    cur_row = 0
    for i in range(m):
        # Найдем строку с нунулевым элементом, чтоб вычитать ее из строк ниже
        non_zero_row = find_non_zero_row(matrix, cur_row, i)
        if non_zero_row == -1:
            continue
        # Поставим строку с ненулевым элементом на место текущей строки
        matrix[[cur_row, non_zero_row]] = matrix[[non_zero_row, cur_row]]
        # Поделим строку на число так, чтобы на диагонали был единичный элемент
        matrix[cur_row] /= matrix[cur_row][i]
        for j in range(cur_row + 1, n):
            # Из всех строк ниже текущей вычтем текущую, умноженную на коээфициент
            matrix[j] -= matrix[j][i] * matrix[cur_row]
        cur_row += 1
    
    return matrix


def check_if_any_solutuion_exists(matrix):
    """Функция для проверки наличия решений СЛАУ"""
    for i in range(matrix.shape[0]):
        # Если в приведенной матрцие есть строка вида 
        # '0 0 ... 0 | n', n != 0, то решений нет
        if np.count_nonzero(matrix[i]) == 1:
            return False
    return True


def find_non_basic_variables(matrix):
    """Функция для нахождения свободных переменных - тех, 
    которые не лежат на ступеньках матрицы"""
    n, m = matrix.shape
    m -= 1
    row = 0
    non_basic = []
    for col in range(m):
        if matrix[row][col] != 0:
            row += 1
        else:
            non_basic.append(col)
        if row == matrix.shape[0]: 
            # случай, когда уравнений меньше, чем переменных
            non_basic.extend(list(range(n, m)))
            break
    return non_basic


def back_substitution_for_one_solution(matrix):
    """Функция для нахождения корней, когда СЛАУ имеет единственное решение"""
    sm = matrix[np.any(matrix != 0, axis=1)]
    n = sm.shape[0]
    x = np.zeros(n, dtype=np.int64) + Fraction()
    for m in range(n - 1, -1, -1):
        # Обычное нахождение корней: переносим все известное в "правую часть" 
        x[m] = Fraction(sm[m][-1] - np.dot(sm[m][m:-1], x[m:]))
    return x


def shift_columns_to_the_end(matrix, columns):
    """Функция для перемещения определенных столбцов в конец матрицы.
    По сути это перемещение чисел в правую часть уравнений"""
    wthoc = np.delete(matrix, columns, axis=1)
    wthc = -matrix[:, columns]
    return np.concatenate([wthoc, wthc], axis=1)


def back_substitution_for_infty_solutions(matrix, n, non_basic_variables):
    """Функция для нахождения решения СЛАУ с бесконечным количеством решений"""
    # Перенесем свободные переменные в правую часть и оставим ненулевые строки
    sm = shift_columns_to_the_end(matrix, non_basic_variables)
    sm = sm[np.any(sm != 0, axis=1)]
    # Приведем матрицу так, чтобы "левая" часть (с неизвестными переменными) стала единичной
    m = sm.shape[0]
    for i in range(m - 2, -1, -1):
        for j in range(i + 1, m):
            sm[i] -= sm[i][j] * sm[j]

    return sm


def represent_root(coef, free_vars):
    """Функция, выводящая корень уравнения, зависящий от свободных переменных"""
    ans = [str(coef[0])]
    for i, j in zip(coef[1:], free_vars):
        if i == 0:
            continue
        sign = "-" if i < 0 else "+"
        elem = f"{abs(i)}*x{j+1}" if abs(i) != 1 else "x{j+1}"
        ans.extend([sign, elem])
    return " ".join(ans)


def gaussian_elimination(A, b=None):
    """Функция, решающая СЛАУ методов Гаусса"""
    if b is None:
        ext_matrix = A.copy()
    else:
        ext_matrix = np.concatenate([A, b], axis=1)

    ext_matrix = ext_matrix + Fraction()
    # Приведем матрицу к ступенчатому виду
    REM = get_row_echelon_form(ext_matrix)

    repr_matrix(REM, "Приведенная к ступенчатому виду матрциа:")

    # Проверка, есть ли решения у СЛАУ
    if not check_if_any_solutuion_exists(REM):
        print("Решений нет!")
        return
    
    # Найдем свободные переменные
    non_basic_variables = find_non_basic_variables(REM)
    if not non_basic_variables:
        # Если свободных переменных нет, то решение одно
        print("Решение одно")
        roots = back_substitution_for_one_solution(REM)
        for i in range(len(roots)):
            print(f"x{i+1} = {roots[i]}")
    else:
        # Если свободные переменные есть, то решений бесконечно много
        print("Решений бесконечно много")
        print("Свободные переменные -", ", ".join([f"x{i+1}" for i in non_basic_variables]))
        coefs = back_substitution_for_infty_solutions(REM, REM.shape[1] - 1, non_basic_variables)
        basic_variables = [i for i in range(REM.shape[1] - 1) if i not in non_basic_variables]
        for i in range(coefs.shape[0]):
            root = represent_root(coefs[i][coefs.shape[1] - 1 - len(non_basic_variables):], non_basic_variables)
            print(f"x{basic_variables[i] + 1} = {root}")
    


if __name__ == "__main__":
    N, M = 2, 2
    A = np.array(np.random.randint(1, 10,(N, M)), dtype=np.int64)
    b = np.array(np.random.randint(-100, 100, (N, 1)), dtype=np.int64)
    # A = np.array([
    #     [3, 2, -5, -1],
    #     [2, -1, 3, 13],
    #     [1, 2, -1, 9],
    #     [12, 8, -20, -4]
    # ])
    gaussian_elimination(A, b)