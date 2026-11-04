# 4주차 Deep Dive · 객체, 참조, 생성자, this에서 헷갈렸던 것

> 개념 요약: [week04.md](week04.md)
>
> **틀렸던 것 → 처음 생각 → 원리 → 깨달음** 순서의 기록

---

## 1. 객체를 대입하면 "주소"가 복사된다

### 처음 생각 (오답)
`Student s2 = s1;`을 하면 s1과 똑같은 학생이 **하나 더** 생긴다고 생각했다.

### 원리
```java
Student s1 = new Student("철수");
Student s2 = s1;        // new 없음 → 객체는 그대로 1개
s2.name = "영희";
System.out.println(s1.name);   // 영희
```
```
 스택                 힙
 s1 [0x100] ──┐
              ├──▶  0x100: Student { name = "영희" }
 s2 [0x100] ──┘
```

### 깨달음
**객체는 `new`를 쓸 때만 생긴다.** `=`는 주소를 복사할 뿐이라, 두 변수는 같은 객체를 함께 가리킨다.

---

## 2. `NullPointerException`은 "점(.) 왼쪽"이 null일 때

### 처음 생각 (오답)
`null`이 어디에 있든 출력하면 예외가 난다고 생각했다.

### 원리
```java
String s = null;
System.out.println(s);            // null 출력 (예외 아님)
System.out.println(s.length());   // NullPointerException
```
`s.length()`는 "s가 가리키는 객체의 length를 실행해라"인데, 가리키는 객체가 **없다.**

```
s [null] ──▶ (없음)
   │
   └─ .length()  →  갈 곳이 없음 → NPE
```

### 깨달음
NPE를 찾을 때는 **점(.) 바로 왼쪽**이 null인지 본다.

---

## 3. 필드 기본값과 `this` 없는 대입

### 처음 생각 (오답)
생성자에서 `x = x;`라고 쓰면 필드 x에 값이 들어간다고 생각했다.

### 원리
```java
class Point {
    int x;                 // 필드 (기본값 0)

    Point(int x) {         // 매개변수 x
        x = x;             // 매개변수 x에 매개변수 x를 대입 → 필드는 그대로
    }
}

Point p = new Point(5);
System.out.println(p.x);   // 0
```
메서드 안에서 이름이 같으면 **가까운 쪽(매개변수)**이 이긴다.

```java
Point(int x) {
    this.x = x;            // this.x = 이 객체의 필드
}
// p.x → 5
```

| 변수 | 기본값 |
|---|---|
| 필드 `int` | 0 |
| 필드 `double` | 0.0 |
| 필드 `boolean` | false |
| 필드 참조형 | null |
| **지역 변수** | **없음** (초기화 안 하고 쓰면 컴파일 에러) |

### 깨달음
`this.`가 붙어야 **필드**다. 이름이 같을 때 `this`가 없으면 필드는 기본값(0) 그대로 남는다.

---

## 4. 실행 순서는 "파일에 적힌 순서"가 아니라 "호출 순서"

### 처음 생각 (오답)
코드를 위에서 아래로 적힌 순서대로 실행된다고 생각해서, main 위에 있는 클래스의 메서드부터 실행된다고 봤다.

### 원리
자바 프로그램은 **main에서 시작**한다. 다른 메서드와 생성자는 **호출될 때만** 실행된다.

```java
class A {
    A() { System.out.println("A 생성자"); }
    void hello() { System.out.println("hello"); }
}

public class Main {
    public static void main(String[] args) {
        System.out.println("시작");
        A a = new A();          // 이때 A 생성자 실행
        a.hello();              // 이때 hello 실행
    }
}
// 시작 / A 생성자 / hello
```

### 깨달음
출력 순서 문제는 **main을 한 줄씩 따라가면서**, `new`를 만나면 생성자로, `.메서드()`를 만나면 그 메서드로 **점프**한다.

---

## 5. 어떤 생성자가 실행될지는 `new`의 인자가 정한다

### 처음 생각 (오답)
생성자가 여러 개면 위에 있는 것부터 차례로 실행된다고 생각했다.

### 원리
```java
class Car {
    String color;
    int speed;

    Car() {
        this("흰색");                       // ② Car(String)으로 이동
        System.out.println("기본 생성자");   // ⑤
    }
    Car(String color) {
        this(color, 0);                      // ③ Car(String, int)로 이동
        System.out.println("색 생성자");     // ④
    }
    Car(String color, int speed) {
        this.color = color;
        this.speed = speed;
        System.out.println("전체 생성자");   // ③-1
    }
}

new Car();          // ① 인자 없음 → Car()부터 시작
// 전체 생성자 / 색 생성자 / 기본 생성자

new Car("빨강");    // 인자 String 1개 → Car(String)부터 시작
// 전체 생성자 / 색 생성자
```
```
new Car()
 └ Car() ─this("흰색")─▶ Car(String) ─this(color,0)─▶ Car(String,int)
                                                      "전체 생성자"
                         ◀──────── 돌아옴 ────────────
                         "색 생성자"
   ◀──── 돌아옴 ─────────
   "기본 생성자"
```

### 깨달음
- 시작 생성자는 `new`의 **인자 모양**으로 결정된다
- `this()`가 **있을 때만** 다른 생성자로 이어진다
- 한 칸씩 내려갔다가, 끝에서부터 **거꾸로 돌아오면서** 나머지 줄을 실행한다

---

## 6. 인스턴스 필드는 `new` 할 때마다 생긴다

### 처음 생각 (오답)
서술형에서 인스턴스 필드가 "**클래스가 생길 때**" 만들어진다고 썼다.

### 원리
```java
class Dog { int age; }

Dog d1 = new Dog();   // d1의 age 생성
Dog d2 = new Dog();   // d2의 age 따로 생성
d1.age = 3;
System.out.println(d2.age);   // 0
```
```
d1 ──▶ Dog { age = 3 }
d2 ──▶ Dog { age = 0 }     ← 객체마다 자기 필드
```
클래스에 1개만 있는 건 `static` 필드다 (5주차).

### 깨달음
인스턴스 필드 = **객체마다 하나씩**, `new` 할 때 생성.

---

## 정리

| 착각 | 바로잡은 규칙 |
|---|---|
| 객체 대입 = 객체 복제 | **주소 복사**, 객체는 new에서만 생김 |
| null 출력 = 예외 | **점 왼쪽**이 null일 때 NPE |
| `x = x`로 필드 저장 | `this.x = x` |
| 파일 순서대로 실행 | **main부터 호출 순서**대로 |
| 생성자 위에서부터 실행 | `new`의 인자로 시작 생성자 결정, `this()`로만 이어짐 |
| 필드는 클래스가 생길 때 | **new 할 때마다** 객체별로 |
