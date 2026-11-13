# 06 Deep Dive · 트리 순회를 "근거 있게" 풀기까지

> 개념 요약: [06-tree-traversal.md](06-tree-traversal.md)
>
> **틀렸던 것 → 처음 생각 → 원리 → 깨달음** 순서의 기록

---

## 1. 출발점: 예시문제 3번을 아예 못 풀었다

```python
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.key = key

def testFunction(root):
    if root:
        testFunction(root.left)
        print(root.key, end="/")
        testFunction(root.right)

root = Node(1)
root.left = Node(5)
root.right = Node(3)
root.left.left = Node(2)
root.left.right = Node(7)
root.right.left = Node(6)
root.right.right = Node(4)
testFunction(root)
# 정답: 2/5/7/1/6/3/4/
```
"파이썬을 너무 얕게 배운 것 같다, 함수는 처음 본다." 클래스, 재귀, 트리 세 가지가 한꺼번에 나와서 어디서부터 읽을지 몰랐다. 그래서 클래스(04)와 재귀(03)를 먼저 따로 익히고 돌아왔다.

---

## 2. 정답은 골랐지만 근거가 없었다

### 처음 생각
```python
def f(r):
    if r:
        print(r.key, end="")
        f(r.left)
        f(r.right)

root = Node('A')
root.left = Node('B')
root.right = Node('C')
root.left.right = Node('D')
root.right.left = Node('E')
f(root)
```
`ABDCE`를 골라서 맞혔다. 그런데 다시 읽어보니 **트리 만드는 아래쪽 줄만 보고 그림을 그렸고, 위의 함수는 보지 않았다.** 근거 없이 고른 것이었다.

### 원인 1: 트리 그림이 어디서 나오는지 몰랐다
설명에 쓰인 트리 그림이 **미리 완성된 채로** 나와서, 코드 어느 줄에서 그 모양이 생기는지 연결이 안 됐다.

빈 힙에서 시작해 한 줄씩 다시 따라갔다.

| 줄 | 일어나는 일 |
|---|---|
| `root = Node('A')` | A 상자 생성 (left: None, right: None, key: 'A'), root 이름표 |
| `root.left = Node('B')` | `=` 오른쪽 먼저: B 상자 생성 → A의 left 칸에 연결 |
| `root.right = Node('C')` | C 상자 생성 → A의 right 칸에 연결 |
| `root.left.right = Node('D')` | root → A, A의 left → B. **B의 right 칸**에 D |
| `root.right.left = Node('E')` | root → A, A의 right → C. **C의 left 칸**에 E |

여기까지는 **출력이 하나도 없다.** 트리는 상자들의 칸 연결일 뿐이다.

### 원인 2: 함수 쪽을 안 봤다
"시험에선 순회 함수는 다 똑같이 주겠지? 아래 트리 만드는 부분만 보면 되겠지?"라고 생각했다.

같은 트리라도 함수에 따라 답이 다르다.

| 순회 | 결과 |
|---|---|
| 전위 (print 맨 앞) | `ABDCE` |
| 중위 (print 가운데) | `BDAEC` |
| 후위 (print 맨 뒤) | `DBECA` |

→ 함수에서 **print 위치, left/right 순서, end, print·return 개수** 네 가지를 반드시 확인하기로 했다.

---

## 3. 40까지 내려가고 그다음을 몰랐다

### 처음 생각
```python
def g(r):
    if r:
        g(r.left)
        print(r.key, end=",")
        g(r.right)

root = Node(10)
root.left = Node(20)
root.right = Node(30)
root.left.left = Node(40)
root.right.left = Node(50)
root.right.right = Node(60)
g(root)
```
"r.left니까 왼쪽으로 계속 내려가서 40 출력, 오른쪽은 None이니 끝. 그다음부터 모르겠다." (정답 `40,20,10,50,30,60,`은 골랐지만 근거는 40까지였다)

### 원리: 끝나면 불렀던 함수의 다음 줄로
g(40)이 끝나면 "다음 노드로 넘어가는" 게 아니다. **40을 불렀던 g(20)이 깨어나서, 멈춰 있던 줄(`g(r.left)`)의 다음 줄인 print로** 간다.

### 풀린 설명: 할 일 체크리스트
호출될 때마다 노드가 할 일 3개짜리 체크리스트를 받는다.

| 순서 | 코드 | 할 일 |
|---|---|---|
| 1 | `g(r.left)` | 왼쪽 일을 맡기고 **기다림** |
| 2 | `print(r.key)` | 내 출력 |
| 3 | `g(r.right)` | 오른쪽 일을 맡기고 기다림 |

| 단계 | 체크리스트 상태 (✓ 끝, ▶ 진행·대기, □ 아직) | 출력 |
|---|---|---|
| 1 | g(10) ▶□□ → g(20) ▶□□ → g(40) ▶□□ | |
| 2 | g(40): 왼쪽 None ✓, 출력 ✓, 오른쪽 None ✓ → **끝** | `40,` |
| 3 | **g(20)이 깨어남**: 왼쪽 ✓, 출력 ✓ | `40,20,` |
| 4 | g(20): 오른쪽 None ✓ → 끝. **g(10)이 깨어남**: 왼쪽 ✓, 출력 ✓ | `40,20,10,` |
| 5 | g(10): 오른쪽 ▶ → g(30) ▶ → g(50): ✓✓✓ | `…,50,` |
| 6 | g(30) 깨어남: 출력 ✓ → 오른쪽 g(60): ✓✓✓ | `…,30,60,` |
| 7 | g(30) 끝 → g(10) 끝 | `40,20,10,50,30,60,` |

10이 세 번째에야 나오는 이유: **왼쪽 일(40, 20)이 완전히 끝나야** 자기 출력으로 넘어가기 때문.

### 깨달음
03의 재귀 규칙("호출한 줄에서 멈추고, 끝나면 다음 줄")을 트리에 그대로 쓰면 된다. 트리라고 새로운 규칙이 있는 게 아니었다.

---

## 정리

| 착각 | 바로잡은 규칙 |
|---|---|
| 트리 그림이 원래 있는 것 | `Node()` 생성 + **칸 연결** 코드가 만든 모양 |
| 트리 만드는 줄만 보면 됨 | 함수의 **print 위치 · 좌우 순서 · end · 개수** 확인 |
| 한 노드가 끝나면 다음 노드로 | **불렀던 함수의 다음 줄**로 복귀 |
| 루트가 먼저 나옴 (중위에서) | 왼쪽 서브트리가 **전부 끝나야** 루트 출력 |

### 문제 푸는 순서
1. 트리 만드는 줄을 한 줄씩 읽으며 상자·칸 연결로 그림 그리기
2. 함수에서 4가지 확인
3. 묶음으로 쪼개기 (빠르게) 또는 체크리스트로 따라가기 (확실하게)

---

## 모의고사 1회에서 틀린 것: 오른쪽 먼저 도는 순회 (2026-11-13)

```python
def f(r):
    if r:
        f(r.right)
        print(r.key, end=" ")
        f(r.left)
# 트리: M(K(A, Q), Z(-, B))
```
내 답: `B Z M A Q K` (정답: `B Z M Q K A`)

`B Z M`까지는 맞았는데 K 서브트리에서 **왼쪽(A)부터** 썼다. 이 함수는 끝까지 **[오른쪽] 나 [왼쪽]**이라 K 서브트리도 Q → K → A. 확인 항목 ② "left와 right 중 누가 먼저인가"를 **서브트리마다** 똑같이 적용한다.
