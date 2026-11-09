# 3주차 · 역행렬, 기본행렬, 특별한 행렬

> 교재 1.5~1.7 · 코드: [code/week03_inverse.py](code/week03_inverse.py) · 이 주차 증명은 [proofs.md](proofs.md)

## 1. 역행렬

정방행렬 $A$에 대해 $AB = BA = I$인 $B$가 있으면 $B = A^{-1}$ (역행렬)

| 용어 | 뜻 |
|---|---|
| 가역행렬 | 역행렬이 있음 |
| 특이행렬 | 역행렬이 없음 |

**2×2 공식**: $A = \begin{pmatrix}a&b\\c&d\end{pmatrix}$, $ad - bc \neq 0$이면

$$A^{-1} = \frac{1}{ad - bc}\begin{pmatrix}d&-b\\-c&a\end{pmatrix}$$

| 예 | $ad - bc$ | 결과 |
|---|---|---|
| $\begin{pmatrix}1&4\\2&7\end{pmatrix}$ | $7 - 8 = -1$ | $A^{-1} = \begin{pmatrix}-7&4\\2&-1\end{pmatrix}$ |
| $\begin{pmatrix}1&4\\2&8\end{pmatrix}$ | $8 - 8 = 0$ | 특이행렬 (2행이 1행의 2배) |

- 대각행렬: 대각 성분의 역수 $\text{diag}(2, -3, 5)^{-1} = \text{diag}(\frac{1}{2}, -\frac{1}{3}, \frac{1}{5})$. 대각에 0이 하나라도 있으면 역행렬 없음

## 2. 기본행렬과 $[A \mid I] \to [I \mid A^{-1}]$

- **기본행렬 $E$** = 단위행렬 $I$에 ERO를 **딱 한 번** 한 행렬
- $EA$ = $A$에 그 ERO를 한 결과 (행 연산을 "곱셈"으로 바꿔 쓸 수 있다)
- $E^{-1}$ = 반대 연산의 기본행렬. 예: $R_2 - 2R_1$의 역은 $R_2 + 2R_1$

$$E = \begin{pmatrix}1&0&0\\-2&1&0\\0&0&1\end{pmatrix},\quad E^{-1} = \begin{pmatrix}1&0&0\\2&1&0\\0&0&1\end{pmatrix}$$

**가우스-조르단 역행렬 구하기**: ERO로 왼쪽 $A$를 $I$로 만들면 오른쪽이 $A^{-1}$

- 원리: $E_k \cdots E_1 A = I$ 이면 $E_k \cdots E_1 = A^{-1}$ 이고, 같은 ERO를 $I$에 하면 $E_k \cdots E_1 I = A^{-1}$
- 왼쪽이 $I$가 안 되면(0인 행이 생기면) 특이행렬

$$A = \begin{pmatrix}1&2&3\\2&5&3\\1&0&8\end{pmatrix} \Rightarrow A^{-1} = \begin{pmatrix}-40&16&9\\13&-5&-3\\5&-2&-1\end{pmatrix}$$

## 3. 역행렬 성질

| 성질 | 숫자 예 / 이유 |
|---|---|
| $(A^{-1})^{-1} = A$ | 되돌리기를 되돌리면 원래대로 |
| $(cA)^{-1} = \frac{1}{c}A^{-1}$ | $(2A)(\frac{1}{2}A^{-1}) = I$ |
| $(AB)^{-1} = B^{-1}A^{-1}$ | 양말 신고 신발 신었으면, 벗을 땐 신발 먼저 |
| $(A^T)^{-1} = (A^{-1})^T$ | |

## 4. 역행렬로 연립방정식 풀기와 가역행렬 동치 정리

$Ax = b$의 양변 **왼쪽**에 $A^{-1}$을 곱하면 $x = A^{-1}b$

예: $x + 4y = 3$, $2x + 7y = 5$ → $\begin{pmatrix}-7&4\\2&-1\end{pmatrix}\begin{pmatrix}3\\5\end{pmatrix} = \begin{pmatrix}-1\\1\end{pmatrix}$

**$n \times n$ 행렬 $A$에 대해 아래는 전부 같은 말** (하나가 참이면 전부 참)

1. $A$는 가역
2. $A$는 기본행렬들의 곱
3. RREF($A$) $= I$
4. 모든 $b$에 대해 $Ax = b$의 해가 딱 하나
5. $Ax = 0$의 해는 자명해 $x = 0$뿐
6. $\det A \neq 0$ (4주차)

## 5. 특별한 행렬

| 행렬 | 조건 | 예 |
|---|---|---|
| 대칭 | $A^T = A$ | $\begin{pmatrix}2&2\\2&6\end{pmatrix}$ |
| 교대대칭 | $A^T = -A$ (대각 성분은 전부 0) | $\begin{pmatrix}0&2\\-2&0\end{pmatrix}$ |
| 직교 | $Q^TQ = I$, 즉 $Q^{-1} = Q^T$ | $\frac{1}{\sqrt{2}}\begin{pmatrix}1&-1\\1&1\end{pmatrix}$ (45° 회전) |

**대칭 + 교대대칭 분해**: 모든 정방행렬은 딱 한 가지 방법으로 나뉜다

$$A = \underbrace{\frac{A + A^T}{2}}_{S} + \underbrace{\frac{A - A^T}{2}}_{K},\qquad
\begin{pmatrix}2&4\\0&6\end{pmatrix} = \begin{pmatrix}2&2\\2&6\end{pmatrix} + \begin{pmatrix}0&2\\-2&0\end{pmatrix}$$

**직교행렬**: 열벡터들이 서로 수직이고 길이가 1. 길이를 바꾸지 않는다 ($\lVert Qx \rVert = \lVert x \rVert$). 예: $x = (3, 4)$ → $\lVert Qx \rVert = 5$

## 6. 정방이 아닌 행렬의 역행렬

- 세로로 긴 행렬($m > n$)의 열들이 일차독립이면 **왼쪽 역행렬** $L = (A^TA)^{-1}A^T$, $LA = I$ (단 $AL \neq I$)
- 무어-펜로즈 **의사역행렬** `np.linalg.pinv(A)`: 모든 행렬에 존재, 7주차 최소제곱법의 기초

$$A = \begin{pmatrix}1&0\\1&1\\0&1\end{pmatrix} \Rightarrow L = \frac{1}{3}\begin{pmatrix}2&1&-1\\-1&1&2\end{pmatrix}$$

## 7. 직접 구현

$[A \mid I]$ 소거를 분수로 직접 구현하고 `np.linalg.inv`, `np.linalg.pinv`와 비교했다.

```text
A⁻¹ (가우스-조르단):
  [  -40,    16,     9]
  [   13,    -5,    -3]
  [    5,    -2,    -1]
[[1,4],[2,8]]의 역행렬: None
(AB)⁻¹ == B⁻¹A⁻¹ : True
(AB)⁻¹ == A⁻¹B⁻¹ : False
‖x‖ = 5.0  ‖Qx‖ = 5.0
LT = I ? True / L == pinv(T) ? True
```

## 현업에서는

로봇·3D 그래픽스의 회전 행렬은 직교행렬이라서 역회전을 계산할 때 역행렬 대신 전치만 하면 된다. 교안에서는 대칭/교대대칭 분해가 컴퓨터 비전(Optical Flow)에서 변형과 회전을 나누는 데 쓰인다고 소개했다.
