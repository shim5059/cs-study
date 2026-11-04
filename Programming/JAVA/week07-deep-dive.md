# 7주차 Deep Dive · 업캐스팅 메서드 호출을 "진짜로" 이해하기까지

> 개념 요약: [week07.md](week07.md)
>
> 중간고사 때부터 계속 같은 곳(업캐스팅된 변수의 메서드 호출)에서 틀렸다. 7주차 복습에서 며칠에 걸쳐 여러 비유를 시도한 끝에 원리를 잡았다. 그 과정을 그대로 남긴다.

---

## 1. 출발점: 무엇을 모르는지 몰랐다

### 처음 생각 (오답)
```java
class Bird { void fly() { System.out.println("날다"); } }
class Eagle extends Bird {
    void fly()  { System.out.println("높이 날다"); }
    void hunt() { System.out.println("사냥"); }
}

Bird b = new Eagle();
b.fly();    // 내 답: 날다         (정답: 높이 날다)
b.hunt();   // 내 답: 사냥 정상 출력 (정답: 컴파일 에러)
```
내 설명은 "부모를 먼저 보고, 부모에 hunt가 없으니 자식 것을 실행한다"였다. 찾는 순서도, 에러가 나는 이유도 모두 거꾸로였다.

### 진짜 원인
`Bird b = new Eagle();`에서 **`Bird`와 `Eagle`이 각각 무슨 일을 하는지** 몰랐다. 둘 다 "타입"이라는 것만 알고 역할을 구분하지 못했다.

---

## 2. 해결: 두 타입은 하는 일이 하나씩이다

```
Bird      b   =   new Eagle();
 ↑                     ↑
변수 타입               객체 타입
"이 메서드 불러도 돼?"    "실제로 누구 걸 실행해?"
 → 허락만 함             → 실행을 정함
```

메서드 호출 `b.m()`은 **검사 2번**이다.

```
① 컴파일 때: 변수 타입이 "가진" 메서드에 m이 있나?
             없으면 → 컴파일 에러, 끝
② 실행 때:   실제 객체 기준으로 실행
             (객체가 오버라이딩했으면 그것, 아니면 물려받은 것)
```

### 스스로 확인한 경우의 수

| 부모(변수 타입)에 m | 자식(객체)에 m | 결과 |
|---|---|---|
| 있음 | 있음 (오버라이딩) | **자식** 것 실행 |
| 있음 | 없음 | 물려받은 **부모** 것 실행 |
| **없음** | 있음 | **컴파일 에러** (허락 못 받음) |

세 번째 줄이 `b.hunt()`다. 실제 객체가 hunt를 갖고 있어도 **허락을 못 받아서** 객체까지 가지도 못한다.

---

## 3. "가진 메서드"는 눈에 보이는 것만이 아니다

### 처음 생각 (오답)
```java
interface MakeDonut {
    default void make() { System.out.println("도넛을 만듭니다."); }
}
class Donut implements MakeDonut { }   // 안이 비어 있음

Donut d = new Donut();
d.make();   // 내 답: Donut 안에 make가 없으니 컴파일 에러
```

### 원리
"변수 타입이 가진 메서드" = **직접 쓴 것 + 물려받은 것**

```
Donut이 가진 메서드
 ├─ 직접 쓴 것:   없음
 └─ 물려받은 것:  make()  ← implements MakeDonut (default)
```
`d.make()` → 허락 O → 물려받은 make 실행 → `도넛을 만듭니다.`

`b.hunt()`가 에러였던 건 Bird가 hunt를 **직접 쓰지도, 물려받지도 않아서**다. 그래서 **"클래스 안에 없다"고 판단하기 전에 `extends`, `implements` 뒤를 먼저 본다.**

---

## 4. 가장 오래 막힌 곳: 부모 메서드 "안에서" 부른 메서드

### 처음 생각 (오답)
```java
class Animal {
    void sound() { System.out.println("..."); }
    void eat() {
        System.out.println("냠냠");
        sound();                      // ← 여기
    }
}
class Cat extends Animal {
    void sound() { System.out.println("야옹"); }
}

Animal a = new Cat();
a.sound();   // 내 답: 야옹      ✅
a.eat();     // 내 답: 냠냠 / ... ❌ (정답: 냠냠 / 야옹)
```
`a.sound()`는 맞혔는데 `eat()` 안의 `sound()`는 `...`이라고 했다. "eat 코드가 Animal에 적혀 있으니 그 안의 sound도 Animal 것"이라고 생각했다.

### 시도한 설명들
1. **2층집 비유** (1층 Animal, 2층 Cat, 호출은 항상 2층부터) → 그림은 이해했지만 eat 안의 호출에는 적용이 안 됐다
2. **this와 메서드 목록표** → `this`라는 새 단어가 나와서 오히려 더 헷갈렸다
3. **짧은 질문을 하나씩 주고받기** → 여기서 풀렸다

