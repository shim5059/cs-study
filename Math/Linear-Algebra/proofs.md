# 증명 모음 · 중간고사 대비

> 퀴즈 1·2와 중간고사에 나온 증명을 한 줄씩 정리했다. 각 줄의 "이유" 칸에는 어떤 정의나 성질을 썼는지 적었다.

## 증명 레시피

```text
① 가정과 결론을 식으로 바꾼다            "직교행렬" → QᵀQ = I
② 용어를 정의로 풀어 쓴다               "대칭" → Aᵀ = A
③ 패턴을 고른다
   A. 양변에 det         (det가 들어간 결론)
   B. 곱해서 I가 되는지   (역행렬이 들어간 결론)
   C. 정의대로 전개      (길이, 전치)
   D. 반례 하나          ("성립하지 않음"을 보일 때)
④ 한 줄에 한 단계, 이유를 옆에 적는다
```

- 이유 칸에 결론을 쓰면 순환논증이 된다
- 증명 전에 2×2나 작은 숫자로 먼저 확인하면 방향이 잡힌다

## 한눈에 보기

| 증명 | 핵심 아이디어 | 패턴 |
|---|---|---|
| 1. $(AB)^{-1} = B^{-1}A^{-1}$ | 곱해서 $I$가 나오는지 | B |
| 2. 대칭 + 교대대칭 분해의 유일성 | 전치해서 연립방정식 | C |
| 3. $\lVert Qx \rVert = \lVert x \rVert$ | 길이 제곱 = 자기 자신과 내적 | C |
| 4. $\det Q = \pm 1$ | $Q^TQ = I$ 양변에 det | A |
| 5. 3×3 교대대칭 $\det K = 0$ | $K^T = -K$ 양변에 det, 홀수 크기 | A |
| 6. $\det(\text{adj}A) = (\det A)^2$ | $A \cdot \text{adj}A = dI$ 양변에 det | A |
| 7. 반사벡터 $\lVert r \rVert = \lVert u \rVert$ | 수직인 두 성분 → 피타고라스 | C |
| 8. 대칭행렬 집합은 부분공간 ([week09.md](week09.md) 4절) | 전치가 덧셈·스칼라곱을 통과 | C |

---

## 1. $(AB)^{-1} = B^{-1}A^{-1}$

**무엇을 보이나**: $AB$에 $B^{-1}A^{-1}$을 곱하면 $I$가 나온다 (역행렬의 정의)

| 줄 | 식 | 이유 |
|---|---|---|
| 1 | $(AB)(B^{-1}A^{-1})$ | 확인할 곱 |
| 2 | $= A(BB^{-1})A^{-1}$ | 결합법칙 (괄호 위치만 옮김) |
| 3 | $= AIA^{-1}$ | $BB^{-1} = I$ |
| 4 | $= AA^{-1} = I$ | $AI = A$, 역행렬 정의 |
| 5 | 반대 순서 $(B^{-1}A^{-1})(AB) = I$도 같은 방법 | 역행렬은 양쪽 곱이 모두 $I$여야 함 |

**핵심**: 안쪽부터 짝이 맞아 지워지도록 순서를 뒤집는다 (양말 → 신발, 벗을 땐 신발 → 양말).

---

## 2. 대칭 + 교대대칭 분해의 유일성

**무엇을 보이나**: $A = S + K$ ($S^T = S$, $K^T = -K$)로 나누는 방법은 $S = \frac{A + A^T}{2}$, $K = \frac{A - A^T}{2}$ 하나뿐이다

숫자 확인: $A = \begin{pmatrix}2&4\\0&6\end{pmatrix}$ → $S = \begin{pmatrix}2&2\\2&6\end{pmatrix}$, $K = \begin{pmatrix}0&2\\-2&0\end{pmatrix}$

| 줄 | 식 | 이유 |
|---|---|---|
| 1 | $A = S + K$라 하자 ($S^T = S$, $K^T = -K$) | 가정 |
| 2 | $A^T = S^T + K^T$ | 1줄 양변 전치, 합의 전치 = 전치의 합 |
| 3 | $A^T = S - K$ | 대칭·교대대칭 정의 대입 |
| 4 | $A + A^T = 2S$ | 1줄 + 3줄 |
| 5 | $A - A^T = 2K$ | 1줄 − 3줄 |
| 6 | $S = \frac{A + A^T}{2}$, $K = \frac{A - A^T}{2}$ | 양변 ÷ 2 |
| 7 | ∴ 어떤 분해든 $S$, $K$는 이 값이어야 한다 → 유일 | 1줄의 $S$, $K$를 아무거나 잡았으므로 |

(존재: $\left(\frac{A + A^T}{2}\right)^T = \frac{A^T + A}{2}$ 이므로 대칭, 교대대칭도 같은 방법으로 확인)

**핵심**: 모르는 것이 $S$, $K$ 두 개, 식이 두 개($A$와 $A^T$) → 연립방정식처럼 더하고 뺀다.

---

## 3. 직교행렬은 길이를 보존한다

**무엇을 보이나**: $Q^TQ = I$이면 $\lVert Qx \rVert = \lVert x \rVert$

