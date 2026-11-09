# 7주차 · 추상 클래스, 인터페이스, 캐스팅·생성자 정리

> 헷갈렸던 부분과 해결 과정: [week07-deep-dive.md](week07-deep-dive.md)

> 교재 6장 후반 (중간고사 이후 첫 수업)

## 1. 한 줄 읽는 법: `Animal a = new Cat();`

| 위치 | 이름 | 하는 일 |
|---|---|---|
| `=` 왼쪽 (`Animal`) | 변수 타입 | 메서드를 **불러도 되는지 허락**만 |
| `new` 뒤 (`Cat`) | 객체 타입 | **실제로 실행**할 것을 정함 |

- 객체는 **`new` 줄에서만** 생김. 캐스팅은 변수 타입만 바꾸고 객체는 그대로

### 메서드 호출 `x.m()` 검사 2번
1. **허락 (컴파일)**: 변수 타입이 **가진** 메서드(직접 쓴 것 + 물려받은 것)에 `m`이 있나? 없으면 컴파일 에러
2. **실행 (런타임)**: 실제 객체 기준. 오버라이딩했으면 그것, 아니면 물려받은 것
3. 메서드 **안에서** 부르는 `m()`(= `this.m()`)도 **같은 객체 기준**으로 다시 1, 2
4. `super.m()`만 예외로 부모 것을 바로 실행

```java
class Animal {
    void sound() { System.out.println("..."); }
    void eat() {
        System.out.println("냠냠");
        sound();                 // 실행 중인 객체의 sound
    }
}
class Cat extends Animal {
    void sound() { System.out.println("야옹"); }
    void climb() { System.out.println("나무 타기"); }
}

Animal a = new Cat();
a.eat();                // 냠냠 / 야옹
// a.climb();           // 컴파일 에러: Animal이 가진 메서드에 climb 없음
Cat k = (Cat) a;        // 같은 객체, 변수 타입만 Cat
k.climb();              // 나무 타기
System.out.println(a == k);   // true (같은 객체)
```

## 2. 추상 클래스
- **추상 메서드**: 내용 `{}` 없이 선언만 → `abstract void show();`
- 추상 메서드가 **하나라도** 있으면 클래스에 `abstract`
- `new` 불가, **변수 타입으로는 가능** (업캐스팅)
- 일반 필드·일반 메서드·생성자 가질 수 있음
- 자식은 추상 메서드를 **전부** 구현하거나, 자신도 `abstract`가 되어 다음 자식에게 넘김

```java
abstract class Donut {
    int price;
    void setPrice(int price) { this.price = price; }
    abstract void show();
}
class ChocoDonut extends Donut {
    void show() { System.out.println("초코 도넛 " + price + "원"); }
}

Donut d = new ChocoDonut();   // OK
// Donut x = new Donut();     // 컴파일 에러: 추상 클래스는 객체 생성 불가
```

## 3. 인터페이스
- 같은 **동사(기능)**에 대한 약속 (추상 클래스 = 비슷한 **명사**의 공통 부모)
- 메서드는 자동으로 `public abstract` → 구현할 때 **반드시 `public`**
- `implements`로 구현, **여러 개** 가능 (클래스 `extends`는 1개만)
- 변수는 자동 상수 `public static final`, **생성자 없음**, `new` 불가

```java
interface Sellable {
    void pack();
    void pay();
}
class ChocoDonut implements Sellable {
    public void pack() { System.out.println("포장"); }
    public void pay()  { System.out.println("결제"); }
    void smell()       { System.out.println("초코 향"); }   // 자기만의 메서드
}

ChocoDonut d1 = new ChocoDonut();
Sellable d2 = d1;                       // 업캐스팅: pack, pay만 허락
ChocoDonut d3 = (ChocoDonut) d2;        // 다운캐스팅: smell 다시 허락
// d2.smell();                          // 컴파일 에러
```

### default / static 메서드

| | default | static |
|---|---|---|
| 내용 | 있음 | 있음 |
| 물려받나 | 예 | **아니요** |
| 부르는 법 | `객체변수.메서드()` | `인터페이스이름.메서드()` |

```java
interface MakeDonut {
    default void make() { System.out.println("도넛을 만듭니다."); }
}
interface DonutUtil {
    static void printStart() { System.out.println("-- 시작 --"); }
}
class Donut implements MakeDonut { }

DonutUtil.printStart();     // -- 시작 --
new Donut().make();         // 도넛을 만듭니다. (물려받은 default)
```

## 4. 추상 클래스 vs 인터페이스

| | 추상 클래스 | 인터페이스 |
|---|---|---|
| 연결 | `extends` 1개 | `implements` 여러 개 |
| `new` | 불가 | 불가 |
| 필드 | 일반 필드 O | 상수만 (`public static final`) |
| 생성자 | O | X |
| 내용 없는 메서드 | `abstract` 붙임 | 자동 `public abstract` |
| 내용 있는 메서드 | 그냥 씀 | `default` 또는 `static` |

