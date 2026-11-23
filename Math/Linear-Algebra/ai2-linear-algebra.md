# 인공지능기초2에서 나온 선형대수

> 인공지능기초2(화요일)는 선형대수와 다른 과목이지만 벡터·행렬 내용이 많이 겹친다. 여기에는 인공지능기초2 10주차(11/17) 수업과 실습에서 선형대수 노트와 이어지는 것만 모았다. 제출 과제(연습문제 3.7~3.13)의 답은 싣지 않고, 개념과 직접 만든 예시로 정리했다.

| 인공지능기초2 | 선형대수 노트 | 연결 |
|---|---|---|
| 정사영·코사인·직교 (연습문제 3.7~3.9) | [6주차](week06.md) | 같은 공식 |
| 코시-슈바르츠 부등식 (연습문제 3.11) | [증명 14번](proofs.md) | $\cos\theta$가 −1~1인 이유 |
| 점과 평면 사이의 거리 | [7주차](week07.md) 평면 | 법선 방향 그림자의 길이 |
| 그레디언트·야코비안·헤시안·라플라시안 | 3주차 대칭행렬 | 미분 결과를 벡터·행렬로 모음 |
| 선형변환·표준행렬 (4장) | 11주차 예습, [10주차](week10.md) 기저 | 기저가 어디로 가는지 |

## 1. 정사영·코사인·직교 — 6주차와 같은 공식

| 이름 | 식 | 결과 |
|---|---|---|
| $x$의 $y$ 방향 정사영 | $\text{proj}_y x = \dfrac{x \cdot y}{y \cdot y}\,y$ | 벡터 |
| 사잇각 | $\cos\theta = \dfrac{x \cdot y}{\lVert x \rVert \lVert y \rVert}$ | 숫자 (−1~1) |
| 수직 | $x \cdot y = 0$ | 판정 |

예: $x = (2, 3)$, $y = (4, -1)$

$$x \cdot y = 8 - 3 = 5,\quad y \cdot y = 17 \Rightarrow \text{proj}_y x = \frac{5}{17}\begin{bmatrix}4\\-1\end{bmatrix},\qquad \cos\theta = \frac{5}{\sqrt{13}\sqrt{17}} \approx 0.336$$

- 10주차 연결: 그람-슈미트의 그림자 화살표가 이 정사영이다. 기준 벡터의 길이가 1이면($q$) 분모 $y \cdot y = 1$이 사라져서 $(x \cdot q)\,q$가 된다
- 정사영은 벡터, 코사인은 숫자다. 묻는 것이 어느 쪽인지 먼저 본다

## 2. 코시-슈바르츠 부등식

$$\lvert x \cdot y \rvert \le \lVert x \rVert \lVert y \rVert$$

- 양변을 $\lVert x \rVert \lVert y \rVert$로 나누면 $-1 \le \cos\theta \le 1$. 이 부등식이 있어야 내적으로 각도를 정의할 수 있다
- 7주차 피어슨 상관계수(평균을 뺀 벡터의 코사인)가 −1~1인 것도 같은 이유다
- 등호는 두 벡터가 평행할 때 (각도 0° 또는 180°)
- 증명(이차식 + 판별식): [proofs.md 14번](proofs.md)

## 3. 점과 평면 사이의 거리 — 7주차 평면 + 6주차 정사영

평면 위의 한 점 $P$, 법선 $n$, 거리를 잴 점 $Q$

$$d = \frac{\lvert (Q - P) \cdot n \rvert}{\lVert n \rVert}$$

- $(Q - P)$를 법선 방향으로 내린 그림자의 길이에서 부호만 뗀 것이다 (거리는 음수가 없음)
- 7주차 평면 $ax + by + cz + d = 0$의 계수 $(a, b, c)$가 법선이다

예: 평면 $x + 2y + 2z = 0$ ($P$ = 원점, $n = (1, 2, 2)$, $\lVert n \rVert = 3$), $Q = (3, 3, 3)$

$$d = \frac{\lvert 3 + 6 + 6 \rvert}{3} = 5$$

- 실습에서는 4차원에서도 같은 식으로 계산했다. 내적과 길이만 쓰므로 차원과 상관없다

## 4. 그레디언트·야코비안·헤시안 — 미분 결과를 벡터·행렬로 모은 것

| 이름 | 무엇을 미분하나 | 결과 모양 | $f(x, y) = x^2 + 3xy$의 경우 |
|---|---|---|---|
| 그레디언트 $\nabla f$ | 함수 1개를 각 변수로 한 번 | 열벡터 | $\begin{bmatrix}2x + 3y\\3x\end{bmatrix}$ |
| 헤시안 $H_f$ | 함수 1개를 두 변수로 두 번 | 정방행렬 | $\begin{bmatrix}2 & 3\\3 & 0\end{bmatrix}$ |
| 라플라시안 $\nabla^2 f$ | 각 변수로 두 번 미분해서 더함 | 숫자(함수) | $2 + 0 = 2$ |
| 야코비안 $J_F$ | 함수 여러 개 $F = (f_1, \ldots, f_m)$를 각 변수로 한 번 | $m \times n$ 행렬 | 아래 예 |

