# 5주차 · 메서드, 메모리, 패키지, static, 예외 처리

> 헷갈렸던 부분과 해결 과정: [week05-deep-dive.md](week05-deep-dive.md)

> 교재 5장

## 1. 오버로딩 vs 오버라이딩

| | 오버로딩 | 오버라이딩 |
|---|---|---|
| 뜻 | 같은 이름, **매개변수가 다른** 메서드 여러 개 | 부모 메서드를 자식이 **고쳐 씀** (교체) |
| 위치 | 같은 클래스 | 부모-자식 |
| 조건 | 매개변수 개수·타입이 달라야 함 | 이름·매개변수·반환형 같음, 접근 범위를 **좁히면 안 됨** |
| 어느 걸 부를지 | **컴파일 때 인자 타입**으로 결정 | **실행 때 실제 객체**로 결정 |

```java
class O {
    int add(int a, int b) { return a + b; }
    double add(double a, double b) { return a + b + 0.5; }
    String add(String a, int b) { return a + b; }
}
O o = new O();
o.add(1, 2);       // 3
o.add(1.0, 2.0);   // 3.5
o.add("x", 3);     // x3
o.add(1, 2.0);     // 3.5  (int, double에 딱 맞는 게 없음 → 1이 1.0으로 바뀌어 double 버전)
```
- 반환형만 다른 것은 오버로딩이 아님 (컴파일 에러)

## 2. 매개변수 전달
- **기본형** 전달 → 값 복사 → 메서드 안에서 바꿔도 원본 그대로
- **참조형** 전달 → 주소 복사 → 메서드 안에서 객체 내용을 바꾸면 원본도 바뀜

## 3. 메모리 구조

| 영역 | 저장하는 것 | 수명 |
|---|---|---|
| 스택 | 메서드 실행 중 지역 변수, 매개변수 | 메서드가 끝나면 자동 소멸 |
| 힙 | `new`로 만든 **객체** | 가리키는 변수가 없으면 **가비지 컬렉터**가 정리 |

```java
String[] fruits = {"사과", "바나나", "체리"};
fruits[1] = "포도";   // "바나나" 객체는 연결이 끊김 → 가비지
```

## 4. 패키지와 import
- **패키지**: 클래스를 하나의 이름 공간으로 묶은 단위
- 다른 패키지의 클래스는 `import`로 가져옴

```java
import java.util.Scanner;   // java.util 패키지의 Scanner 클래스
```

## 5. 접근 제한자

| 제한자 | 같은 클래스 | 같은 패키지 | 다른 패키지의 자식 | 전체 |
|---|:-:|:-:|:-:|:-:|
| `public` | O | O | O | O |
| `protected` | O | O | O | X |
| (default, 안 씀) | O | O | X | X |
| `private` | O | X | X | X |

- 아무것도 안 쓰면 **default** (public이 기본값이 아님)
- 접근 제한은 **이름을 쓸 수 있는 위치**의 제한일 뿐. 클래스 안의 public 메서드는 private 필드를 정상 사용

## 6. getter / setter
```java
class Account {
    private int balance;

    public int getBalance() { return balance; }

    public void setBalance(int balance) {
        if (balance >= 0) this.balance = balance;
    }
}
```
- 필드는 `private`, 접근은 메서드로 → 잘못된 값 차단
- `final` 필드는 setter가 있어도 값을 바꿀 수 없음

## 7. static
- 객체가 아니라 **클래스에 1개**, 모든 객체가 공유
- `클래스이름.멤버`로 사용 (객체 없이 사용 가능)
- static 메서드도 **호출해야** 실행됨
- static 메서드 안에서 인스턴스 필드를 못 쓰는 이유: **어느 객체의 필드인지 알 수 없어서**

```java
class Counter {
    static int count = 0;   // 모든 객체가 공유
    Counter() { count++; }
}
```

- `static final`: 객체 없이 접근하는 **바뀌지 않는 상수** (`Math.PI`처럼)
- **불변 객체**: 생성된 뒤 상태를 바꿀 수 없는 객체 (`String`이 대표)

## 8. 예외 처리

| | 체크 예외 | 비체크 예외 |
|---|---|---|
| 확인 시점 | **컴파일러가** 처리 여부 검사 | 실행 중 발생, 컴파일러가 강제 안 함 |
| 처리 안 하면 | **컴파일 에러** | 컴파일 OK, 실행 중 터짐 |
| 예 | `Thread.sleep()`, 파일 입출력 | `10 / 0`, 없는 배열 칸, `null.length()` |

```java
try {
    int x = 10 / 0;              // 예외 발생 → 아래 줄 건너뜀
    System.out.println("안 보임");
} catch (ArithmeticException e) {
    System.out.println("0으로 나눔");
} finally {
    System.out.println("항상 실행");
}
System.out.println("계속 실행");  // 잡았으면 프로그램은 안 죽음
```
- 예외가 없으면 `catch`는 실행 안 됨
- **try-with-resources** (자바 7+): `try (자원 선언) { }` → 자원을 자동으로 닫음

### 실행 순서 (복습 추가)

| 상황 | 순서 |
|---|---|
| 예외 안 남 | try **전부** → catch 건너뜀 → finally → 다음 코드 |
| 예외 남 | try에서 **예외 난 줄까지** → 맞는 catch **하나** → finally → 다음 코드 |

```java
try {
    System.out.print("1 ");
    int x = 10 / 0;              // 예외 → 아래 줄 건너뜀
    System.out.print("2 ");
} catch (ArithmeticException e) {
    System.out.print("3 ");
} finally {
    System.out.print("4 ");
}
System.out.println("5");
// 1 3 4 5   (10 / 2처럼 예외가 없으면 1 2 4 5)
```

### catch가 여러 개면 위에서부터 첫 번째 맞는 것 하나만
```java
int[] a = new int[2];               // 0번, 1번 칸만 있음
try {
    System.out.print("A");
    a[2] = 5;                       // 없는 칸 → ArrayIndexOutOfBoundsException
    System.out.print("B");
} catch (ArithmeticException e) {   // 종류가 다름 → 통과
    System.out.print("C");
} catch (Exception e) {             // 모든 예외의 부모 → 잡힘
    System.out.print("D");
} finally {
    System.out.print("E");
}
System.out.print("F");
// ADEF
```
- `Exception`(부모) catch를 자식 catch보다 **위에** 쓰면 컴파일 에러 (아래 catch에 도달 불가)

### 자주 나오는 예외

| 예외 | 언제 |
|---|---|
| `ArithmeticException` | **정수**를 0으로 나눔 (`1.0 / 0`은 `Infinity`, 예외 아님) |
| `ArrayIndexOutOfBoundsException` | 없는 배열 칸 |
| `NullPointerException` | null로 메서드·필드 사용 |
| `NumberFormatException` | `Integer.parseInt("a")` |
| `ClassCastException` | 잘못된 다운캐스팅 |

### return과 finally
```java
static int f() {
    try {
        System.out.print("t ");
        return 1;                  // 돌아가기 직전에
    } finally {
        System.out.print("f ");    // finally 먼저 실행
    }
}
System.out.println(f());           // t f 1
```
- finally 안에도 return이 있으면 그 값이 이김: `try { return 1; } finally { return 2; }` → 2
