"""6주차: 내적, 노름, 사잇각, 정사영, 반사, 외적, 넓이·부피, 토크."""
import numpy as np

# 내적·노름·사잇각
u = np.array([1, 1, 0])
v = np.array([0, 1, 1])
cos_t = u @ v / (np.linalg.norm(u) * np.linalg.norm(v))
print("u·v =", u @ v, " cosθ =", round(cos_t, 6), " θ =", round(np.degrees(np.arccos(cos_t)), 2), "도")

# 부호 = 같은 쪽(+) / 수직(0) / 반대 쪽(-)
for a, b in [((2, 3), (4, -1)), ((2, 1), (-1, 2)), ((2, 1), (-3, 1))]:
    print(f"{a}·{b} = {np.dot(a, b)}")

# 정사영과 직교 분해: u = u∥ + u⊥
u = np.array([2, 3])
v = np.array([4, 0])
u_par = (u @ v) / (v @ v) * v  # 계수 (u·v)/‖v‖² 에 v를 곱해야 벡터가 된다
u_perp = u - u_par
print("\nu∥ =", u_par, " u⊥ =", u_perp, " u⊥·v =", u_perp @ v)

# 반사: 직선(방향 v) 기준으로 접기 → r = 2u∥ - u, 길이는 그대로
r = 2 * u_par - u
print("반사 r =", r, " ‖r‖ =", round(np.linalg.norm(r), 6), " ‖u‖ =", round(np.linalg.norm(u), 6))

# 외적: 두 벡터 모두와 수직, 길이 = 평행사변형 넓이
u = np.array([1, 2, 0])
v = np.array([0, 1, 3])
n = np.cross(u, v)
print("\nu×v =", n, " (u×v)·u =", n @ u, " (u×v)·v =", n @ v)
print("넓이 ‖u×v‖ =", round(np.linalg.norm(n), 6), " = √46 =", round(np.sqrt(46), 6))
print("v×u =", np.cross(v, u), "← 순서 바꾸면 방향 반대")

# 스칼라 삼중적 = 3×3 행렬식 = 평행육면체 부피
u, v, w = np.array([1, 0, 0]), np.array([0, 2, 0]), np.array([1, 1, 3])
print("\n|u·(v×w)| =", abs(u @ np.cross(v, w)), " |det| =", round(abs(np.linalg.det(np.array([u, v, w], float))), 6))

# 토크 τ = r × F
r = np.array([0.5, 1.0, 0.0])
F = np.array([10, 0, 20])
print("토크 τ =", np.cross(r, F), "N·m")
