# 03 · 함수, 반환값, 재귀

> 헷갈렸던 부분과 해결 과정: [03-function-recursion-deep-dive.md](03-function-recursion-deep-dive.md)

## 1. 함수 기본 (Java 비교)

| Java | Python |
|---|---|
| `int add(int a, int b) { return a + b; }` | `def add(a, b):` + 들여써서 `return a + b` |
| 반환 타입 지정 | 타입 안 씀 |
| `void` | `return`이 없으면 **None** 반환 |

```python
def calc(a, b=3):              # b 기본값 3 (기본값 있는 매개변수는 뒤쪽에)
    return a * b, a + b        # 여러 값 반환 → 튜플

print(calc(2, 5))              # (10, 7)
print(calc(2))                 # (6, 5)
x, y = calc(2)                 # x = 6, y = 5
```
- 기본값은 **값을 안 넘겼을 때만** 쓰인다. 넘기면 덮어쓴다
```python
def greet(name, greeting="안녕"):
    return greeting + ", " + name

print(greet("철수"))              # 안녕, 철수
print(greet("영희", "반가워"))    # 반가워, 영희
```

### 전역 변수를 함수 안에서 바꾸기
```python
cnt = 0
def g():
    global cnt      # 바깥 cnt를 쓰겠다는 선언 (없으면 에러)
    cnt += 1
g()
g()
print(cnt)          # 2
```

### `a, b = b, a + b`
오른쪽을 **먼저 전부 계산**한 뒤 왼쪽에 한꺼번에 넣는다.
```python
p, q = 1, 2
p, q = q, p + q     # (2, 1 + 2) → p = 2, q = 3  (q = 4 아님)
print(p, q)         # 2 3
```

## 2. 함수 호출 자리는 반환값으로 바뀐다

| 단계 | 모습 |
|---|---|
| 처음 | `print(len("abc"))` |
| len 끝 | `print(3)` |
| 출력 | `3` |

호출 줄의 모양에 따라 반환값의 행방이 다르다. **함수 안의 print는 세 경우 모두 실행**된다.

| 줄의 모양 | 반환값 |
|---|---|
| `f()` | **버려짐** |
| `x = f()` | x에 저장 |
| `print(f())` | 출력 |

```python
def g(n):
    print(n, end=" ")
    return n * 10

g(1)              # 화면: 1        (10은 버려짐)
x = g(2)          # 화면: 2        (20은 x에)
print(g(3), x)    # 화면: 3 30 20
# 전체: 1 2 3 30 20
```

- 대화형 창(`>>>`, 주피터)에선 `g(1)`만 쳐도 10이 보이지만, **파일로 실행하면 출력되지 않는다**

## 3. 재귀

- **재귀**: 함수가 자기 자신을 호출
- **종료 조건**: 재귀를 멈추는 조건. 걸리면 그 **아래 줄**은 실행하지 않음
- 호출마다 **자기만의 매개변수·지역 변수**를 가짐

### 규칙 하나
> 함수를 부르면 그 줄에서 멈추고, 부른 함수가 완전히 끝나야 돌아와서 **다음 줄**을 이어서 실행한다.

### 값을 돌려받는 재귀
```python
def fact(n):
    if n <= 1:
        return 1
    return n * fact(n - 1)

print(fact(4))      # 24
```
| 내려가기 | 올라오기 |
|---|---|
| `fact(4)` = 4 × `fact(3)` | 4 × 6 = **24** |
| `fact(3)` = 3 × `fact(2)` | 3 × 2 = 6 |
| `fact(2)` = 2 × `fact(1)` | 2 × 1 = 2 |
| `fact(1)` → 종료 조건 | **1** |

### print 위치에 따른 순서

| print 위치 | 출력 시점 |
|---|---|
| 재귀 호출 **앞** | 내려가면서 (먼저 호출된 것부터) |
| 재귀 호출 **뒤** | 올라오면서 (**가장 깊은 것부터**) |

```python
def f(n):
    if n == 0:
        return
    print(n, end=" ")    # 호출 앞
    f(n - 1)
    print(n, end=" ")    # 호출 뒤

f(3)                     # 3 2 1 1 2 3
```

```python
def f(n):
    if n <= 0:
        return 0
    print(n, end=" ")
    r = n + f(n - 2)
    print(r, end=" ")
    return r

f(5)                     # 5 3 1 1 4 9
```
| 구간 | 출력 |
|---|---|
| 내려가기 (호출 앞 print) | `5 3 1` |
| 바닥 `f(-1)` | 0 반환, 출력 없음 |
| 올라오기 (호출 뒤 print) | `1 4 9` |

```python
def h(n):
    print(n, end="<")    # 종료 조건보다 위 → 바닥에서도 출력됨
    if n == 0:
        return 10
    v = h(n - 1) + n
    print(v, end=">")
    return v

print(h(2))              # 2<1<0<11>13>13
```
마지막 `13`은 **바깥 print**가 h(2)의 반환값을 출력한 것이다.
