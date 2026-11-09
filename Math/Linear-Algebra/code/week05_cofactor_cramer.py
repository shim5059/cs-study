"""5주차: 여인수 전개(재귀), 수반행렬, 크래머 공식을 직접 구현한다."""
from fractions import Fraction

import numpy as np


def minor(A, i, j):
    """i행, j열을 지운 부분행렬"""
    return [row[:j] + row[j + 1:] for k, row in enumerate(A) if k != i]


def det_cofactor(A):
    """1행 기준 여인수 전개: det A = Σ a1j · C1j"""
    if len(A) == 1:
        return A[0][0]
    if len(A) == 2:
        return A[0][0] * A[1][1] - A[0][1] * A[1][0]
    return sum((-1) ** j * A[0][j] * det_cofactor(minor(A, 0, j))
               for j in range(len(A)) if A[0][j] != 0)  # 0인 칸은 건너뜀


def cofactor(A, i, j):
    return (-1) ** (i + j) * det_cofactor(minor(A, i, j))  # Cij = (-1)^(i+j) Mij


def adjugate(A):
    """adj(A)의 (i, j) 성분 = Cji  (여인수 행렬을 전치)"""
    n = len(A)
    return [[cofactor(A, j, i) for j in range(n)] for i in range(n)]


def cramer(A, b):
    d = det_cofactor(A)
    xs = []
    for i in range(len(A)):
        Ai = [row[:i] + [b[k]] + row[i + 1:] for k, row in enumerate(A)]  # i번째 열을 b로 교체
        xs.append(Fraction(det_cofactor(Ai), d))
    return xs


# 교안 예제 2: 4×4 (0이 많은 행으로 전개하면 빠름)
A4 = [[2, 0, 1, 3], [0, 3, 0, 0], [1, 2, 0, 2], [0, 1, 4, 1]]
print("4×4 det =", det_cofactor(A4), " numpy:", round(np.linalg.det(np.array(A4, float)), 6))

# 교안 예제 3: 수반행렬과 역행렬
A = [[1, 2, 0], [0, 1, 1], [2, 0, 1]]
adj = adjugate(A)
d = det_cofactor(A)
print("\ndet A =", d)
print("adj(A) =", adj)
print("A · adj(A) =", (np.array(A) @ np.array(adj)).tolist(), "← det(A)·I")

# 교안 예제 4, 5: 크래머 공식
print("\nx1 + 2x2 = 5, 3x1 + 4x2 = 11 →", [str(v) for v in cramer([[1, 2], [3, 4]], [5, 11])])
A3 = [[1, 0, 2], [-3, 4, 6], [-1, -2, 3]]
b3 = [6, 30, 8]
x = cramer(A3, b3)
print("3×3 시스템 →", [str(v) for v in x])
print("numpy solve  →", np.round(np.linalg.solve(np.array(A3, float), np.array(b3, float)), 6))

# det(adj A) = (det A)^(n-1). 3×3이면 (det A)²
print("\ndet(adj A) =", det_cofactor(adj), " (det A)² =", d ** 2)
