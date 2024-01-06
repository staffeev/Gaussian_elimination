import numpy as np

def gaussian_elimintation(matrix):
    """Function to solve system of linear equations using
    Gaussian elimination method"""
    n = matrix.shape[0]
    for i in range(0, n):  # transform into an upper-triangular matrix
        for j in range(i + 1, n):
            coef = matrix[j][i] / matrix[i][i]
            matrix[j] -= coef * matrix[i]
    
    x = np.zeros(n)
    for m in range(n - 1, -1, -1):  # get roots
        x[m] = (matrix[m][-1] - (matrix[m][m:-1] * x[m:]).sum()) / matrix[m][m]

    return x


if __name__ == "__main__":
    matrix = np.array([
        [1, 2, 3, 1],
        [1, 1, 5, -1],
        [2, -1, 2, 6]
    ], dtype=np.float64)
    roots = gaussian_elimintation(matrix)
    print(roots.tolist())