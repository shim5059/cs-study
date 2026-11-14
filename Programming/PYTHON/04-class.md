# 04 · 클래스, self, 메모리, 상속 (Java 비교)

> 헷갈렸던 부분과 해결 과정: [04-class-deep-dive.md](04-class-deep-dive.md)

## 1. Java와 1:1 비교

| Java | Python |
|---|---|
| `class Dog {` | `class Dog:` |
| `String name;` (필드 선언) | 없음. `self.name = ...`이 실행될 때 **칸이 생김** |
| 생성자 `Dog(String name)` | `def __init__(self, name):` |
| `this.name = name;` | `self.name = name` |
| `String bark()` | `def bark(self):` (**첫 매개변수로 self**) |
| `new Dog("바둑")` | `Dog("바둑")` (new 없음) |
| `class Cat extends Animal` | `class Cat(Animal):` |
| `super(name);` | `super().__init__(name)` |
| `if (node != null)` | `if node:` (None은 거짓) |

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
print(w1.money, w2.money)   # 700 500
```

## 2. 인자는 어디로 들어가나

| 호출 | self (자동) | 나머지 매개변수 |
|---|---|---|
| `Wallet(1000)` | **방금 만든 새 객체** | `money = 1000` |
| `w1.spend(300)` | **점 앞의 객체 (w1)** | `cost = 300` |

- 괄호 안 인자는 self를 **건너뛰고** 두 번째 매개변수부터 들어감
- 정의의 매개변수 개수 = 호출 인자 개수 + 1
- `self`는 예약어가 아니라 **그냥 첫 번째 매개변수 이름** (관례로 self)

```python
class Wallet2:
    def __init__(me, money):    # 이름을 me로 바꿔도
        me.money = money
    def spend(A, cost):         # A로 바꿔도 동작
        A.money -= cost
        return A.money

print(Wallet2(1000).spend(300))   # 700
```

## 3. `self.money = money`

| 표현 | 정체 | 수명 |
|---|---|---|
| `money` | 매개변수 | 함수가 끝나면 사라짐 |
| `self.money` | 객체 안의 칸 (속성) | 객체가 살아 있는 동안 |

= "곧 사라질 매개변수 값을 객체 안 칸에 옮겨 보관" (Java `this.money = money`)

## 4. 메모리: Python에는 "참조변수 타입"이 없다

```
Java:   P p = new C();          Python:   p = C()
        ↑변수 타입  ↑객체 타입              ↑이름표   ↑객체 타입
```

| | Java | Python |
|---|---|---|
| 변수 | 타입이 있는 리모컨 (`P`) | 타입 없는 **이름표** |
| 객체 | 힙에 생성 | 힙에 생성 (같음) |
| 부모·자식에 같은 이름 필드 | 객체 안에 칸 **2개** | 이름당 칸 **1개** (덮어씀) |
| 필드·메서드 기준 | 필드는 변수 타입, 메서드는 객체 | **전부 실제 객체** |

```
Python 객체 p ──▶ [ C 객체: v = 2 ]  ──▶ class C (메서드) ──▶ class P (메서드)
```
- 메서드는 객체가 아니라 **클래스**에 있고, `p.show()`는 객체 → 자기 클래스 → 부모 클래스 순으로 찾는다
- 그래서 오버라이딩한 메서드가 실행된다 (Java 동적 바인딩과 같은 결과)

```python
class Animal:
    def __init__(self, name):
        self.name = name
    def sound(self):
        return "..."
    def intro(self):
        return self.name + ":" + self.sound()   # self는 실제 객체

class Cat(Animal):
    def __init__(self, name):
        super().__init__(name)
        print("Cat 생성", end=" ")
    def sound(self):
        return "야옹"

c = Cat("나비")
print(c.intro())     # Cat 생성 나비:야옹
```

## 5. 생성자 호출 순서: Java와 다르다

| | Java | Python |
|---|---|---|
| 자식 생성자에 부모 호출이 없으면 | `super()` **자동** | 부모 `__init__` **실행 안 됨** |
| 부모 호출 위치 | 반드시 첫 줄 | 아무 줄 (쓴 곳에서 실행) |
| 자식에 생성자가 없으면 | 기본 생성자 → `super()` | 부모 `__init__`을 **물려받아** 실행 |

```python
class P:
    def __init__(self):
        print("P", end="")
        self.v = 1

class C1(P):                 # super 없음
    def __init__(self):
        print("C", end="")
        self.v = 2

class C2(P):                 # super 맨 앞
    def __init__(self):
        super().__init__()
        print("C", end="")
        self.v = 2

class C3(P):                 # super 맨 뒤
    def __init__(self):
        print("C", end="")
        self.v = 2
        super().__init__()

class C4(P):                 # __init__ 없음
    pass

a = C1(); print(" |", a.v)   # C | 2
b = C2(); print(" |", b.v)   # PC | 2
c = C3(); print(" |", c.v)   # CP | 1   ← 부모가 같은 칸을 1로 덮어씀
d = C4(); print(" |", d.v)   # P | 1
```

### 부모 메서드까지 부르는 경우 (복습 추가)
```python
class A:
    def __init__(self):
        print("A생성")
        self.x = 1
    def show(self):
        print("A.show", self.x)

class B(A):
    def __init__(self):
        print("B생성 시작")
        super().__init__()     # 이 줄에서 A의 __init__ 실행
        self.x = 2             # 같은 객체의 x를 2로 덮어씀
        print("B생성 끝")
    def show(self):
        print("B.show", self.x)
        super().show()         # A의 show, self는 같은 객체

b = B()
b.show()
```
```
B생성 시작
A생성
B생성 끝
B.show 2
A.show 2
```
- 메서드는 실제 객체의 클래스(B)부터 찾고, 없으면 부모(A)에서 찾는다
- `self`는 객체 하나라 A의 show에서도 x는 2

## 6. 객체마다 칸이 따로, 변경은 남는다

```python
class Counter:
    def __init__(self, start):
        self.count = start
    def up(self, n=1):
        self.count += n
        return self.count

a = Counter(5)
b = Counter(10)
a.up()                    # a: 6  (반환값 버려짐, 변경은 남음)
b.up(3)                   # b: 13 (반환값 버려짐, 변경은 남음)
print(a.up(2), b.count)   # 8 13
```

```python
class Bag:
    def __init__(self):
        self.items = []          # 객체마다 자기 리스트
    def put(self, x):
        self.items.append(x)
        return len(self.items)

p = Bag()
q = Bag()
p.put("A")
q.put("B")
n = p.put("C")
print(n, p.items, q.items)       # 2 ['A', 'C'] ['B']
```

## 7. 자주 나는 오류 두 가지

| 실수 | 결과 |
|---|---|
| `def spend(cost):` (self 빠짐) | 호출 시 TypeError: 1개 받는데 2개 들어옴 |
| `money = money` (`self.` 빠짐) | 객체에 칸이 안 생김 → 읽을 때 AttributeError |
