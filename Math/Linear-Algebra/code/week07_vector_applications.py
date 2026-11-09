"""7주차: 공간의 직선·평면, 코사인 유사도 vs 피어슨 상관계수, 최소제곱법."""
import numpy as np

# 1) 직선 r(t) = r0 + t·d  (도착점 = 출발점 + 걸음 수 × 한 걸음)
r0 = np.array([1, 2, -1])
d = np.array([2, -1, 3])
for t in [-1, 0, 1, 2]:
    print(f"t={t:>2} → {r0 + t * d}")

# 두 점이 주어지면 방향은 B - A (점 B의 좌표를 그대로 쓰면 안 됨)
A, B = np.array([1, 4, 2]), np.array([3, 1, 5])
print("d = B - A =", B - A, " r(1) =", A + 1 * (B - A), "== B")
print("틀린 방향(B 좌표)으로 t=1 →", A + B, "≠ B")

# 2) 세 점으로 평면: u, v → n = u×v → n·(r - P1) = 0
P1, P2, P3 = np.array([1, 0, 1]), np.array([2, 3, 0]), np.array([0, 2, 4])
n = np.cross(P2 - P1, P3 - P1)
d_const = n @ P1
print(f"\n법선 n = {n},  평면: {n[0]}x + ({n[1]})y + {n[2]}z = {d_const}")
print("세 점 대입:", [int(n @ P) for P in (P1, P2, P3)])


# 3) 코사인 유사도와 피어슨 상관계수
def cos_sim(x, y):
    return x @ y / (np.linalg.norm(x) * np.linalg.norm(y))


def pearson(x, y):
    return cos_sim(x - x.mean(), y - y.mean())  # 평균을 먼저 빼고 → 코사인


x = np.array([1, 2, 3, 4], dtype=float)
y = np.array([2, 1, 5, 3], dtype=float)
print(f"\n교안 예제 3: cos = {cos_sim(x, y):.4f}, pearson = {pearson(x, y):.4f}, np.corrcoef = {np.corrcoef(x, y)[0, 1]:.4f}")

a = np.array([90, 80, 70], dtype=float)  # 계속 떨어짐
b = np.array([60, 70, 80], dtype=float)  # 계속 오름
print(f"정반대 흐름: cos = {cos_sim(a, b):.4f} (속음), pearson = {pearson(a, b):.4f}")

doc_a, doc_b = np.array([2.0, 1.0]), np.array([20.0, 10.0])  # 길이만 10배 차이
print(f"길이만 다른 두 벡터: cos = {cos_sim(doc_a, doc_b):.4f}")

xs = np.array([-1, 0, 1], dtype=float)
print(f"y = x² (곡선 관계): pearson = {pearson(xs, xs ** 2):.4f} ← 직선 관계만 잰다")

# 4) 최소제곱법: AᵀA β = Aᵀb
px = np.array([1, 2, 3, 4], dtype=float)
py = np.array([1, 3, 2, 5], dtype=float)
A = np.column_stack([np.ones_like(px), px])  # 설계행렬 [1, x]
beta_normal = np.linalg.solve(A.T @ A, A.T @ py)
beta_lstsq = np.linalg.lstsq(A, py, rcond=None)[0]
residual = py - A @ beta_normal
print("\nAᵀA =", (A.T @ A).tolist(), " Aᵀb =", (A.T @ py).tolist())
print("정규방정식 β =", np.round(beta_normal, 6) + 0.0, " lstsq β =", np.round(beta_lstsq, 6) + 0.0)  # + 0.0: -0. 표시 방지
print("잔차 e =", np.round(residual, 6), " Aᵀe =", np.round(A.T @ residual, 10), "← 열공간과 직교")