숫자 확인: $Q = \frac{1}{\sqrt2}\begin{pmatrix}1&-1\\1&1\end{pmatrix}$, $x = (3, 4)$ → $\lVert Qx \rVert = 5 = \lVert x \rVert$

| 줄 | 식 | 이유 |
|---|---|---|
| 1 | $\lVert Qx \rVert^2 = (Qx)^T(Qx)$ | 길이의 제곱 = 자기 자신과의 내적 ($\lVert v \rVert^2 = v^Tv$) |
| 2 | $= x^TQ^TQx$ | 곱의 전치: $(Qx)^T = x^TQ^T$ (순서 뒤집힘) |
| 3 | $= x^TIx = x^Tx$ | 직교행렬 정의 $Q^TQ = I$ |
| 4 | $= \lVert x \rVert^2$ | 1줄과 같은 성질 |
| 5 | ∴ $\lVert Qx \rVert = \lVert x \rVert$ | 길이는 0 이상이라 양변 루트 |

**핵심**: 길이를 제곱해서 내적으로 바꾸면 $Q^TQ$가 등장한다.

---

## 4. 직교행렬의 행렬식은 1 또는 −1

| 줄 | 식 | 이유 |
|---|---|---|
| 1 | $Q^TQ = I$ | 직교행렬 정의 |
| 2 | $\det(Q^TQ) = \det I = 1$ | 양변에 det |
| 3 | $\det(Q^T)\det(Q) = 1$ | $\det(AB) = \det A \det B$ |
| 4 | $(\det Q)^2 = 1$ | $\det(Q^T) = \det Q$ |
| 5 | ∴ $\det Q = \pm 1$ | |

숫자 확인: 위 45° 회전 $Q$는 $\frac{1}{2}(1 + 1) = 1$, 반사 $\begin{pmatrix}1&0\\0&-1\end{pmatrix}$은 $-1$

**핵심**: 정의식 양변에 det → 곱의 법칙 → 제곱.

---

## 5. 3×3 교대대칭행렬의 행렬식은 0

| 줄 | 식 | 이유 |
|---|---|---|
| 1 | $K^T = -K$ | 교대대칭 정의 |
| 2 | $\det(K^T) = \det(-K)$ | 양변에 det |
| 3 | $\det K = (-1)^3\det K$ | 왼쪽: $\det(K^T) = \det K$ / 오른쪽: $\det(cA) = c^n\det A$, $n = 3$ |
| 4 | $\det K = -\det K$ | $(-1)^3 = -1$ |
| 5 | $2\det K = 0$ → $\det K = 0$ | |

**핵심**: 크기가 **홀수**라서 $(-1)^n = -1$. 2×2라면 $(-1)^2 = 1$이라 결론이 안 나온다 (예: $\begin{pmatrix}0&2\\-2&0\end{pmatrix}$의 det는 4).

---

## 6. 3×3 가역행렬에서 $\det(\text{adj}\,A) = (\det A)^2$

숫자 확인: $A = \begin{pmatrix}1&2&0\\0&1&1\\2&0&1\end{pmatrix}$, $\det A = 5$ → $\det(\text{adj}A) = 25$

| 줄 | 식 | 이유 |
|---|---|---|
| 1 | $A \cdot \text{adj}(A) = dI$ ($d = \det A$) | 수반행렬의 성질 |
| 2 | $\det A \cdot \det(\text{adj}A) = \det(dI)$ | 양변에 det, 곱의 법칙 |
| 3 | $\det(dI) = d^3$ | $\det(cA) = c^n\det A$, $n = 3$, $\det I = 1$ |
| 4 | $d \cdot \det(\text{adj}A) = d^3$ | 2줄, 3줄 |
| 5 | $\det(\text{adj}A) = d^2$ | $A$가 가역이라 $d \neq 0$, 양변 ÷ $d$ |

**핵심**: $d \neq 0$(가역)이어야 나눌 수 있다. 이 조건을 증명에 꼭 적는다.

---

## 7. 반사벡터의 길이는 원래 벡터와 같다

**무엇을 보이나**: $r = 2u_\parallel - u$이면 $\lVert r \rVert = \lVert u \rVert$

숫자 확인: $u = (2, 3)$, $x$축 기준 → $r = (2, -3)$, 둘 다 길이 $\sqrt{13}$

| 줄 | 식 | 이유 |
|---|---|---|
| 1 | $u = u_\parallel + u_\perp$, $u_\parallel \cdot u_\perp = 0$ | 직교 분해 |
| 2 | $r = 2u_\parallel - (u_\parallel + u_\perp) = u_\parallel - u_\perp$ | 1줄 대입 |
| 3 | $\lVert r \rVert^2 = \lVert u_\parallel \rVert^2 + \lVert u_\perp \rVert^2$ | $u_\parallel \perp u_\perp$ → 피타고라스 (교차항 $-2u_\parallel \cdot u_\perp = 0$) |
| 4 | $\lVert u \rVert^2 = \lVert u_\parallel \rVert^2 + \lVert u_\perp \rVert^2$ | 같은 이유 |
| 5 | ∴ $\lVert r \rVert = \lVert u \rVert$ | 3줄 = 4줄, 길이는 0 이상 |

**핵심**: 수직 성분의 부호만 바뀌고, 제곱하면 부호는 사라진다.
