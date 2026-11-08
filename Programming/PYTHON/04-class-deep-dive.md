# 04 Deep Dive · self와 인자, 객체 변경

> 개념 요약: [04-class.md](04-class.md)
>
> **틀렸던 것 → 처음 생각 → 원리 → 깨달음** 순서의 기록
>
> Java 객체 동작은 알고 있었지만, 파이썬 코드에서 같은 것을 알아보지 못했다.

---

## 1. "인자 5가 self에 들어간다"고 생각했다

### 처음 생각 (오답)
```python
class Counter:
    def __init__(self, start):
        self.count = start

a = Counter(5)
```
"인자 5를 가져가서 self에 넣음. 그래서 `self.count = start`는 뭔지 모르겠다."

### 원리
5는 `start`에 들어가고, **self에는 방금 만든 객체**가 자동으로 들어간다.

같은 코드를 Java로 바꾸니 바로 보였다.
```java
class Counter {
    int count;
    Counter(int start) { this.count = start; }
}
Counter a = new Counter(5);
```
| Java | Python |
|---|---|
| `this` (매개변수 목록에 안 적고 몰래 넘김) | `self` (맨 앞에 **대놓고** 적음) |
| `this.count = start;` | `self.count = start` |

하는 일은 똑같다. `self.count = start` = 매개변수 `start`(곧 사라짐)의 값을 객체 안 `count` 칸에 옮겨 보관.

### 실행 순서 (지갑 예제로 정리)
```python
class Wallet:
    def __init__(self, money):
        self.money = money
    def spend(self, cost):
        self.money -= cost
        return self.money

w1 = Wallet(1000)
w2 = Wallet(500)
w1.spend(300)
print(w1.money, w2.money)
```
| 단계 | 매개변수 | 힙 |
|---|---|---|
| `Wallet(1000)` | self = 새 지갑A, money = 1000 | 지갑A.money = 1000, 이름표 w1 |
| `Wallet(500)` | self = 새 지갑B, money = 500 | 지갑B.money = 500, 이름표 w2 |
| `w1.spend(300)` | self = 지갑A, cost = 300 | 지갑A.money = 700 (B는 그대로) |
| print | | `700 500` |

---

## 2. self는 꼭 self여야 하나?

### 질문
"메서드에서 매개변수를 받을 때는 다 self로 받는 거임? A, B 같은 이름으로도 되나? self는 그냥 매개변수명임?"

### 원리
그렇다. Python은 **첫 번째 매개변수**에 객체를 넣는다. 이름은 상관없다.
```python
class Wallet2:
    def __init__(me, money):
        me.money = money
    def spend(A, cost):
        A.money -= cost
        return A.money

print(Wallet2(1000).spend(300))   # 700 (정상)
```
관례상 모두 `self`라고 쓸 뿐이다.

### 이걸 알고 나니 보인 오류 유형
```python
class Bad:
    def spend(cost):        # 첫 매개변수 = 객체 자리인데 cost라고 이름 붙임
        return cost

Bad().spend(300)            # TypeError: spend() takes 1 positional argument but 2 were given
```
```python
class Bad2:
    def __init__(self, money):
        money = money       # self. 없음 → 칸이 안 생김

print(Bad2(5).money)        # AttributeError
```

---

## 3. 반환값을 버리면 변경도 없던 일이 된다고 생각했다

### 처음 생각 (오답)
```python
class Counter:
    def __init__(self, start):
        self.count = start
    def up(self, n=1):
        self.count += n
        return self.count

a = Counter(5)
b = Counter(10)
a.up()
b.up(3)
print(a.up(2), b.count)
```
내 답: `8 10` (정답: `8 13`)

a 쪽(기본값, 객체 분리)은 맞혔다. `b.up(3)`은 print로 안 감쌌으니 아무 일도 없었다고 봤다.

### 원리
버려지는 건 **반환값뿐**이다. `self.count += n`은 이미 객체B의 칸을 바꿔놓았다.

| 메서드 안에서 일어난 일 | `b.up(3)`만 쓴 경우 |
|---|---|
| `self.count += n` (객체 칸 변경) | **일어남** → 13으로 남음 |
| `return self.count` | 반환값 13은 버려짐 |

기사님이 가구를 옮겨주고 영수증을 건넸는데, 영수증을 버렸다고 가구가 제자리로 돌아가지는 않는다.

### 확인 문제 (맞힘)
```python
class Bag:
    def __init__(self):
        self.items = []
    def put(self, x):
        self.items.append(x)
        return len(self.items)

p = Bag()
q = Bag()
p.put("A")
q.put("B")
n = p.put("C")
print(n, p.items, q.items)    # 2 ['A', 'C'] ['B']
```

---

## 4. Java로 아는 걸 Python에서 다시 확인한 것

"뭐가 참조변수 타입이고 뭐가 객체 타입인지, 뭐가 메모리에 올라가는지, 생성자 순서는 같은지" 물어봐서 정리한 것.

| 질문 | 답 |
|---|---|
| 참조변수 타입은? | **없음.** 변수는 이름표, 타입은 객체만 |
| 필드·메서드 기준은? | **전부 실제 객체** (Java의 "필드는 변수 타입" 같은 구분 불필요) |
| 메모리에는? | 힙에 객체 1개, 속성은 **이름당 1칸**, 메서드는 클래스에 보관 |
| 생성자 순서는 같은가? | **다름.** 부모 `__init__`은 `super().__init__()`을 **쓴 곳에서만** 실행 |

```python
class P:
    def __init__(self):
        print("P", end="")
        self.v = 1
    def show(self):
        return "P.show"

class C(P):
    def __init__(self):
        print("C", end="")
        self.v = 2
    def show(self):
        return "C.show"

p = C()
print(" |", p.v, p.show())    # C | 2 C.show
```
같은 구조를 Java로 실행하면 `PC | 1 C.show`다 (부모 생성자 자동 호출, 필드는 변수 타입 P 기준).

---

## 정리

| 착각 | 바로잡은 규칙 |
|---|---|
| 인자가 self에 들어간다 | self는 **자동**(새 객체 / 점 앞 객체), 인자는 **두 번째부터** |
| `self.x = x`가 뭔지 모름 | 매개변수 값을 **객체 칸에 보관** (= Java `this.x = x`) |
| self는 키워드 | 그냥 **첫 번째 매개변수 이름** |
| 반환값을 버리면 변경도 없음 | 반환값만 버려지고 **객체 변경은 남음** |
| 생성자 순서는 Java와 같음 | 부모 `__init__`은 **직접 부른 곳에서만** |
