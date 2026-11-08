# 06 · 이진 트리와 트리 순회

> 헷갈렸던 부분과 해결 과정: [06-tree-traversal-deep-dive.md](06-tree-traversal-deep-dive.md)
>
> 새 문법은 없다. **클래스(04) + 재귀의 print 위치(03)**를 합친 것

## 1. 용어

| 용어 | 뜻 |
|---|---|
| 트리 | 위에서 아래로 가지를 치는 구조 (조직도, 폴더) |
| 노드 | 트리의 칸 하나 = `Node` 객체 하나 |
| 루트 | 맨 꼭대기 노드 |
| 자식 | 바로 아래 연결된 노드. **이진 트리**는 최대 2개 (left, right) |
| 리프 | 자식이 없는 노드 |
| 서브트리 | 어떤 노드를 꼭대기로 보고 그 아래를 통째로 묶은 것 |
| 순회 | 모든 노드를 한 번씩 방문 |

## 2. 트리는 코드 한 줄씩 만들어진다

```python
class Node:
    def __init__(self, key):
        self.left = None       # 왼쪽 자식 칸
        self.right = None      # 오른쪽 자식 칸
        self.key = key

root = Node(1)                 # ① 1번 상자 생성, root 이름표
root.left = Node(5)            # ② 새 상자(5)를 만들어 root의 left 칸에 연결
root.right = Node(3)
root.left.left = Node(2)       # root → 5번 상자 → 그 left 칸
root.left.right = Node(7)
root.right.left = Node(6)
root.right.right = Node(4)
```

- `Node(5)` = 힙에 칸 3개(left, right, key)짜리 상자 생성
- `root.left = ...` = root 상자의 left 칸에 그 상자를 넣기
- `root.left.right`는 **왼쪽부터** 읽는다: root → (left 칸) → 그 상자의 right 칸
- 연결 안 한 칸은 `__init__`에서 넣은 **None 그대로**

```
          1
        /   \
       5     3
      / \   / \
     2   7 6   4
```
트리 그림 = 상자들의 left/right 칸이 누구를 가리키는지를 위아래로 펼친 것

## 3. `if root:` = 종료 조건

| Java | Python |
|---|---|
| `if (root != null)` | `if root:` |

None은 거짓 → 자식이 없는 칸까지 내려가면 아무것도 안 하고 돌아온다.

## 4. 순회 3종류: print 위치만 다르다

```python
def preorder(r):           # 전위: 나 → 왼 → 오
    if r:
        print(r.key, end="/")
        preorder(r.left)
        preorder(r.right)

def inorder(r):            # 중위: 왼 → 나 → 오  (예시문제 3번)
    if r:
        inorder(r.left)
        print(r.key, end="/")
        inorder(r.right)

def postorder(r):          # 후위: 왼 → 오 → 나
    if r:
        postorder(r.left)
        postorder(r.right)
        print(r.key, end="/")

preorder(root);  print()   # 1/5/2/7/3/6/4/
inorder(root);   print()   # 2/5/7/1/6/3/4/
postorder(root); print()   # 2/7/5/6/4/3/1/
```
**전·중·후 = "나"를 언제 출력하느냐** (맨 앞 / 가운데 / 맨 뒤)

## 5. 손으로 푸는 법

### 묶음으로 쪼개기
중위라면 "[왼쪽 묶음] 나 [오른쪽 묶음]"을 안쪽까지 반복

| 단계 | 모양 |
|---|---|
| 1 | [5의 서브트리] **1** [3의 서브트리] |
| 2 | [2] **5** [7] · **1** · [6] **3** [4] |
| 3 | 2 5 7 1 6 3 4 |

전위는 "나 [왼] [오]", 후위는 "[왼] [오] 나"로 같은 방식

### 체크리스트로 따라가기
호출될 때마다 노드가 **할 일 3개**를 받는다고 본다 (중위 기준).

| 순서 | 코드 | 할 일 |
|---|---|---|
| 1 | `f(r.left)` | 왼쪽 일을 아래에 맡기고 **끝날 때까지 기다림** |
| 2 | `print(r.key)` | 내 출력 |
| 3 | `f(r.right)` | 오른쪽 일을 맡기고 기다림 |

> 함수가 끝나면 **자기를 불렀던 함수**로 돌아가서, 그 함수가 멈춰 있던 줄의 **다음 줄**부터 이어서 실행한다.

## 6. 시험에서 함수를 볼 때 확인할 4가지

트리 만드는 줄만 보고 고르면 안 된다. 같은 트리라도 함수가 바뀌면 답이 바뀐다.

| 확인 | 바뀌는 것 |
|---|---|
| ① print가 몇 번째 줄인가 | 전위 / 중위 / 후위 |
| ② left와 right 중 누가 먼저인가 | 좌우가 뒤집힌 순서 |
| ③ print의 `end` | 구분자 (마지막 `/` 포함 여부) |
| ④ print가 여러 개거나 return이 있나 | 출력 개수, 반환값 |

## 7. 연습 문제

### A B C D E 트리
```python
root = Node('A')
root.left = Node('B')
root.right = Node('C')
root.left.right = Node('D')    # B의 오른쪽 (B의 왼쪽은 None)
root.right.left = Node('E')    # C의 왼쪽 (C의 오른쪽은 None)
```
```
        A
      /   \
     B     C
      \   /
       D E
```
| 순회 | 결과 |
|---|---|
| 전위 | `ABDCE` |
| 중위 | `BDAEC` (B의 왼쪽이 None이라 B가 D보다 먼저) |
| 후위 | `DBECA` |

### 10 ~ 60 트리 (중위, `end=","`)
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
# 40,20,10,50,30,60,
```
