"""8주차: 미분 공식을 수치 미분(중앙차분)으로 검산. NumPy만 사용."""
import numpy as np


def d(f, x, h=1e-6):
    """중앙차분 (f(x+h) - f(x-h)) / 2h 로 근사한 미분계수"""
    return (f(x + h) - f(x - h)) / (2 * h)


x = 0.7  # 검산할 점

# (공식으로 구한 도함수, 원래 함수) 짝
checks = {
    "몫: (x^2+1)/(x-3)": (lambda t: (t**2 + 1) / (t - 3),
                         lambda t: (2 * t * (t - 3) - (t**2 + 1)) / (t - 3) ** 2),
    "x^(-1/3)":        (lambda t: t ** (-1 / 3), lambda t: (-1 / 3) * t ** (-4 / 3)),
    "tan x":           (np.tan, lambda t: 1 / np.cos(t) ** 2),
    "sec x":           (lambda t: 1 / np.cos(t), lambda t: np.tan(t) / np.cos(t)),
    "csc x":           (lambda t: 1 / np.sin(t), lambda t: -1 / (np.sin(t) * np.tan(t))),
    "(x^3+1)^100":     (lambda t: (t**3 + 1) ** 100, lambda t: 300 * t**2 * (t**3 + 1) ** 99),
    "e^(x^2+1)":       (lambda t: np.exp(t**2 + 1), lambda t: 2 * t * np.exp(t**2 + 1)),
    "ln 100x":         (lambda t: np.log(100 * t), lambda t: 1 / t),
}
for name, (f, fp) in checks.items():
    num, formula = d(f, x), fp(x)
    print(f"{name:18s} 수치 {num: .6g}  공식 {formula: .6g}  일치 {np.isclose(num, formula, rtol=1e-5)}")

# 시그모이드: σ' = σ(1-σ), 최댓값 0.25 (x=0)
sig = lambda t: 1 / (1 + np.exp(-t))
xs = np.linspace(-6, 6, 1201)
print("σ' = σ(1-σ) ?", np.allclose(d(sig, xs), sig(xs) * (1 - sig(xs))))
print("σ'(0) =", round(sig(0) * (1 - sig(0)), 4))

# 삼각함수 극한: sin7x/5x → 7/5, tan x / x → 1
for t in (1e-2, 1e-4):
    print(f"x={t:g}: sin7x/5x = {np.sin(7 * t) / (5 * t):.6f}, tanx/x = {np.tan(t) / t:.6f}")

# 고계도함수: cos x를 27번 미분 = sin x (주기 4)
cycle = ["cos", "-sin", "-cos", "sin"]
print("cos의 27계 도함수:", cycle[27 % 4])

# 속도·가속도: s = t^3 + t → v = 3t^2 + 1, a = 6t
s = lambda t: t**3 + t
v = lambda t: d(s, t, 1e-4)
print("a(1), a(3) ≈", round(d(v, 1.0, 1e-3), 3), round(d(v, 3.0, 1e-3), 3))
