"""4주차: 행 연산으로 상삼각행렬을 만들어 행렬식을 구한다 (det = 대각선 곱 × 부호)."""
from fractions import Fraction

import numpy as np


def det_by_elimination(A):
    M = [[Fraction(x) for x in row] for row in A]
    n = len(M)
    sign = 1
    for c in range(n):
        p = next((i for i in range(c, n) if M[i][c] != 0), None)
        if p is None:
            return Fraction(0)  # 대각선에 0이 생김 → det = 0
        if p != c:
            M[c], M[p] = M[p], M[c]
            sign = -sign  # 행 교환: 부호 반전
        for i in range(c + 1, n):  # 행 가산: det 변하지 않음
            k = M[i][c] / M[c][c]
            M[i] = [a - k * b for a, b in zip(M[i], M[c])]
    result = Fraction(sign)
    for i in range(n):
        result *= M[i][i]  # 삼각행렬 det = 대각선 곱
    return result


examples = {
    "교안 예제 3 [[1,2,3],[2,5,8],[3,6,10]]": [[1, 2, 3], [2, 5, 8], [3, 6, 10]],
    "사루스 예제 [[1,2,3],[0,4,5],[1,0,6]]": [[1, 2, 3], [0, 4, 5], [1, 0, 6]],
    "특이행렬 [[2,0,1],[4,1,3],[2,1,2]]": [[2, 0, 1], [4, 1, 3], [2, 1, 2]],
    "행 교환이 필요한 [[0,2],[3,1]]": [[0, 2], [3, 1]],
}
for name, A in examples.items():
    print(f"{name}: 직접 = {det_by_elimination(A)}, numpy = {np.linalg.det(np.array(A, float)):.4f}")

# 성질 확인
A = np.array([[2, 1], [1, 3]], dtype=float)
B = np.array([[4, 0], [2, 1]], dtype=float)
det = np.linalg.det
print("\ndet(AB) =", round(det(A @ B), 6), " det(A)det(B) =", round(det(A) * det(B), 6))
print("det(A+B) =", round(det(A + B), 6), " det(A)+det(B) =", round(det(A) + det(B), 6), "← 덧셈은 안 됨")

C = np.array([[1, 2, 3], [0, 4, 5], [1, 0, 6]], dtype=float)  # det = 22, n = 3
print("det(2C) =", round(det(2 * C), 6), " 2³·det(C) =", round(8 * det(C), 6), " 2·det(C) =", round(2 * det(C), 6))
print("det(Cᵀ) =", round(det(C.T), 6), " det(C⁻¹) =", round(det(np.linalg.inv(C)), 6), " 1/22 =", round(1 / 22, 6))
