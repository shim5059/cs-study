# 5주차 · 여인수 전개, 수반행렬, 크래머 공식

> 헷갈렸던 부분과 해결 과정: [week05-deep-dive.md](week05-deep-dive.md)

> 교재 2.2 · 코드: [code/week05_cofactor_cramer.py](code/week05_cofactor_cramer.py) · 이 주차 증명은 [proofs.md](proofs.md)

## 1. 소행렬과 여인수

| 용어 | 정의 | 예 $A = \begin{pmatrix}1&2&3\\0&4&5\\1&0&6\end{pmatrix}$ |
|---|---|---|
| 소행렬 $M_{ij}$ | $i$행과 $j$열을 지우고 남은 행렬의 det | $M_{12} = \begin{vmatrix}0&5\\1&6\end{vmatrix} = -5$ |
| 여인수 $C_{ij}$ | $(-1)^{i+j} M_{ij}$ | $C_{12} = (-1)^3(-5) = 5$ |

부호판 ($i + j$가 짝수면 $+$, 홀수면 $-$)

$$\begin{pmatrix}+&-&+\\-&+&-\\+&-&+\end{pmatrix}$$

## 2. 여인수 전개 (라플라스 전개)

**한 줄(행 또는 열)을 골라, 그 줄의 칸마다 (성분 × 여인수)를 구해서 전부 더한다.**

$$\det A = a_{i1}C_{i1} + a_{i2}C_{i2} + \cdots + a_{in}C_{in}$$

0이 많은 줄을 고르면 계산이 줄어든다.

$$A = \begin{pmatrix}2&0&1&3\\0&3&0&0\\1&2&0&2\\0&1&4&1\end{pmatrix}
\xrightarrow{\text{2행 기준}}
\det A = 3 \cdot C_{22} = 3 \cdot \begin{vmatrix}2&1&3\\1&0&2\\0&4&1\end{vmatrix} = 3 \times (-5) = -15$$

## 3. 수반행렬과 역행렬 공식

- 여인수 행렬 $C$: 각 칸을 여인수 $C_{ij}$로 바꾼 행렬
- 수반행렬 $\text{adj}(A) = C^T$ → **$(i, j)$ 칸에는 $C_{ji}$** (번호가 뒤집힌다)
- 핵심 관계: $A \cdot \text{adj}(A) = \det(A)\, I$ → $A^{-1} = \dfrac{1}{\det A}\text{adj}(A)$

$$A = \begin{pmatrix}1&2&0\\0&1&1\\2&0&1\end{pmatrix},\ \det A = 5,\quad
\text{adj}(A) = \begin{pmatrix}1&-2&2\\2&1&-1\\-2&4&1\end{pmatrix},\quad
A \cdot \text{adj}(A) = \begin{pmatrix}5&0&0\\0&5&0\\0&0&5\end{pmatrix}$$

## 4. 크래머 공식

$\det A \neq 0$이면 $Ax = b$의 해는

$$x_i = \frac{\det A_i(b)}{\det A}\qquad (A_i(b) = A\text{의 } i\text{번째 열을 } b\text{로 바꾼 행렬})$$

예: $x_1 + 2x_2 = 5$, $3x_1 + 4x_2 = 11$

| 행렬 | det |
|---|---|
| $A = \begin{pmatrix}1&2\\3&4\end{pmatrix}$ | $-2$ |
| $A_1(b) = \begin{pmatrix}\mathbf{5}&2\\\mathbf{11}&4\end{pmatrix}$ | $-2$ → $x_1 = 1$ |
| $A_2(b) = \begin{pmatrix}1&\mathbf{5}\\3&\mathbf{11}\end{pmatrix}$ | $-4$ → $x_2 = 2$ |

- 기하적 의미: $x_1 a_1 + x_2 a_2 = b$에서 $a_1$을 $b$로 바꾼 평행사변형의 넓이는 원래 넓이의 $x_1$배
- 장점: 원하는 미지수 하나만 바로 구할 수 있음 (교안 예제 5: $x_2 = \frac{72}{44} = \frac{18}{11}$)
- 한계: det를 $n + 1$번 구해야 해서 $n$이 크면 가우스 소거법이 훨씬 빠르다

## 5. 직접 구현

여인수 전개를 재귀 함수로, 수반행렬과 크래머 공식을 그 위에 직접 구현했다.

```text
4×4 det = -15  numpy: -15.0
adj(A) = [[1, -2, 2], [2, 1, -1], [-2, 4, 1]]
A · adj(A) = [[5, 0, 0], [0, 5, 0], [0, 0, 5]] ← det(A)·I
3×3 시스템 → ['-10/11', '18/11', '38/11']
numpy solve  → [-0.909091  1.636364  3.454545]
det(adj A) = 25  (det A)² = 25
```

## 현업에서는

여인수 전개는 $n!$에 가깝게 계산이 늘어나서 실제 프로그램에서는 쓰지 않는다. 직접 재귀로 짜 보면서 "정의대로 푸는 알고리즘"과 "실제로 쓰는 알고리즘(소거법)"이 다를 수 있다는 걸 확인했다.