### 풀린 질문
> eat 안의 `sound();`는 `a.sound();`를 한 번 더 부르는 것과 같다. 그럼 뭐가 출력될까?

이미 맞혔던 ①번 `a.sound()`와 **같은 것**으로 연결하니 바로 "야옹"이 나왔다.

### 원리
```
a.eat()
 └ Cat에 eat 없음 → 물려받은 Animal.eat 실행
     ├ "냠냠"
     └ sound()   ← 지금 eat을 실행하는 건 a의 객체(Cat)
                  → a.sound()와 같음 → Cat.sound → "야옹"
```
코드가 **적힌 곳**(Animal)과 코드를 **실행하는 객체**(Cat)는 다르다. 엄마가 쓴 레시피에 "네 목소리로 울어라"라고 적혀 있어도, 고양이가 따라 하면 "야옹"이다.

```java
Animal z = new Animal();
z.eat();     // 냠냠 / ...   ← 진짜 Animal 객체일 때만 "..."
```

### 깨달음
**부모 메서드 안에서 부른 메서드도, 처음 호출한 그 객체 기준으로 다시 검사 2번을 한다.** `super.m()`만 예외로 부모 것으로 바로 간다.

---

## 5. 캐스팅은 객체를 만들지 않는다

### 처음 생각 (오답)
```java
Animal c = a;
Cat k = (Cat) c;
```
`(Cat) c`를 `new Cat()`처럼, 즉 Cat 객체를 **새로 만드는 것**으로 읽었다. 또 `(Cat) c`를 하면 **c 자체의 타입이 Cat으로 바뀐다**고 생각했다.

### 원리 (직접 확인)
```java
Cat d1 = new Cat();
Animal d2 = d1;
Cat d3 = (Cat) d2;

System.out.println(d1 == d2);   // true  같은 객체
System.out.println(d1 == d3);   // true  같은 객체

Cat other = new Cat();
System.out.println(d1 == other);   // false  new는 새 객체
```

| | 바뀌나? |
|---|---|
| 객체 | **안 바뀜, 새로 안 생김** |
| `c`의 변수 타입 | **안 바뀜** (계속 Animal → `c.climb()`은 여전히 에러) |
| 새 변수 `k` | Cat 타입으로 **같은 객체**를 가리킴 |

`(Cat)`이 필요한 이유는 컴파일러가 `c`를 Animal로만 알기 때문이다. Animal 변수에는 Dog이 들어 있을 수도 있으니, "이 안에 Cat이 있다"고 **약속**해 줘야 한다. 약속이 틀리면 실행 중에 `ClassCastException`이 난다.

### 그림을 그리는 규칙을 바꿨다
처음엔 줄마다 객체를 새로 그리고, 화살표를 **타입 이름(Sellable)**으로 향하게 그렸다.

```
❌ 처음 그림                         ✅ 고친 그림
d1 → (ChocoDonut)                   d1 [ChocoDonut] ─┐  pay, pack, smell
d2 → [Sellable] ← (Choco)(Choco)    d2 [Sellable]   ─┼─▶ ( ChocoDonut 객체 1개 )
d3 → (Choco)(Choco)(Choco)          d3 [ChocoDonut] ─┘  pay, pack, smell
                                    (d2는 pay, pack만 허락)
```
- 왼쪽 네모 = **변수** (이름 [타입] + 허락되는 메서드)
- 오른쪽 동그라미 = **객체**, `new` 줄에서만 하나 추가
- 화살표는 항상 **객체**로

---

## 6. 추상 클래스에서 헷갈린 것

### 처음 생각 (오답)
- 추상 메서드를 **다 구현한** 자식에도 `abstract`를 붙여야 한다고 봤다.
- `new Shape()`(추상 클래스)를 "쓸 이유가 없는 코드"라고만 하고 에러인 줄 몰랐다.
- 반대로 `abstract`가 붙은 자식이 추상 메서드를 일부만 구현한 것은 에러라고 봤다.

### 원리
```java
abstract class Animal {
    abstract void sound();
    abstract void move();
}
abstract class Bird extends Animal {     // move만 구현, sound는 다음 자식에게 넘김 → OK
    void move() { System.out.println("난다"); }
}
class Eagle extends Bird {               // 남은 sound를 구현 → 일반 클래스 완성
    void sound() { System.out.println("끼룩"); }
}
class Sparrow extends Bird { }           // 컴파일 에러: sound가 아직 비어 있음
```
```
Animal (숙제 2개: sound, move)
  └ Bird (move 해결, sound 넘김) ← abstract라 OK
      ├ Eagle (sound 해결) ← 숙제 끝, new 가능
      └ Sparrow (sound 안 함, abstract도 없음) ← 에러
```

