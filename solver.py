import numpy as np
from fractions import Fraction


def find_non_zero_row(matrix, cur_row, col):
    """Function to find row with non-zero element in `col`-th column"""
    for i in range(cur_row, matrix.shape[0]):
        if matrix[i][col] != 0:
            return i
    return -1


def get_row_echelon_form(matrix):
    """Function to get row-echelon form of matrix for
    Gaussian elimination method"""
    n, m = matrix.shape
    cur_row = 0
    for i in range(m):
        non_zero_row = find_non_zero_row(matrix, cur_row, i)
        if non_zero_row == -1:
            continue
        matrix[[cur_row, non_zero_row]] = matrix[[non_zero_row, cur_row]]
        matrix[cur_row] /= matrix[cur_row][i]
        for j in range(cur_row + 1, n):
            matrix[j] -= matrix[j][i] * matrix[cur_row]
        cur_row += 1
    
    return matrix


def check_if_any_solutuion_exists(matrix):
    """Funcion to find out if SLE has solutions"""
    for i in range(matrix.shape[0]):
        if np.count_nonzero(matrix[i]) == 1:
            return False
    return True


def find_non_basic_variables(matrix):
    """Function to find basic variables"""
    row = 0
    non_basic = []
    for col in range(matrix.shape[1] - 1):
        if matrix[row][col] != 0:
            row += 1
        else:
            non_basic.append(col)
    return non_basic


def back_substitution_for_one_solution(matrix):
    n = matrix.shape[0]
    x = np.zeros(n, dtype=np.int64) + Fraction()
    for m in range(n - 1, -1, -1):  # get roots
        x[m] = Fraction((matrix[m][-1] - np.dot(matrix[m][m:-1], x[m:])) / matrix[m][m])
    return x


def shift_columns_to_the_end(matrix, columns):
    wthoc = np.delete(matrix, columns, axis=1)
    wthc = -matrix[:, columns]
    return np.concatenate([wthoc, wthc], axis=1)


def back_substitution_for_infty_solutions(matrix, n, non_basic_variables):
    sm = shift_columns_to_the_end(matrix, non_basic_variables)
    sm = sm[np.any(sm != 0, axis=1)]
    
    m = sm.shape[0]
    for i in range(m - 2, -1, -1):
        for j in range(i + 1, m):
            sm[i] -= sm[i][j] * sm[j]

    return sm


def represent_root(coef, free_vars):
    ans = [str(coef[0])]
    for i, j in zip(coef[1:], free_vars):
        if i == 0:
            continue
        ans.append(f"({i})*x{j+1}")
    return " + ".join(ans)


def gaussian_elimination(A, b=None):
    """Function for finding solutions for SLE using Gussian elimintation method"""
    if b is None:
        ext_matrix = A.copy()
    else:
        ext_matrix = np.concatenate([A, b], axis=1)

    for i in ext_matrix:
        print(*i, sep="\t")
    print()
    ext_matrix = ext_matrix + Fraction()
    REM = get_row_echelon_form(ext_matrix)

    for i in REM:
        print(*i, sep="\t")
    print()

    if not check_if_any_solutuion_exists(REM):
        print("Решений нет!")
        return
    
    non_basic_variables = find_non_basic_variables(REM)
    if not non_basic_variables:
        print("Решение одно")
        roots = back_substitution_for_one_solution(REM)
        for i in range(REM.shape[0]):
            print(f"x{i+1} = {roots[i]}")
    else:
        print("Решений бесконечно много")
        print("Свободные переменные -", ", ".join([f"x{i+1}" for i in non_basic_variables]))
        coefs = back_substitution_for_infty_solutions(REM, REM.shape[1] - 1, non_basic_variables)
        basic_variables = [i for i in range(REM.shape[1] - 1) if i not in non_basic_variables]
        for i in range(coefs.shape[0]):
            root = represent_root(coefs[i][coefs.shape[1] - 1 - len(non_basic_variables):], non_basic_variables)
            print(f"x{basic_variables[i] + 1} = {root}")
    


if __name__ == "__main__":
    N, M = 4, 4 
    A = np.array(np.random.randint(1, 10,(N, M)), dtype=np.int64)
    b = np.array(np.random.randint(-10, 10,(N, 1)), dtype=np.int64)
    gaussian_elimination(A, b)