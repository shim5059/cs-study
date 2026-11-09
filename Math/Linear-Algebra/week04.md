# 4주차 · 행렬식의 정의와 성질

> 헷갈렸던 부분과 해결 과정: [week04-deep-dive.md](week04-deep-dive.md)

> 교재 2.1~2.2 · 코드: [code/week04_determinant.py](code/week04_determinant.py)

## 1. 행렬식이란

정방행렬 하나를 **숫자 하나**로 요약한 값. $\det A$ 또는 $|A|$

| 보는 관점 | 뜻 |
|---|---|
| 판정 | $\det A \neq 0$ ⇔ 가역 |
| 기하 | 그 행렬로 변환했을 때 넓이(2D)·부피(3D)가 몇 배가 되나 |
| $\det A = 0$ | 평면이 선이나 점으로 **납작해짐** → 다시 펼칠 수 없음 → 역행렬 없음 |

## 2. 계산 공식

**2×2**: $\begin{vmatrix}a&b\\c&d\end{vmatrix} = ad - bc$

| 예 | 계산 | 결과 |
|---|---|---|
| $\begin{pmatrix}3&5\\2&4\end{pmatrix}$ | $12 - 10$ | $2$ → 가역 |
| $\begin{pmatrix}2&-4\\-3&6\end{pmatrix}$ | $12 - 12$ | $0$ → 특이 |

**3×3 사루스 법칙** (3×3 전용, 4×4 이상은 안 됨)

$$\det = (aei + bfg + cdh) - (ceg + bdi + afh)$$

$\begin{pmatrix}1&2&3\\0&4&5\\1&0&6\end{pmatrix}$: $(24 + 10 + 0) - (12 + 0 + 0) = 22$

## 3. 행 연산이 행렬식에 주는 영향

| ERO | det 변화 | 예 ($\det A = 22$) |
|---|---|---|
| 행 교환 | 부호 반대 | $-22$ |
| 한 행을 $c$배 | $c$배 | 한 행을 2배 → $44$ |
| 한 행의 배수를 다른 행에 더함 | **안 변함** | $22$ |

**삼각행렬의 det = 대각 성분의 곱** → 행 가산 연산으로 상삼각행렬을 만들면 빠르게 계산된다

$$\begin{pmatrix}1&2&3\\2&5&8\\3&6&10\end{pmatrix}
\xrightarrow{R_2 - 2R_1,\ R_3 - 3R_1}
\begin{pmatrix}1&2&3\\0&1&2\\0&0&1\end{pmatrix}
\Rightarrow \det = 1 \cdot 1 \cdot 1 = 1$$

## 4. 행렬식 법칙

| 법칙 | 숫자 예 |
|---|---|
| $\det(AB) = \det A \cdot \det B$ | $A = \begin{pmatrix}2&1\\1&3\end{pmatrix}$, $B = \begin{pmatrix}4&0\\2&1\end{pmatrix}$: $5 \times 4 = 20 = \det(AB)$ |
| $\det(A^T) = \det A$ | $22 = 22$ |
| $\det(A^{-1}) = \frac{1}{\det A}$ | $\frac{1}{22}$ |
| $\det(cA) = c^n \det A$ ($n$: 크기) | 3×3에서 $\det(2A) = 2^3 \times 22 = 176$ (모든 행에 2가 곱해지므로) |
| $\det(A + B) \neq \det A + \det B$ | 위 $A, B$: $\det(A + B) = 21$, $\det A + \det B = 9$ |

## 5. 직접 구현

행 교환 횟수를 세면서 상삼각행렬을 만드는 함수를 짜서 `np.linalg.det`와 비교했다.

```text
교안 예제 3 [[1,2,3],[2,5,8],[3,6,10]]: 직접 = 1, numpy = 1.0000
사루스 예제 [[1,2,3],[0,4,5],[1,0,6]]: 직접 = 22, numpy = 22.0000
특이행렬 [[2,0,1],[4,1,3],[2,1,2]]: 직접 = 0, numpy = 0.0000
행 교환이 필요한 [[0,2],[3,1]]: 직접 = -6, numpy = -6.0000
det(2C) = 176.0  2³·det(C) = 176.0  2·det(C) = 44.0
```

## 현업에서는

`np.linalg.det`도 내부적으로는 이 방식(LU 분해 후 대각선 곱)으로 계산한다. 소수 계산이라 0이어야 할 값이 `1e-16`처럼 나올 수 있어서, 특이행렬 판정에는 9주차의 `matrix_rank`가 더 안전하다.
