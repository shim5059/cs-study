"""10주차: 이변수 극한의 경로 판정, 편도함수, 클레로 정리를 수치로 확인. NumPy만 사용."""
import numpy as np

# 1) xy^2/(x^2+y^4): 경로마다 원점 근처 값 비교
f = lambda x, y: x * y**2 / (x**2 + y**4)
for t in (1e-1, 1e-3, 1e-5):
    print(f"t={t:g}  y축 {f(0.0, t):.4f}  y=x {f(t, t):.6f}  x=y^2 {f(t**2, t):.4f}")
print("→ 직선은 0, 포물선은 0.5 → 극한 없음")

# 2) 연속함수는 대입: (x^2 y^3 - x^3 y^2 + 3x + 2y), (x,y)→(1,2)
g = lambda x, y: x**2 * y**3 - x**3 * y**2 + 3 * x + 2 * y
print("근처 값", round(g(1 + 1e-6, 2 - 1e-6), 4), " 대입 값", g(1, 2))


# 3) 편도함수: 나머지 변수는 고정하고 중앙차분
def px(F, x, y, h=1e-6):
    return (F(x + h, y) - F(x - h, y)) / (2 * h)


def py(F, x, y, h=1e-6):
    return (F(x, y + h) - F(x, y - h)) / (2 * h)


x0, y0 = 1.0, 1.0
hill = lambda x, y: 4 - x**2 - 2 * y**2
print("4-x^2-2y^2 at (1,1): f_x", round(px(hill, x0, y0), 6), "(공식 -2)",
      " f_y", round(py(hill, x0, y0), 6), "(공식 -4)")

s = lambda x, y: np.sin(x / (1 + y))
fx = np.cos(x0 / (1 + y0)) / (1 + y0)
fy = np.cos(x0 / (1 + y0)) * (-x0 / (1 + y0) ** 2)
print("sin(x/(1+y)): f_x 일치", np.isclose(px(s, x0, y0), fx), " f_y 일치", np.isclose(py(s, x0, y0), fy))

# 4) 클레로: f = x^3 + x^2 y^3 - 2y^2, f_xy = f_yx = 6xy^2
F = lambda x, y: x**3 + x**2 * y**3 - 2 * y**2
h = 1e-4
fx_ = lambda x, y: px(F, x, y, h)
fy_ = lambda x, y: py(F, x, y, h)
a, b = 1.5, -0.5
print("f_xy", round(py(fx_, a, b, h), 4), " f_yx", round(px(fy_, a, b, h), 4), " 공식 6xy^2 =", 6 * a * b**2)
