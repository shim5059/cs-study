# 6주차 Deep Dive · 예외 던지기, 상속, 캐스팅, 바인딩에서 헷갈렸던 것

> 개념 요약: [week06.md](week06.md)
>
> **틀렸던 것 → 처음 생각 → 원리 → 깨달음** 순서의 기록

---

## 1. `throw`가 실행되면 그 메서드는 즉시 끝난다

### 처음 생각 (오답)
다른 메서드 안에서 `throw`가 실행되어도 그 메서드의 나머지 줄과 main의 다음 줄이 실행된다고 봤다.

### 원리
```java
static void check(int n) {
    if (n < 0) throw new IllegalArgumentException("음수");
    System.out.println("통과 " + n);
}

public static void main(String[] args) {
    try {
        check(-1);                       // ① 예외 발생
        check(5);                        // 건너뜀
        System.out.println("try 끝");    // 건너뜀
    } catch (IllegalArgumentException e) {
        System.out.println("잡음");      // ②
    }
    System.out.println("main 계속");     // ③
}
// 잡음 / main 계속
```
```
check(-1) ──throw──▶ check 즉시 종료
                         │ 예외가 부른 쪽으로 올라감
                         ▼
main의 try 나머지 건너뜀 ──▶ catch ──▶ 다음 줄
```

### 깨달음
예외는 **던져진 곳에서 멈추고, 잡아 줄 catch를 찾아 위(부른 쪽)로 올라간다.**

---

## 2. `throw`와 `throws`는 다른 것

| | `throw` | `throws` |
|---|---|---|
| 종류 | **동작** (예외를 지금 던짐) | **선언** (이 메서드는 예외를 밖으로 넘길 수 있음) |
| 위치 | 메서드 **안** | 메서드 **선언부** |
| 예 | `throw new Exception();` | `void read() throws IOException` |

### 처음 생각 (오답)
- `throw new ArithmeticException()`도 try-catch나 throws가 없으면 **컴파일 에러**라고 봤다.
- `throws`로 넘긴 메서드 `c()`가 에러라고 골랐다. 실제로 에러인 건 그 메서드를 **처리 없이 부른 쪽** `a()`였다.

### 원리
```java
static void c() throws java.io.IOException {   // 체크 예외를 밖으로 넘김 (OK)
    throw new java.io.IOException();
}
static void a() {
    c();          // 컴파일 에러: 넘겨받은 체크 예외를 처리 안 함
}

static void d() {
    throw new ArithmeticException();   // 비체크 → 처리 없어도 컴파일 OK
}
```

### 깨달음
1. 먼저 **체크인지 비체크인지** 판단한다 (비체크면 컴파일러가 신경 안 씀)
2. 체크 예외라면 `throws`로 넘긴 쪽이 아니라 **넘겨받은 쪽(부른 쪽)**에 처리 의무가 생긴다

---

## 3. `new Dog[3]`과 `new Dog(3)`

### 처음 생각 (오답)
`new Dog[3]`을 생성자 호출처럼 읽었다.

### 원리
```java
Dog[] dogs = new Dog[3];   // 대괄호: 칸 3개짜리 "배열" 생성, Dog 객체는 0개
Dog d = new Dog(3);        // 소괄호: Dog(int) "생성자" 호출, 객체 1개
```
```
new Dog[3]  →  dogs ──▶ [null, null, null]   (생성자 호출 없음)
new Dog(3)  →  d    ──▶ Dog { ... }          (생성자 실행)
```
`int[] arr`에서도 `int[]`가 **타입**, `arr`가 **변수 이름**이다.

---

## 4. 상속: 방향, 물려받기, 생성자

### 처음 생각 (오답)
- `class Child extends House`를 "House가 Child를 물려받는다"고 반대로 말했다.
- 자식이 안 쓴 메서드는 실행해도 **출력이 없다**고 봤다.
- 일반 메서드 `sound()`를 생성자로 보고 `new` 할 때 실행된다고 봤다.
- "생성자는 한 번만 호출된다"고 생각했다.
- 생성자를 안 쓴 자식은 부모 생성자도 실행 안 된다고 봤다.

### 원리
```java
class Animal {
    Animal() { System.out.println("새 생성"); }
    void sound() { System.out.println("..."); }
}
class Cat extends Animal { }   // 생성자도 sound도 안 씀

Cat c1 = new Cat();   // 새 생성  ← 자동 생성자의 super()
Cat c2 = new Cat();   // 새 생성  ← new 할 때마다 다시
c1.sound();           // ...      ← 물려받은 sound
```
```
class Cat extends Animal      →   Cat이 Animal을 "물려받는다"
      자식        부모

컴파일러가 Cat에 자동으로 넣는 것:
    Cat() { super(); }        →   new Cat() 할 때마다 Animal() 먼저 실행
```

| 구분 | 생성자 | 메서드 |
|---|---|---|
| 이름 | 클래스 이름과 같음 | 자유 |
| 반환형 | **없음** | 있음 (`void` 포함) |
| 실행 | `new` 할 때 자동 | **호출해야** 실행 |

