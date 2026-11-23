"""10주차: 기저·좌표, 차원, 랭크-퇴화차수, 정규직교기저, 직교행렬, 그람-슈미트, QR 분해."""
from fractions import Fraction as F

import numpy as np


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def sub(a, b):
    return [x - y for x, y in zip(a, b)]


def scale(c, a):
    return [c * x for x in a]


def show(v):
    return "(" + ", ".join(str(x) for x in v) + ")"


# ── 1. 좌표벡터: v = c1·v1 + c2·v2 의 c를 성분별 연립방정식으로 구하기 (2×2, 크래머) ──
def coords_2d(v1, v2, target):
    det = v1[0] * v2[1] - v2[0] * v1[1]
    c1 = F(target[0] * v2[1] - v2[0] * target[1], det)
    c2 = F(v1[0] * target[1] - target[0] * v1[1], det)
    return c1, c2


print("[1] 좌표벡터")
for v1, v2, t in (((1, 1), (1, -1), (5, 1)), ((1, 2), (3, 1), (7, 4))):
    c1, c2 = coords_2d(v1, v2, t)
    back = [c1 * a + c2 * b for a, b in zip(v1, v2)]
    print(f"  S = {{{v1}, {v2}}}, v = {t} → [v]_S = ({c1}, {c2}), 검산 c1·v1 + c2·v2 = {show(back)}")

# ── 2. 기저 판정: 열로 세운 행렬의 det ≠ 0 (예제 2) ──
A2 = np.column_stack(([1, 0, 1], [1, 1, 0], [0, 1, 1]))
print("\n[2] 예제 2 det =", round(np.linalg.det(A2), 10), " rank =", np.linalg.matrix_rank(A2), "→ 기저")

# ── 3. 평면의 기저 (예제 3, 단위 대입법): 2x - y + 3z = 0 → y = 2x + 3z ──
print("\n[3] 평면 2x - y + 3z = 0 의 기저")
for x, z in ((1, 0), (0, 1)):
    b = (x, 2 * x + 3 * z, z)
    print(f"  (x, z) = ({x}, {z}) → {b}, 평면 식에 대입: {2 * b[0] - b[1] + 3 * b[2]}")
print("  실습 과제 1: x + 2y - z = 0 → z = x + 2y")
n = np.array([1, 2, -1])
w = [np.array([1, 0, 1]), np.array([0, 1, 2])]
print("   w1·n =", w[0] @ n, " w2·n =", w[1] @ n, " rank[w1 w2] =", np.linalg.matrix_rank(np.column_stack(w)))

# ── 4. 랭크-퇴화차수 정리 ──
print("\n[4] rank + nullity = 열 개수")
for name, M in (("예제 4", [[1, 2, 3], [2, 4, 6]]),
                ("확인 문제", [[1, 2, 0, 1], [0, 1, 1, 0], [1, 3, 1, 1]])):
    M = np.array(M)
    r = np.linalg.matrix_rank(M)
    print(f"  {name}: rank = {r}, nullity = {M.shape[1] - r}, 합 = {M.shape[1]}")
M = np.array([[1, 2, 0, 1], [0, 1, 1, 0], [1, 3, 1, 1]])
print("  확인 문제의 3행 == 1행 + 2행 ?", np.array_equal(M[2], M[0] + M[1]))

# ── 5. 정규직교기저 좌표: c = Qᵀv (역행렬 없이 내적만) ──
print("\n[5] 정규직교기저 좌표 c_i = v·q_i")
s = 1 / np.sqrt(2)
Q2 = np.array([[s, s], [s, -s]])          # 열: q1 = (1,1)/√2, q2 = (1,-1)/√2
v = np.array([5, 1])
c = Q2.T @ v
print("  v = (5,1) → c = Qᵀv =", np.round(c, 4), "= (3√2, 2√2)?", np.allclose(c, [3 * np.sqrt(2), 2 * np.sqrt(2)]))
print("  재합성 Qc =", np.round(Q2 @ c, 10))

# ── 6. 직교행렬 판정: QᵀQ = I (대칭 Q = Qᵀ 와는 다른 말) ──
print("\n[6] 직교행렬 vs 대칭행렬")
for name, M in (("[[1,1],[1,-1]] (대칭)", [[1, 1], [1, -1]]),
                ("90° 회전 [[0,-1],[1,0]]", [[0, -1], [1, 0]]),
                ("Q2 = (1/√2)[[1,1],[1,-1]]", Q2)):
    M = np.array(M, dtype=float)
    print(f"  {name}: 대칭? {np.allclose(M, M.T)}, 직교(QᵀQ = I)? {np.allclose(M.T @ M, np.eye(2))}, det = {round(np.linalg.det(M), 10)}")
x, y = np.array([3.0, 4.0]), np.array([1.0, -2.0])
R90 = np.array([[0, -1], [1, 0]])
print("  길이 보존 ‖Qx‖ = ‖x‖:", np.linalg.norm(R90 @ x), np.linalg.norm(x),
      " 내적 보존:", (R90 @ x) @ (R90 @ y), x @ y)


# ── 7. 그람-슈미트 ──
def gram_schmidt_orthogonal(vectors):
    """직교화(w 버전, 길이 안 맞춤). 분수로 정확히 계산한다: w_k = v_k - Σ (v_k·w_j)/(w_j·w_j) w_j"""
    ws = []
    for v in vectors:
        v = [F(x) for x in v]
        w = v
        for wj in ws:
            w = sub(w, scale(dot(v, wj) / dot(wj, wj), wj))
        ws.append(w)
    return ws