- 헤시안은 $\frac{\partial^2 f}{\partial x \partial y} = \frac{\partial^2 f}{\partial y \partial x}$라서 **대칭행렬**이다 (3주차). 위 예의 $3$, $3$
- 헤시안의 대각합(대각 성분의 합)이 라플라시안이다
- 야코비안 예: $F(x, y) = (x^2y,\ x + 3y)$ → $J_F = \begin{bmatrix}2xy & x^2\\1 & 3\end{bmatrix}$ (행 = 함수, 열 = 변수, $J_{ij} = \partial f_i / \partial x_j$)
- 실습 코드(10주차2.py)는 행 = 미분 변수, 열 = 함수로 배치해서 위 정의와 전치 관계다. 교재 정의가 어느 쪽인지 확인할 것
- AI에서 쓰는 곳 (수업 설명): 경사하강법은 그레디언트 반대 방향으로 이동하고, 역전파는 연쇄법칙으로 야코비안을 곱해 나간다

## 5. 선형변환과 표준행렬 (4장) — 선형대수 11주차 예습

**정의**: $L: V \to W$가 아래 두 조건을 만족하면 선형변환(선형사상)이다.

| 조건 | 식 |
|---|---|
| ① 덧셈을 보존 | $L(x + y) = L(x) + L(y)$ |
| ② 스칼라곱을 보존 | $L(\alpha x) = \alpha L(x)$ |
| ①② 한 번에 | $L(\alpha x + \beta y) = \alpha L(x) + \beta L(y)$ |

| 예 | 선형? | 이유 |
|---|---|---|
| $L(x) = 3x$ | O | $3(x + y) = 3x + 3y$, $3(\alpha x) = \alpha(3x)$ |
| $L(x) = qx$ ($q \neq 0$) | O | 같은 방법. 게다가 일대일 대응(전단사) |
| $L(x) = ax + b$ ($b \neq 0$) | X | $L(x + y) = a(x + y) + b$인데 $L(x) + L(y) = a(x + y) + 2b$ |

- 선형이면 $L(0) = 0$이다 (②에서 $\alpha = 0$). $+b$는 원점을 옮기므로 선형이 아니다. 9주차 부분공간에 영벡터가 꼭 있어야 했던 것과 같은 이유다

**표준행렬**: $\mathbb{R}^n \to \mathbb{R}^m$ 선형변환은 항상 $L(x) = Ax$로 쓸 수 있고

$$A = \begin{bmatrix} L(e_1) & L(e_2) & \cdots & L(e_n) \end{bmatrix}\qquad (\text{열} = \text{표준기저 벡터가 옮겨지는 곳})$$

- 이유: $x = x_1e_1 + \cdots + x_ne_n$ (표준기저 좌표) → $L(x) = x_1L(e_1) + \cdots + x_nL(e_n) = Ax$
- 10주차 연결: **기저가 어디로 가는지만 알면 모든 벡터가 어디로 가는지 정해진다**

**예제 4-4**: $L(1, 0) = (2, 3)$, $L(1, 1) = (4, 5)$일 때 표준행렬

$$L(0,1) = L(1,1) - L(1,0) = \begin{bmatrix}4\\5\end{bmatrix} - \begin{bmatrix}2\\3\end{bmatrix} = \begin{bmatrix}2\\2\end{bmatrix}\qquad (\text{선형성: } (0,1) = (1,1) - (1,0))$$

$$A = \begin{bmatrix}L(e_1) & L(e_2)\end{bmatrix} = \begin{bmatrix}2 & 2\\3 & 2\end{bmatrix},\qquad \text{검산: } A\begin{bmatrix}1\\1\end{bmatrix} = \begin{bmatrix}4\\5\end{bmatrix}\ ✓$$

- 행으로 적힌 $L(e_1) = (2, 3)$을 행렬에는 **열**로 세운다

**예제 4-5**: $L(1, 2) = (2, 3)$, $L(3, 4) = (4, 5)$일 때 표준행렬

$$A\begin{bmatrix}1 & 3\\2 & 4\end{bmatrix} = \begin{bmatrix}2 & 4\\3 & 5\end{bmatrix} \Rightarrow A = \begin{bmatrix}2 & 4\\3 & 5\end{bmatrix}\begin{bmatrix}1 & 3\\2 & 4\end{bmatrix}^{-1}$$

$$\begin{bmatrix}1 & 3\\2 & 4\end{bmatrix}^{-1} = \frac{1}{4 - 6}\begin{bmatrix}4 & -3\\-2 & 1\end{bmatrix} = \begin{bmatrix}-2 & 3/2\\1 & -1/2\end{bmatrix}$$

$$A = \begin{bmatrix}2 & 4\\3 & 5\end{bmatrix}\begin{bmatrix}-2 & 3/2\\1 & -1/2\end{bmatrix} = \begin{bmatrix}0 & 1\\-1 & 2\end{bmatrix},\qquad \text{검산: } A\begin{bmatrix}1\\2\end{bmatrix} = \begin{bmatrix}2\\3\end{bmatrix},\ A\begin{bmatrix}3\\4\end{bmatrix} = \begin{bmatrix}4\\5\end{bmatrix}\ ✓$$

- 역행렬은 **오른쪽**에 곱한다 ($AB = C$ → $A = CB^{-1}$). 행렬 곱은 순서를 바꿀 수 없다
- $(1,2), (3,4)$가 기저라서($\det = -2 \neq 0$) 역행렬이 있고 $A$가 하나로 정해진다. 기저가 아니면 정보가 모자라서 $A$를 정할 수 없다
- 선형대수 PBL 주제(선형변환을 이용한 이미지 기하 변환)에서 회전·확대·반사를 이 표준행렬로 표현한다