### 깨달음
`extends` 왼쪽(자식)이 오른쪽(부모)을 **물려받는다**. 안 쓴 것은 물려받은 것으로 채워지고, 부모 생성자는 **객체를 만들 때마다** 실행된다.

---

## 5. 오버라이딩 규칙

### 처음 생각 (오답)
- 부모의 `public draw()`를 자식이 `void draw()`(default)로 오버라이딩한 것을 **정상**으로 봤다.
- `@Override`가 있어야 오버라이딩이라고 생각했다.
- 서로 다른 클래스(상속 관계 아님)에 있는 같은 이름 `f()`를 같은 메서드로 봤다.

### 원리
```java
class Shape {
    public void draw() { }
}
class Circle extends Shape {
    void draw() { }   // 컴파일 에러: public → default로 범위를 좁힘
}
```
- 오버라이딩 조건: 상속 관계 + 이름·매개변수·반환형 같음 + 접근 범위 **좁히기 금지**
- `@Override`는 **선택**. 붙이면 위 조건을 컴파일러가 검사해 준다
- 상속 관계가 없는 두 클래스의 `f()`는 이름만 같은 **서로 다른 메서드**다

---

## 6. instanceof와 다운캐스팅 실패

### 처음 생각 (오답)
- `instanceof`가 "정확히 그 클래스일 때만 true"라고 봤다.
- `if (b instanceof Cat)`이 false인데도 if 안의 다운캐스팅이 실행되어 예외가 난다고 봤다.
- 잘못된 다운캐스팅을 **컴파일 에러**라고 썼다.

### 원리
```java
Animal a = new Cat();
Animal b = new Dog();

System.out.println(a instanceof Cat);      // true
System.out.println(a instanceof Animal);   // true (자식 객체 instanceof 부모)

if (b instanceof Cat) {                    // false → 블록 전체를 건너뜀
    Cat c = (Cat) b;
}
System.out.println("끝");                  // 정상 출력

Cat x = (Cat) b;   // 컴파일 OK, 실행 중 ClassCastException
```
컴파일러는 `b`를 Animal 타입으로만 안다. Animal 변수에는 Cat이 들어 있을 수도 있으니 **허락**하고, 실제 객체는 **실행해야** 안다.

---

## 7. 필드는 변수 타입, 메서드는 실제 객체 (바인딩)

### 처음 생각 (오답)
- `println(p.x)`를 `show()` 출력처럼 봤다.
- 필드를 **실제 객체 기준**으로 읽었다(`a.v` → 자식 값).
- 다운캐스팅한 변수의 필드·메서드를 **부모 것**으로 읽었다.
- 변수표는 맞게 채워 놓고 출력을 쓸 때 표의 칸을 **거꾸로** 읽었다.
- 정적/동적 바인딩의 정의를 서로 바꿔 썼다.

### 원리
```java
class P { int x = 10; void show() { System.out.println("P " + x); } }
class C extends P { int x = 20; void show() { System.out.println("C " + x); } }

P p = new C();
C c = (C) p;

System.out.println(p.x);   // 10   필드 → 변수 타입 P
p.show();                  // C 20 메서드 → 실제 객체 C
System.out.println(c.x);   // 20   필드 → 변수 타입 C
c.show();                  // C 20 메서드 → 실제 객체 C
```

먼저 변수표를 만든다.

| 변수 | 변수 타입 (= 왼쪽) | 실제 객체 (new 뒤) |
|---|---|---|
| `p` | P | C |
| `c` | C | C |

```
필드  x      → 표의 "변수 타입" 칸   (정적 바인딩: 컴파일 때 결정)
메서드 show() → 표의 "실제 객체" 칸   (동적 바인딩: 실행 때 결정)
```

- `show()`는 `void`라서 `println(p.show())`처럼 쓰면 **컴파일 에러**

### 깨달음
**"필드는 = 왼쪽, 메서드는 new 뒤."** 출력 문제는 변수표부터 그리고, 줄마다 필드인지 메서드인지 확인한 뒤 표의 칸을 고른다.

---

## 정리

| 착각 | 바로잡은 규칙 |
|---|---|
| throw 후에도 다음 줄 실행 | 메서드 즉시 종료 → **위로 올라가 catch** |
| 비체크 throw = 컴파일 에러 | 비체크면 **컴파일 OK** |
| throws 붙은 쪽이 에러 | **부른 쪽**에 처리 의무 |
| `new Dog[3]` = 생성자 | 대괄호는 **배열**, 소괄호는 생성자 |
| 상속 방향 반대 | `extends` **왼쪽이 물려받음** |
| 생성자는 한 번만 | **new 할 때마다** |
| default로 오버라이딩 OK | 범위 **좁히기 금지** |
| instanceof는 정확히 그 클래스만 | **부모 클래스도 true** |
| 잘못된 다운캐스팅 = 컴파일 에러 | **실행 중** ClassCastException |
| 필드를 객체 기준으로 | 필드 = **변수 타입**, 메서드 = **실제 객체** |
