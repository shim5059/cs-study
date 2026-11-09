"""3주차: [A | I] → [I | A⁻¹] 를 직접 구현하고 역행렬 성질을 확인한다."""
from fractions import Fraction

import numpy as np


def inverse_gauss_jordan(A):
    """가우스-조르단 소거법으로 역행렬을 구한다. 특이행렬이면 None."""
    n = len(A)
    # 확장첨가행렬 [A | I] 만들기
    M = [[Fraction(x) for x in row] + [Fraction(int(i == j)) for j in range(n)]
         for i, row in enumerate(A)]
    for c in range(n):
        p = next((i for i in range(c, n) if M[i][c] != 0), None)
        if p is None:
            return None  # 왼쪽이 I가 될 수 없음 → 특이행렬
        M[c], M[p] = M[p], M[c]
        lead = M[c][c]
        M[c] = [x / lead for x in M[c]]
        for i in range(n):
            if i != c:
                k = M[i][c]
                M[i] = [a - k * b for a, b in zip(M[i], M[c])]
    return [row[n:] for row in M]  # 오른쪽 절반이 A⁻¹


def show(A):
    for row in A:
        print("  [" + ", ".join(f"{str(x):>5}" for x in row) + "]")


# 교안 예제: 3×3 역행렬
A = [[1, 2, 3], [2, 5, 3], [1, 0, 8]]
print("A⁻¹ (가우스-조르단):")
show(inverse_gauss_jordan(A))
print("np.linalg.inv:\n", np.round(np.linalg.inv(np.array(A, dtype=float)), 6))

# 특이행렬은 역행렬이 없다 (ad - bc = 1·8 - 4·2 = 0)
print("\n[[1,4],[2,8]]의 역행렬:", inverse_gauss_jordan([[1, 4], [2, 8]]))

# (AB)⁻¹ = B⁻¹A⁻¹ (순서가 뒤집힌다), A⁻¹B⁻¹와는 다르다
A = np.array([[1, 2], [0, 1]], dtype=float)
B = np.array([[2, 0], [1, 3]], dtype=float)
inv = np.linalg.inv
print("\n(AB)⁻¹ == B⁻¹A⁻¹ :", np.allclose(inv(A @ B), inv(B) @ inv(A)))
print("(AB)⁻¹ == A⁻¹B⁻¹ :", np.allclose(inv(A @ B), inv(A) @ inv(B)))

# 대칭 + 교대대칭 분해: A = (A + Aᵀ)/2 + (A - Aᵀ)/2
A = np.array([[2, 4], [0, 6]], dtype=float)
S = (A + A.T) / 2
K = (A - A.T) / 2
print("\nS =\n", S, "\nK =\n", K)
print("S 대칭?", np.allclose(S, S.T), "/ K 교대대칭?", np.allclose(K, -K.T),
      "/ S + K == A?", np.allclose(S + K, A))

# 직교행렬: QᵀQ = I 이면 Q⁻¹ = Qᵀ, 길이도 그대로
Q = np.array([[1, -1], [1, 1]]) / np.sqrt(2)
x = np.array([3.0, 4.0])
print("\nQᵀQ = I ?", np.allclose(Q.T @ Q, np.eye(2)))
print("‖x‖ =", np.linalg.norm(x), " ‖Qx‖ =", round(np.linalg.norm(Q @ x), 6))

# 높은 행렬(3×2)의 왼쪽 역행렬 L = (AᵀA)⁻¹Aᵀ 과 의사역행렬 pinv 비교
T = np.array([[1, 0], [1, 1], [0, 1]], dtype=float)
L = inv(T.T @ T) @ T.T
print("\nL * 3 =\n", np.round(L * 3, 6))
print("LT = I ?", np.allclose(L @ T, np.eye(2)), "/ L == pinv(T) ?", np.allclose(L, np.linalg.pinv(T)))
