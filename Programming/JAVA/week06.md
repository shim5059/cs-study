# 6주차 · 예외 던지기, 열거형, 상속과 다형성

> 헷갈렸던 부분과 해결 과정: [week06-deep-dive.md](week06-deep-dive.md)

> 교재 5장 후반 ~ 6장 (중간고사 범위: 3~6장, 추상 클래스 이전까지)

## 1. 예외 던지기
- `throw`: 예외를 **직접 발생**시키는 **동작**
- `throws`: "이 메서드는 이 예외를 밖으로 넘길 수 있다"는 **선언**

```java
static void check(int n) {
    if (n < 0) {
        throw new IllegalArgumentException("음수");
    }
    System.out.println("통과 " + n);   // throw 되면 실행 안 됨
}

public static void main(String[] args) {
    try {
        check(-1);                        // 예외 → check 즉시 종료 → main의 catch로
        System.out.println("안 보임");
    } catch (IllegalArgumentException e) {
        System.out.println("잡음: " + e.getMessage());
    }
}
```
- 비체크 예외는 `throw`로 던져도 try-catch 없이 **컴파일 OK**
- 체크 예외를 `throws`로 넘긴 메서드를 부르는 쪽은 **처리 의무**가 생김

## 2. 객체 배열
```java
Dog[] dogs = new Dog[3];      // 칸 3개짜리 배열, Dog 객체는 아직 없음 (전부 null)
dogs[0] = new Dog();          // 이때 객체 생성
```
- `new Dog[3]`(대괄호, 배열) ≠ `new Dog(3)`(소괄호, 생성자 호출)

## 3. 열거형 enum
- 서로 관련 있는 **고정된 상수**의 묶음

```java
enum Season { SPRING, SUMMER, FALL, WINTER }

Season s = Season.SUMMER;
```

## 4. 상속
```java
class Animal {
    void sound() { System.out.println("..."); }
}

class Cat extends Animal {
    @Override
    void sound() { System.out.println("야옹"); }   // 오버라이딩 (교체)
}
```
- `class 자식 extends 부모` — **한 번에 하나만** 상속
- 쓰는 이유: 중복 코드 제거, 메서드를 **고쳐 쓰기**(오버라이딩)
- `@Override`는 선택 사항 (붙이면 컴파일러가 오버라이딩 조건을 검사해 줌)
- 오버라이딩할 때 접근 범위를 **좁히면 컴파일 에러** (public → default ✗)
- `final` 메서드는 **오버라이딩 불가**, `final` 클래스는 **상속 불가**
- 자식 생성자 첫 줄에 `this(…)`나 `super(…)`가 **없으면** `super();`가 자동으로 들어감 → **부모 생성자가 먼저** 실행 (`new` 할 때마다, 자세한 흐름은 7주차)

## 5. 객체 캐스팅

```java
Animal a = new Cat();     // 업캐스팅 (자동)
Cat c = (Cat) a;          // 다운캐스팅 (괄호 필수)
```

| | 업캐스팅 | 다운캐스팅 |
|---|---|---|
| 방향 | 자식 → 부모 타입 | 부모 → 자식 타입 |
| 문법 | 자동 | `(자식타입)` 필수 |
| 실패 | 없음 | 실제 객체가 그 타입이 아니면 **실행 중** `ClassCastException` |

- 객체는 **새로 안 생김**. 바뀌는 건 **변수 타입**뿐

## 6. instanceof
```java
if (a instanceof Cat) {   // 실제 객체가 Cat(또는 Cat의 자식)이면 true
    Cat c = (Cat) a;
}
```
- 자식 객체 `instanceof 부모클래스`도 **true**
- 조건이 거짓이면 if 블록 전체를 건너뜀

## 7. 다형성과 바인딩

| | 정적 바인딩 | 동적 바인딩 |
|---|---|---|
| 결정 시점 | **컴파일** 때 | **실행** 때 |
| 기준 | **변수 타입** (`=` 왼쪽) | **실제 객체** (`new` 뒤) |
| 대상 | 필드, **static 메서드** | (오버라이딩된) 인스턴스 메서드 |

```java
class P { int x = 10; void show() { System.out.println("P " + x); } }
class C extends P { int x = 20; void show() { System.out.println("C " + x); } }

P p = new C();
System.out.println(p.x);   // 10  (필드: 변수 타입 P)
p.show();                  // C 20 (메서드: 실제 객체 C)
```
- 다형성 = **누가 하느냐(실제 객체)에 따라 동작이 달라진다**

### 필드 · static · super까지 섞인 경우 (복습 추가)
```java
class P {
    int v = 10;
    static String s() { return "Ps"; }
    void m1() {
        System.out.print("P1 ");
        m2();                                  // 실제 객체 C → C의 m2
    }
    void m2() { System.out.print("P2 " + v + " "); }   // P 안의 코드 → P의 v
}
class C extends P {
    int v = 20;
    static String s() { return "Cs"; }
    void m2() { System.out.print("C2 " + v + " "); }   // C 안의 코드 → C의 v
    void m3() { super.m2(); }                  // 부모 버전 강제 호출
}

P p = new C();
p.m1();                                        // P1 C2 20
((C) p).m3();                                  // P2 10
System.out.println(p.v + ((C) p).v);           // 30 (int + int → 덧셈)
System.out.println(p.s() + " " + ((C) p).s()); // Ps Cs (static은 변수 타입)
```
- 메서드 안에서 쓴 필드 이름은 **그 메서드가 쓰인 클래스의 필드**
