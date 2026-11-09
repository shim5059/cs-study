"""2주차: 가우스-조르단 소거법을 직접 구현하고 NumPy 결과와 비교한다.

분수(Fraction)로 계산해서 손으로 푼 결과와 똑같은 형태로 나오게 했다.
"""
from fractions import Fraction

import numpy as np


def rref(M):
    """첨가행렬 M을 기약 행 사다리꼴(RREF)로 바꾸고, 피벗 열 번호도 돌려준다."""
    A = [[Fraction(x) for x in row] for row in M]  # 정수 → 분수 (소수 오차 없음)
    rows, cols = len(A), len(A[0])
    pivots = []
    r = 0  # 지금 피벗을 만들 행
    for c in range(cols - 1):  # 마지막 열(상수항)은 피벗 후보가 아님
        # 1) c열에서 0이 아닌 값이 있는 행 찾기
        p = next((i for i in range(r, rows) if A[i][c] != 0), None)
        if p is None:
            continue  # 이 열은 자유변수 열
        A[r], A[p] = A[p], A[r]  # ERO ① 행 교환
        lead = A[r][c]
        A[r] = [x / lead for x in A[r]]  # ERO ② 스칼라배: 선행성분을 1로
        for i in range(rows):  # ERO ③ 행 가산: 피벗 열의 다른 성분을 0으로
            if i != r and A[i][c] != 0:
                k = A[i][c]
                A[i] = [a - k * b for a, b in zip(A[i], A[r])]
        pivots.append(c)
        r += 1
        if r == rows:
            break
    return A, pivots


def show(A):
    for row in A:
        print("  [" + ", ".join(f"{str(x):>4}" for x in row) + "]")


# 교안 예제: x + 2y + 3z = 9, 2x - y + z = 8, 3x - z = 3
M = [[1, 2, 3, 9],
     [2, -1, 1, 8],
     [3, 0, -1, 3]]
R, piv = rref(M)
print("RREF:")
show(R)
print("피벗 열:", piv)

# NumPy로 같은 연립방정식 풀기 (검산)
A = np.array([[1, 2, 3], [2, -1, 1], [3, 0, -1]], dtype=float)
b = np.array([9, 8, 3], dtype=float)
print("np.linalg.solve:", np.linalg.solve(A, b))

# 해가 무수히 많은 경우: 두 식이 사실상 같은 식
R2, piv2 = rref([[1, 1, 3], [2, 2, 6]])
print("\nx + y = 3, 2x + 2y = 6 의 RREF:")
show(R2)
print("피벗 열:", piv2, "→ y는 자유변수")

# 행렬 곱 vs 아다마르곱, 그리고 AB ≠ BA
A = np.array([[1, 2], [0, 1]])
B = np.array([[2, 0], [1, 3]])
print("\nAB =\n", A @ B)
print("BA =\n", B @ A)
print("A * B (아다마르곱, 같은 자리끼리) =\n", A * B)
