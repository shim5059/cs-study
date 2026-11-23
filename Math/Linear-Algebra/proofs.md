# 증명 모음

> 퀴즈 1·2와 중간고사에 나온 증명(1~7번)과 9주차 이후 기말 범위 증명(8번~)을 한 줄씩 정리했다. 각 줄의 "이유" 칸에는 어떤 정의나 성질을 썼는지 적었다.

## 증명 레시피

```text
① 가정과 결론을 식으로 바꾼다            "직교행렬" → QᵀQ = I
② 용어를 정의로 풀어 쓴다               "대칭" → Aᵀ = A
③ 패턴을 고른다
   A. 양변에 det         (det가 들어간 결론)
   B. 곱해서 I가 되는지   (역행렬이 들어간 결론)
   C. 정의대로 전개      (길이, 전치)
   D. 반례 하나          ("성립하지 않음"을 보일 때)
   E. 양변에 q_i를 내적  (직교·정규직교가 들어간 결론, 다른 항이 0으로 지워짐)
   F. 0 이상인 식 + 판별식 (부등식, 고등학교 이차부등식과 같은 방법)
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
| 9. 기저에 대한 좌표는 유일하다 | 두 표현을 빼면 일차독립 정의 | C |
| 10. 정규직교기저 좌표 $c_i = v \cdot q_i$ | 양변에 $q_i$ 내적, $\delta_{ij}$ | E |
| 11. 0 아닌 직교 집합은 일차독립 | 양변에 $u_i$ 내적, 길이 ≠ 0 | E |
| 12. $(Qx) \cdot (Qy) = x \cdot y$ | 내적을 $x^Ty$로, $Q^TQ = I$ | C |
| 13. 그람-슈미트 남은 조각 $u_k \perp q_i$ | $q_i$ 내적, $\delta_{ij}$로 한 항만 남음 | E |
| 14. 코시-슈바르츠 $\lvert x \cdot y \rvert \le \lVert x \rVert \lVert y \rVert$ (인공지능기초2에서도 나옴) | $\lVert x - ty \rVert^2 \ge 0$, 판별식 | F |

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

---

## 9. 기저에 대한 좌표는 유일하다 (10주차)

**무엇을 보이나**: $S = \{v_1, \ldots, v_n\}$이 기저이면 $v = c_1v_1 + \cdots + c_nv_n$을 만족하는 $c_1, \ldots, c_n$은 한 가지뿐이다

숫자 확인: $S = \{(1,1), (1,-1)\}$, $v = (5,1)$ → $(c_1, c_2) = (3, 2)$ 하나뿐

| 줄 | 식 | 이유 |
|---|---|---|
| 1 | $v = c_1v_1 + \cdots + c_nv_n$, $v = d_1v_1 + \cdots + d_nv_n$이라 하자 | 표현이 두 가지 있다고 가정 |
| 2 | $0 = (c_1 - d_1)v_1 + \cdots + (c_n - d_n)v_n$ | 1줄의 두 식을 빼고 같은 $v_i$끼리 묶음 (분배법칙) |
| 3 | $c_1 - d_1 = \cdots = c_n - d_n = 0$ | $S$는 기저라서 일차독립 → 0을 만드는 계수는 전부 0뿐 (9주차 정의) |
| 4 | ∴ 모든 $i$에 대해 $c_i = d_i$ → 유일 | 두 표현이 같다 |

**핵심**: "두 개 있다고 하고 빼서 0을 만든다" → 일차독립 정의. 기저의 두 조건 중 생성은 표현이 "있다", 일차독립은 "하나뿐"을 맡는다.

---

## 10. 정규직교기저에 대한 좌표는 $c_i = v \cdot q_i$

숫자 확인: $v = (5,1)$, $q_1 = \frac{1}{\sqrt2}(1,1)$, $q_2 = \frac{1}{\sqrt2}(1,-1)$ → $c_1 = 3\sqrt2$, $c_2 = 2\sqrt2$, $3\sqrt2\,q_1 + 2\sqrt2\,q_2 = (5,1)$

| 줄 | 식 | 이유 |
|---|---|---|
| 1 | $v = c_1q_1 + \cdots + c_nq_n$ | 정규직교기저로 표현 (좌표의 정의) |
| 2 | $v \cdot q_i = c_1(q_1 \cdot q_i) + \cdots + c_n(q_n \cdot q_i)$ | 양변에 $q_i$를 내적, 내적의 분배법칙 |
| 3 | $= c_1\delta_{1i} + \cdots + c_n\delta_{ni}$ | 정규직교: $q_j \cdot q_i = \delta_{ji}$ |
| 4 | $= c_i$ | $j = i$인 항만 1, 나머지는 0 |

**핵심**: 내적하면 다른 방향의 항이 전부 0이 되어 자기 계수만 남는다. 직교(길이가 1은 아님)라면 4줄이 $c_i(u_i \cdot u_i)$가 되어 $c_i = \frac{v \cdot u_i}{u_i \cdot u_i}$이다.

---

## 11. 0이 아닌 벡터들의 직교 집합은 일차독립

| 줄 | 식 | 이유 |
|---|---|---|
| 1 | $c_1u_1 + \cdots + c_ku_k = 0$이라 하자 ($u_i \neq 0$, $i \neq j$면 $u_i \cdot u_j = 0$) | 일차독립 정의로 확인할 식 |
| 2 | $c_1(u_1 \cdot u_i) + \cdots + c_k(u_k \cdot u_i) = 0 \cdot u_i = 0$ | 양변에 $u_i$를 내적 |
| 3 | $c_i(u_i \cdot u_i) = 0$ | $j \neq i$인 항은 직교라서 0 |
| 4 | $c_i\lVert u_i \rVert^2 = 0$ | $u \cdot u = \lVert u \rVert^2$ |
| 5 | $c_i = 0$ | $u_i \neq 0$이라 $\lVert u_i \rVert^2 \neq 0$, 양변을 나눔 |
| 6 | ∴ 모든 계수가 0 → 일차독립 | $i$를 아무거나 잡았으므로 |

**핵심**: 영벡터가 섞이면 5줄에서 나눌 수 없다. 그래서 "0이 아닌" 조건이 필요하다 ($\{(1,0), (0,0)\}$은 직교지만 종속).

---

## 12. 직교행렬은 내적을 보존한다

**무엇을 보이나**: $Q^TQ = I$이면 $(Qx) \cdot (Qy) = x \cdot y$

숫자 확인: 90° 회전 $Q = \begin{pmatrix}0&-1\\1&0\end{pmatrix}$, $x = (3,4)$, $y = (1,-2)$ → $Qx = (-4,3)$, $Qy = (2,1)$ → $-8 + 3 = -5 = 3 - 8$

| 줄 | 식 | 이유 |
|---|---|---|
| 1 | $(Qx) \cdot (Qy) = (Qx)^T(Qy)$ | 내적을 행렬곱으로: $a \cdot b = a^Tb$ |
| 2 | $= x^TQ^TQy$ | 곱의 전치: $(Qx)^T = x^TQ^T$ (순서 뒤집힘) |
| 3 | $= x^TIy = x^Ty$ | 직교행렬 정의 $Q^TQ = I$ |
| 4 | $= x \cdot y$ | 1줄과 같은 성질 |

**핵심**: 3번 증명(길이 보존)의 $x$ 하나를 $x$, $y$ 두 개로 바꾼 것이다. 길이와 내적이 모두 그대로라서 $\cos\theta = \frac{x \cdot y}{\lVert x \rVert \lVert y \rVert}$도 그대로 → 각도 보존.

---

## 13. 그람-슈미트의 남은 조각은 앞의 $q$들과 수직

**무엇을 보이나**: $q_1, \ldots, q_{k-1}$이 정규직교이고 $u_k = v_k - \sum_{j=1}^{k-1}(v_k \cdot q_j)\,q_j$이면, $i < k$인 모든 $i$에 대해 $u_k \cdot q_i = 0$

숫자 확인: 예제 5의 $u_2 = (\frac12, -\frac12, 1)$, $q_1 \propto (1,1,0)$ → $\frac12 - \frac12 + 0 = 0$

| 줄 | 식 | 이유 |
|---|---|---|
| 1 | $u_k \cdot q_i = v_k \cdot q_i - \sum_{j=1}^{k-1}(v_k \cdot q_j)(q_j \cdot q_i)$ | 양변에 $q_i$를 내적 ($i < k$), 분배법칙 |
| 2 | $= v_k \cdot q_i - \sum_{j=1}^{k-1}(v_k \cdot q_j)\,\delta_{ji}$ | 앞에서 만든 $q$들은 정규직교 |
| 3 | $= v_k \cdot q_i - v_k \cdot q_i$ | 합에서 $j = i$인 항만 남음 |
| 4 | $= 0$ → $u_k \perp q_i$ | |

**핵심**: 빼는 그림자 중 $q_i$ 방향 하나가 $v_k$의 $q_i$ 방향 성분을 정확히 지운다. 나머지 그림자는 $q_i$와 수직이라 영향을 주지 않는다.

---

## 14. 코시-슈바르츠 부등식 (인공지능기초2에서도 나옴)

**무엇을 보이나**: 모든 벡터 $x$, $y$에 대해 $\lvert x \cdot y \rvert \le \lVert x \rVert \lVert y \rVert$

숫자 확인: $x = (1,2)$, $y = (3,1)$ → $x \cdot y = 5$, $\lVert x \rVert \lVert y \rVert = \sqrt5\sqrt{10} = \sqrt{50} \approx 7.07$

| 줄 | 식 | 이유 |
|---|---|---|
| 0 | $y = 0$이면 양변이 모두 0이라 성립. 이제 $y \neq 0$이라 하자 | 경우 나누기 |
| 1 | 모든 실수 $t$에 대해 $f(t) = \lVert x - ty \rVert^2 \ge 0$ | 길이의 제곱은 0 이상 |
| 2 | $f(t) = (x - ty) \cdot (x - ty) = \lVert y \rVert^2t^2 - 2(x \cdot y)t + \lVert x \rVert^2$ | $\lVert v \rVert^2 = v \cdot v$, 분배법칙으로 전개 |
| 3 | $t$에 대한 이차식이고 최고차항 계수 $\lVert y \rVert^2 > 0$ | $y \neq 0$ |
| 4 | $\frac{D}{4} = (x \cdot y)^2 - \lVert x \rVert^2\lVert y \rVert^2 \le 0$ | 고등학교: $a > 0$일 때 $at^2 + bt + c \ge 0$이 항상 성립 ⇔ $D \le 0$ |
| 5 | $(x \cdot y)^2 \le \lVert x \rVert^2\lVert y \rVert^2$ | 4줄 정리 |
| 6 | ∴ $\lvert x \cdot y \rvert \le \lVert x \rVert \lVert y \rVert$ | 양변이 0 이상이라 루트 |

**핵심**: "0 이상인 이차식이면 판별식 ≤ 0"이라는 고등학교 사실 하나로 끝난다. 이 부등식 덕분에 $\cos\theta = \frac{x \cdot y}{\lVert x \rVert \lVert y \rVert}$가 항상 −1~1 사이라서 6주차의 사잇각 정의와 7주차 피어슨 상관계수의 범위가 성립한다. 등호는 $x$, $y$가 평행할 때다.