## 5. 생성자 호출 흐름 (super, this)
- 자식 생성자 첫 줄에 `super();` 자동 → 부모 생성자 먼저
- 부모 생성자가 값을 받으면 `super(값);`을 **직접** 써야 함 (안 쓰면 컴파일 에러)
- `this(값)`: 같은 클래스의 다른 생성자
- `super()`와 `this()`는 생성자 **첫 줄**에, **둘 중 하나만**
- `this()`가 있는 생성자에는 `super()`가 자동으로 안 들어가고, 마지막에 도착한 생성자에 들어감

```java
class Father {
    Father() { System.out.println("아버지 생성자"); }
}
class Son extends Father {
    Son() {
        this("철수");
        System.out.println("Son 기본 생성자");
    }
    Son(String name) {
        // super(); 숨어 있음
        System.out.println("Son 이름 생성자: " + name);
    }
}

new Son();
// 아버지 생성자
// Son 이름 생성자: 철수
// Son 기본 생성자
```
- 호출은 자식 → 부모 순서, **실행 완료(출력)**는 부모 → 자식 순서

### 공단 예시문제 8번 (기능사 실기)
```java
class Test1 {
    Test1() { System.out.print('X'); }
    Test1(char a) {
        this();
        System.out.print(a);
    }
}
class Test2 extends Test1 {
    Test2() {
        super();
        System.out.print('Y');
    }
    Test2(char a) {
        this();
        System.out.print(a);
    }
}

Test1 t1 = new Test2('Z');   // XYZ
```

| 순서 | 생성자 | 첫 줄 | 하는 일 |
|---|---|---|---|
| 1 | `Test2(char a)` | `this()` | `Test2()` 호출 |
| 2 | `Test2()` | `super()` | **인자 없는** `Test1()` 호출 |
| 3 | `Test1()` | (숨은 super → Object) | X |
| 4 | `Test2()` 복귀 | | Y |
| 5 | `Test2(char a)` 복귀 | | Z |

- `Test1(char a)`는 **아무도 부르지 않아서** 실행 안 됨. 생성자는 "누가 불렀는지"를 따라간다

```java
class A {
    A() { System.out.print("A"); }
    A(int n) { this(); System.out.print(n); }
}
class B extends A {
    B() { super(1); System.out.print("B"); }
    B(int n) { this(); System.out.print(n); }
}
new B(7);   // A1B7   (B(7) → B() → A(1) → A())
```
- 조상이 여러 단계면 맨 위부터 출력: `G ← Pa ← Ch`면 `new Ch()` → `GPaCh`

### 생성자 안에서 오버라이딩된 메서드를 부르면 (시험 단골 함정)
```java
class A {
    A() { print(); }                              // 실제 객체 B → B의 print
    void print() { System.out.print("A "); }
}
class B extends A {
    int x = 7;
    B() { print(); }
    void print() { System.out.print("B" + x + " "); }
}
new B();   // B0 B7
```

| 순서 | 일어나는 일 | B의 x |
|---|---|---|
| 1 | 힙에 B 객체 생성, 필드는 **기본값** | 0 |
| 2 | `B()` → 숨은 `super()` → `A()` → `print()` → **B의 print** | **0** → `B0` |
| 3 | `A()` 끝 → 이제야 **B의 필드 초기화** (`x = 7`) | 7 |
| 4 | `B()` 몸체의 `print()` | 7 → `B7` |

- **자식 필드 초기화는 부모 생성자가 끝난 뒤**. 그 전에 자식 메서드가 불리면 필드는 기본값(0, null, false)
- A에 `int x = 3;`이 있어도 결과는 같음 (B의 print는 **B의 x**를 읽음)

## 6. 과제: 배송 시스템 (교재 Lab 6-2)

인터페이스(동사) + 추상 클래스(명사) + 다형성을 한 번에 쓰는 예제

```
Deliverable (interface: pack, ship, confirm)
     ↑ implements
Product (abstract: name, 생성자)
     ↑ extends
Book, Food (super(name) + 메서드 3개)
```

```java
interface Deliverable {
    void pack();
    void ship();
    void confirm();
}

abstract class Product implements Deliverable {
    String name;
    Product(String name) { this.name = name; }
}

class Book extends Product {
    Book(String name) { super(name); }
    public void pack()    { System.out.println(name + ": 책 포장"); }
    public void ship()    { System.out.println(name + ": 책 배송 중"); }
    public void confirm() { System.out.println(name + ": 책 수령 완료"); }
}

class Food extends Product {
    Food(String name) { super(name); }
    public void pack()    { System.out.println(name + ": 식품 냉장 포장"); }
    public void ship()    { System.out.println(name + ": 냉장 배송 중"); }
    public void confirm() { System.out.println(name + ": 식품 수령 완료"); }
}

public class DeliveryExample {
    public static void main(String[] args) {
        Deliverable[] items = { new Book("미라클 자바"), new Food("딸기 도넛") };
        for (Deliverable item : items) {
            item.pack();
            item.ship();
            item.confirm();
        }
    }
}
```
- Product는 `abstract`라서 pack/ship/confirm을 안 써도 됨 → Book, Food가 **public으로** 전부 구현
- `Deliverable[]` 배열 = 업캐스팅, `item.pack()`은 허락은 Deliverable, 실행은 Book/Food