def gram_schmidt_orthonormal(vectors):
    """정규직교화(q 버전, 교안 방식): u_k = v_k - Σ (v_k·q_j) q_j, q_k = u_k / ‖u_k‖"""
    V = np.array(vectors, dtype=float)
    Q = []
    for v in V:
        u = v.copy()
        for q in Q:
            u -= (v @ q) * q             # 그림자 화살표 = (그림자 길이) × q
        Q.append(u / np.linalg.norm(u))  # 남은 조각을 길이 1로
    return np.array(Q).T                 # 열 = q1, q2, ...


print("\n[7] 그람-슈미트 (예제 5)")
vs = [[1, 1, 0], [1, 0, 1], [0, 1, 1]]
ws = gram_schmidt_orthogonal(vs)
for k, w in enumerate(ws, 1):
    print(f"  w{k} (= 교안 u{k}) = {show(w)},  w·w = {dot(w, w)}")
print("  서로 내적:", dot(ws[0], ws[1]), dot(ws[0], ws[2]), dot(ws[1], ws[2]))
Q = gram_schmidt_orthonormal(vs)
print("  q1·√2 =", np.round(Q[:, 0] * np.sqrt(2), 10),
      " q2·√6 =", np.round(Q[:, 1] * np.sqrt(6), 10),
      " q3·√3 =", np.round(Q[:, 2] * np.sqrt(3), 10))
print("  QᵀQ = I ?", np.allclose(Q.T @ Q, np.eye(3)))
print("  그림자 계수: v2·q1 =", round(np.array(vs[1]) @ Q[:, 0], 6), "(1/√2 =", round(1 / np.sqrt(2), 6), ")",
      " v3·q2 =", round(np.array(vs[2]) @ Q[:, 1], 6), "(1/√6 =", round(1 / np.sqrt(6), 6), ")")

print("  순서를 바꾸면 결과가 달라진다 ((1,2),(3,1) vs (3,1),(1,2)):")
for order in ([[1, 2], [3, 1]], [[3, 1], [1, 2]]):
    print("   ", order, "→ w =", [show(w) for w in gram_schmidt_orthogonal(order)])
print("  2D 예: v1 = (3,4), v2 = (10,5) → 그림자 길이 v2·q1 =", np.array([10, 5]) @ (np.array([3, 4]) / 5),
      ", 남은 조각 =", show(gram_schmidt_orthogonal([[3, 4], [10, 5]])[1]))
print("  다른 재료 (1,1,1),(1,0,1),(0,1,1) →", [show(w) for w in gram_schmidt_orthogonal([[1, 1, 1], [1, 0, 1], [0, 1, 1]])])

# ── 8. QR 분해: A = QR, R의 성분 = v_j·q_i ──
print("\n[8] QR 분해")
A = np.array(vs, dtype=float).T          # 열 = v1, v2, v3
R = Q.T @ A                              # R_ij = q_i · v_j → 아래쪽은 0
print("  R =\n", np.round(R, 4))
print("  R 대각 = ‖u_k‖:", np.round(np.diag(R), 4), "vs", np.round([np.sqrt(2), np.sqrt(6) / 2, 2 / np.sqrt(3)], 4))
print("  A == QR ?", np.allclose(Q @ R, A))
Qn, Rn = np.linalg.qr(A)
print("  np.linalg.qr 의 R 대각:", np.round(np.diag(Rn), 4), "← 부호가 음수로 나올 수 있다")
signs = np.sign(np.diag(Rn))
print("  열 부호를 맞추면 손계산 Q와 같다 ?", np.allclose(Qn * signs, Q))

# 최소제곱: Ax = b 의 해가 없을 때 QRx = b → Rx = Qᵀb (7주차 정규방정식과 같은 답)
X = np.array([[1, 1], [1, 2], [1, 3], [1, 4]], dtype=float)  # [1 x] 열 → y = b0 + b1·x
yv = np.array([2, 3, 5, 6], dtype=float)
Qx, Rx = np.linalg.qr(X)
beta_qr = np.linalg.solve(Rx, Qx.T @ yv)
beta_ne = np.linalg.solve(X.T @ X, X.T @ yv)
print("  최소제곱 QR:", np.round(beta_qr, 4), " 정규방정식:", np.round(beta_ne, 4),
      " lstsq:", np.round(np.linalg.lstsq(X, yv, rcond=None)[0], 4))

# ── 9. 실습 과제 2·3 ──
print("\n[9] 실습 과제")
Qhw = gram_schmidt_orthonormal([[1, 0, 2], [2, 1, 0], [0, 1, 3]])
print("  과제 2 Q (행 = q1, q2, q3):\n", np.round(Qhw.T, 4))
print("  q2·√105 =", np.round(Qhw[:, 1] * np.sqrt(105), 6), " QᵀQ = I ?", np.allclose(Qhw.T @ Qhw, np.eye(3)))
print("  과제 2 직교화(w):", [show(w) for w in gram_schmidt_orthogonal([[1, 0, 2], [2, 1, 0], [0, 1, 3]])])
np.random.seed(42)
Qr, _ = np.linalg.qr(np.random.randn(4, 4))
print(f"  과제 3 ‖QᵀQ - I‖ = {np.linalg.norm(Qr.T @ Qr - np.eye(4)):.2e}")
