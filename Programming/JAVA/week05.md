# 5주차 · 메서드, 메모리, 패키지, static, 예외 처리

> 헷갈렸던 부분과 해결 과정: [week05-deep-dive.md](week05-deep-dive.md)

> 교재 5장

## 1. 오버로딩 vs 오버라이딩

| | 오버로딩 | 오버라이딩 |
|---|---|---|
| 뜻 | 같은 이름, **매개변수가 다른** 메서드 여러 개 | 부모 메서드를 자식이 **고쳐 씀** (교체) |
| 위치 | 같은 클래스 | 부모-자식 |
| 조건 | 매개변수 개수·타입이 달라야 함 | 이름·매개변수·반환형 같음, 접근 범위를 **좁히면 안 됨** |

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
