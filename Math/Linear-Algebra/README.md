# 선형대수 (Linear Algebra)

선형대수 수업(2026-2학기)에서 배운 내용을 주차별로 정리한 복습 기록

- 교재: 『기초 선형대수학』(2판, 한빛아카데미) / 부교재: 『개발자를 위한 실전 선형대수학』
- 실습 환경: Python (NumPy, SymPy), Google Colab
- `code/`의 검산 코드는 NumPy와 파이썬 기본 `fractions` 모듈만 써서 직접 구현했고, 모두 실행해서 교안 답과 맞는지 확인했다

각 주차는 두 파일로 나뉜다.
- `weekNN.md`: 개념 요약
- `weekNN-deep-dive.md`: 실제로 틀렸던 것 → 처음 생각 → 원리 → 깨달음

## 주차별 목차

| 주차 | 주제 | 교재 범위 | 헷갈린 것 & 해결 |
|---|---|---|---|
| [1주차](week01.md) | 교과목 개요: 선형대수를 왜 배우나, 기록 습관(TIL) | — | — |
| [2주차](week02.md) | 일차·동차방정식, 해의 3가지 경우, 첨가행렬, ERO, REF·RREF, 가우스 소거법, 행렬 연산 | 1장 | — |
| [3주차](week03.md) | 역행렬, 기본행렬, $[A \mid I] \to [I \mid A^{-1}]$, 가역행렬 동치 정리, 대칭·교대대칭·직교행렬, 의사역행렬 | 1.5~1.7 | — |
| [4주차](week04.md) | 행렬식 정의·기하적 의미, 사루스 법칙, ERO와 행렬식, 행렬식 법칙 | 2.1~2.2 | [deep-dive](week04-deep-dive.md) |
| [5주차](week05.md) | 소행렬·여인수, 여인수 전개, 수반행렬과 역행렬 공식, 크래머 공식 | 2.2 | [deep-dive](week05-deep-dive.md) |
| [6주차](week06.md) | $\mathbb{R}^n$ 벡터, 내적·노름·사잇각, 정사영·직교 분해·반사, 외적, 삼중적·부피 | 3장 | [deep-dive](week06-deep-dive.md) |
| [7주차](week07.md) | 공간의 직선·평면, 코사인 유사도, 피어슨 상관계수, 최소제곱법·정규방정식 | 3.3~3.4 | [deep-dive](week07-deep-dive.md) |
| — | 중간고사 (퀴즈 1·2 범위 = 2~6주차) · 퀴즈 문제에서 출제, 증명 포함 → [증명 모음](proofs.md) | | |
| [9주차](week09.md) | 벡터공간, 부분공간 3조건, 영공간·열공간, span, 일차독립·종속 | 4.1~4.3 | [deep-dive](week09-deep-dive.md) |

## 직접 구현한 것

| 파일 | 내용 |
|---|---|
| [week02_gauss_elimination.py](code/week02_gauss_elimination.py) | 분수 연산으로 RREF(가우스-조르단 소거법) 구현, 피벗·자유변수 찾기 |
| [week03_inverse.py](code/week03_inverse.py) | $[A \mid I] \to [I \mid A^{-1}]$ 구현, 역행렬 성질·직교행렬·왼쪽 역행렬 검증 |
| [week04_determinant.py](code/week04_determinant.py) | 행 교환 횟수를 세며 상삼각화하는 행렬식 계산 |
| [week05_cofactor_cramer.py](code/week05_cofactor_cramer.py) | 재귀 여인수 전개, 수반행렬, 크래머 공식 |
| [week06_vectors.py](code/week06_vectors.py) | 내적·사잇각·정사영·반사·외적·부피·토크 |
| [week07_vector_applications.py](code/week07_vector_applications.py) | 직선·평면, 코사인 vs 피어슨 비교, 정규방정식 vs `np.linalg.lstsq` |
| [week09_subspace.py](code/week09_subspace.py) | 영공간·열공간 확인, `matrix_rank`로 일차독립 판정 |

```bash
python3 code/week05_cofactor_cramer.py
```

## 이 과목에서 배운 것

**개념이 이어지는 흐름**

```text
연립방정식 Ax = b ─▶ 소거법(ERO) ─▶ 역행렬 ─▶ 행렬식(det ≠ 0 ⇔ 가역)
                                              │
벡터·내적(수직 = 내적 0) ─▶ 정사영 ─▶ 최소제곱법(해가 없을 때 가장 가까운 답)
          │
        외적(수직인 벡터 만들기) ─▶ 평면의 법선 ─▶ 영공간(행벡터와 수직인 벡터들)
```

- "가역이다 = RREF가 $I$ = $Ax = 0$의 해가 0뿐 = $\det \neq 0$ = 열들이 일차독립"이 전부 같은 말이라는 것. 3주차, 4주차, 9주차가 같은 사실을 다른 각도에서 본 것이었다
- 공식을 외우는 것보다 **검산 방법**을 같이 기억하는 게 중요하다: 외적은 원래 벡터와 내적해서 0, 수반행렬은 $A \cdot \text{adj}A = \det(A)I$, 평면은 세 점 대입, 피어슨은 평균 뺀 벡터의 합이 0
- 증명은 "가정·결론을 식으로 → 정의로 풀기 → 패턴(양변 det / 곱해서 $I$ / 정의대로 전개 / 반례) → 한 줄에 한 단계" 순서로 접근한다 ([증명 모음](proofs.md))
- 정의대로 푸는 알고리즘(여인수 전개, $(A^TA)^{-1}$)과 실제로 쓰는 알고리즘(소거법·LU, QR)은 다를 수 있다

**다룬 기술**

| 분야 | 내용 |
|---|---|
| NumPy | `@`(행렬곱) vs `*`(원소곱), `np.linalg.solve` / `inv` / `pinv` / `det` / `matrix_rank` / `lstsq`, `np.dot`, `np.cross`, `np.linalg.norm`, `np.corrcoef` |
| 직접 구현 | 가우스-조르단 소거법, 역행렬, 상삼각화 행렬식, 재귀 여인수 전개, 크래머 공식 |
| 수치 계산 | 부동소수점 오차(`det`가 정확히 0이 안 나옴) → `np.isclose`, `matrix_rank`로 판정, 정확한 값이 필요하면 `fractions.Fraction` |
| 응용 | 코사인 유사도(검색·추천), 피어슨 상관계수, 선형 회귀(최소제곱), 법선벡터(그래픽스), 토크(로보틱스) |

## 공부하면서 고친 습관

| 습관 | 고친 방법 |
|---|---|
| 식 없이 답만 씀 | 서술형 대비로 "식 한 줄 + 검산 한 줄" |
| 묻는 게 벡터인지 숫자인지 안 봄 | 답 쓰기 전에 기호($\lVert\ \rVert$가 있나)로 확인 |
| 검산을 안 함 | 위의 주제별 검산 방법을 습관으로 |
| 시험 전에 증명을 건너뜀 → 중간고사에 증명이 많이 나옴 | 퀴즈 증명을 카드로 정리 ([proofs.md](proofs.md)) |