### 깨달음
`abstract`는 "**아직 비어 있는 메서드가 남아 있다**"는 표시다. 다 채우면 붙이지 않고, 덜 채웠으면 붙여서 숙제를 넘긴다.

---

## 7. 인터페이스에서 헷갈린 것

| 처음 생각 (오답) | 원리 |
|---|---|
| 인터페이스에 없는 추가 메서드에도 `public`이 필수? | `public` 필수는 **인터페이스에 약속된 메서드만** (원래 public이라 좁힐 수 없음) |
| `public`과 `void` 중 하나만 쓰나? | `public` = 접근 제어자, `void` = 반환형. **역할이 다름** |
| 인터페이스는 변수를 못 가진다 | 쓰면 자동으로 **상수**(`public static final`)가 됨. 읽기 O, 수정 X |
| `static` 메서드도 `d.printStart()`로 부른다 | 인터페이스 static은 **물려받지 않음** → `인터페이스이름.메서드()`만 |
| 여러 인터페이스에 같은 이름 추상 메서드가 있으면 충돌? | 클래스가 **한 번만 구현**하면 둘 다 해결 |
| 추상 클래스로 여러 개 상속하면 되지 않나? | 추상 클래스도 클래스라 `extends`는 **1개만** |

```java
interface A { int x = 10; }
// A.x = 20;   // 컴파일 에러: cannot assign a value to static final variable x
```

---

## 8. 생성자 흐름에서 헷갈린 것

### 처음 생각 (오답)
1. `Donut d = new Donut();` 줄에서 생성자가 실행되며 **출력이 나오는 것**을 놓쳤다.
2. `this("철수")`로 넘어간 생성자에 **숨은 `super()`**가 있다는 걸 놓쳐서 부모 생성자 출력을 빼먹었다.
3. 과제 그림에서 "Grandfather → Father → Son 순으로 생성자 **호출**"이라고 썼다 (호출 순서는 반대).
4. 과제 그림에 `class Grandfather() {`처럼 **클래스 선언에 괄호**를 붙였다.

### 원리
```java
class Father {
    Father() { System.out.println("아버지 생성자"); }
}
class Son extends Father {
    Son() {
        this("철수");                      // this가 있으면 super()는 자동으로 안 들어감
        System.out.println("Son 기본 생성자");
    }
    Son(String name) {
        // super();  ← this가 없는 이쪽에 숨어 있음
        System.out.println("Son 이름 생성자: " + name);
    }
}
new Son();
// 아버지 생성자
// Son 이름 생성자: 철수
// Son 기본 생성자
```
```
호출:         Son() → Son(String) → Father()      (아래 → 위)
실행 완료:    Father → Son(String) → Son()         (위 → 아래)
```
```java
class Grandfather {          // 클래스 선언: 괄호 없음
    Grandfather() { }        // 생성자: 괄호 있음
}
```

### 깨달음
- `new` = 객체 생성 + **생성자 실행**. 코드를 읽을 때 생성자부터 표시해 둔다
- 어떤 경로로 가든 **부모 생성자는 반드시 한 번, 가장 먼저** 실행된다

---

## 9. 이 과정에서 만든 "코드 읽는 순서"

같은 실수를 반복하지 않으려고 정한 순서다.

1. `extends`, `implements`만 보고 **관계도**를 그린다
2. 각 클래스에서 **생성자, 같은 이름 메서드(오버라이딩), `super.`/`this.`/그냥 호출, `static`**에 표시한다
3. **main을 한 줄씩** 읽으며 줄의 종류를 판단한다
   - `new` → 객체 추가 + 생성자로 점프
   - `=` / 캐스팅 → 변수만 추가, 화살표는 기존 객체로
   - `x.m()` → 허락(변수 타입) → 실행(객체 타입)
   - `인터페이스이름.m()` → static 실행
4. 메서드 안에서 또 호출하면 **같은 객체 기준**으로 3번 반복
5. 옆에 **출력 결과**와 **변수-객체 그림**을 계속 갱신한다

---

## 정리

| 착각 | 바로잡은 규칙 |
|---|---|
| 부모 먼저 보고 없으면 자식 | ① 변수 타입이 **허락** ② **객체**가 실행 |
| 부모에 없고 자식에만 있으면 정상 | **컴파일 에러** |
| 클래스 안이 비면 메서드 없음 | **물려받은 것**도 가진 것 |
| 부모 메서드 안의 호출은 부모 것 | **처음 호출한 객체** 기준 |
| 캐스팅 = 새 객체 / 원래 변수 타입 변경 | 객체 그대로, **새 변수**가 같은 객체를 가리킴 |
| 다 구현한 자식도 abstract | 비어 있는 메서드가 **남아 있을 때만** |
| new 줄은 출력 없음 | **생성자가 실행**됨 |
| this()로 가면 super 없음 | **도착한 생성자**에 숨은 super() |
