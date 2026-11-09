"""9주차: 영공간·열공간, 선형결합, 일차독립 판정."""
import numpy as np

# 예제 4: 세 벡터를 열로 세운 행렬 → det = 0, rank 2 → 종속
A = np.array([[1, 0, 2],
              [2, 1, 5],
              [3, 4, 10]])
print("det =", round(np.linalg.det(A), 10), " rank =", np.linalg.matrix_rank(A))
print("v3 == 2v1 + v2 ?", np.array_equal(A[:, 2], 2 * A[:, 0] + A[:, 1]))

# 예제 2-2A: 영공간 뼈대 벡터를 넣으면 0
B = np.array([[1, 2, 3],
              [2, 4, 6]])
for v in ([-2, 1, 0], [-3, 0, 1]):
    print(f"B @ {v} =", B @ np.array(v))
print("행벡터 (1,2,3)은 영공간 원소? B @ (1,2,3) =", B @ np.array([1, 2, 3]))
r = np.linalg.matrix_rank(B)
print(f"rank = {r}, dim N(B) = 3 - {r} = {3 - r}")

# 예제 2-2B: b가 열공간에 있으면 해가 있다
C = np.array([[1, 2], [2, 4], [3, 6]], dtype=float)
for b in ([3, 6, 9], [1, 0, 0]):
    b = np.array(b, dtype=float)
    x = np.linalg.lstsq(C, b, rcond=None)[0]
    print(f"b = {b}: 해 있음? {np.allclose(C @ x, b)}")

# 예제 3: b = (1,5,9)가 v1, v2의 선형결합인가 (성분 2개로 c를 구하고 나머지로 검산)
v1, v2, b = np.array([1, 2, 3]), np.array([0, 1, 3]), np.array([1, 5, 9])
c1 = b[0]
c2 = b[1] - 2 * c1
print(f"\nc1 = {c1}, c2 = {c2}, 검산: c1·v1 + c2·v2 = {c1 * v1 + c2 * v2} vs b = {b}")

# 다항식도 계수 벡터로 바꾸면 같은 방법: p1 = 1+x, p2 = 1-x², p3 = x+x²
P = np.array([[1, 1, 0], [1, 0, -1], [0, 1, 1]]).T  # 열 = (상수, x, x²) 계수
print("다항식 det =", round(np.linalg.det(P), 10), " rank =", np.linalg.matrix_rank(P), "→ 종속 (p1 - p2 - p3 = 0)")
