# 5주차 Deep Dive · 접근 제한자, static, final, 예외에서 헷갈렸던 것

> 개념 요약: [week05.md](week05.md)
>
> **틀렸던 것 → 처음 생각 → 원리 → 깨달음** 순서의 기록

---

## 1. `protected`는 "다른 패키지면 누구나"가 아니다

### 처음 생각 (오답)
- 처음엔 `protected`를 "다른 패키지에서도 누구나 접근 가능"으로 이해했다.
- 고친 뒤에도 시험 직전 정리에서 "다른 **클래스**의 자식"이라고 다시 틀리게 썼다.

### 원리
```
                같은 클래스   같은 패키지   다른 패키지의 자식   다른 패키지
public              O            O              O                O
protected           O            O              O                X
(default)           O            O              X                X
private             O            X              X                X
```
`protected` = **같은 패키지 전부** + **다른 패키지에서는 상속받은 자식만**

### 깨달음
`protected`는 default에 "**다른 패키지의 자식**"을 하나 더 열어 준 것이다. 기준은 클래스가 아니라 **패키지**다.

---

## 2. `private` 필드는 "값이 없는 것"이 아니다

### 처음 생각 (오답)
밖에서 `private` 필드를 못 쓰면 그 값이 0이 된다고 생각했다.

### 원리
```java
class Account {
    private int balance = 1000;

    public int getBalance() {
        return balance;          // 클래스 안에서는 정상 사용
    }
}

Account a = new Account();
// a.balance;                    // 컴파일 에러: 이름을 쓸 수 없는 위치
System.out.println(a.getBalance());   // 1000
```

### 깨달음
접근 제한은 **이름을 쓸 수 있는 위치**를 제한할 뿐, 값에는 아무 영향이 없다.

---

## 3. 컴파일 에러가 한 줄이라도 있으면 아무것도 실행되지 않는다

### 처음 생각 (오답)
에러 줄 전까지는 실행되고 출력이 나온다고 생각했다.

### 원리
```
소스 코드 ──컴파일──▶ .class 파일 ──실행──▶ 출력
             ▲
             └─ 에러가 하나라도 있으면 .class가 안 만들어짐 → 실행 단계로 못 감
```

### 깨달음
**컴파일 에러 = 프로그램 전체 실행 불가.** 실행 중 예외와는 단계가 다르다.

---

## 4. 컴파일러는 "실행"하지 않는다 (체크/비체크 예외)

### 처음 생각 (오답)
- 컴파일을 "첫 줄부터 실행해 보는 것"으로 생각했다.
- 그래서 `10 / 0`, `arr[3]`, `null.length()`를 **컴파일 에러**로, `Thread.sleep()`을 처리 없이 쓴 것을 **정상**으로 봤다.
- 서술형에서 체크 예외의 예로 0 나누기를 썼다.

### 원리
컴파일러는 값을 계산하지 않고 **문법과 규칙만** 검사한다.

| 코드 | 컴파일 | 실행 | 이유 |
|---|---|---|---|
| `int x = 10 / 0;` | OK | ArithmeticException | 비체크 (값은 실행해야 앎) |
| `arr[3]` (길이 3) | OK | ArrayIndexOutOfBounds | 비체크 |
| `s.length()` (s=null) | OK | NullPointerException | 비체크 |
| `Thread.sleep(100);` (처리 없음) | **에러** | — | **체크 예외 미처리** |

```java
public static void main(String[] args) {
    Thread.sleep(100);   // 컴파일 에러: unreported exception InterruptedException
}

public static void main(String[] args) throws InterruptedException {
    Thread.sleep(100);   // OK: throws로 넘김
}
```

### 깨달음
- **체크 예외**: 컴파일러가 "처리했니?"를 검사 → 안 하면 **컴파일 에러**
- **비체크 예외**: 컴파일러는 검사 안 함 → 문제가 있으면 **실행 중**에 터짐
- 컴파일 판정 문제는 실행 순서를 따라가지 말고 **규칙 위반만** 찾는다

---

## 5. 예외를 잡으면 프로그램은 계속 실행된다

### 처음 생각 (오답)
`catch`로 잡은 뒤에도 예외가 났으니 프로그램이 끝난다고 생각했다.

### 원리
```java
try {
    System.out.println("1");
    int x = 10 / 0;              // 예외 발생 → try 나머지 건너뜀
    System.out.println("2");     // 실행 안 됨
} catch (ArithmeticException e) {
    System.out.println("3");     // 잡음
} finally {
    System.out.println("4");     // 항상
}
System.out.println("5");         // 계속 실행
// 1 3 4 5
```

### 깨달음
**잡으면 안 죽는다.** try 안의 나머지만 건너뛰고, catch → finally → **다음 줄**로 이어진다.

---

## 6. static 메서드는 자동 실행되지 않는다

### 처음 생각 (오답)
- `static` 메서드는 프로그램이 시작하면 자동으로 실행된다고 생각했다.
- 서술형에서 static이 "**컴파일 시점**"에 생성된다고 썼다.

### 원리
- `static` = 객체가 아니라 **클래스에 1개**, 객체 없이 `클래스이름.메서드()`로 부를 수 있다는 뜻
- 메서드는 static이든 아니든 **호출해야** 실행된다
- static 필드는 클래스가 **처음 사용될 때(로딩될 때)** 준비된다 (컴파일 때가 아님)
- 호출되지 않는 메서드도 컴파일러는 **문법 검사를 한다**

---

## 7. static 메서드에서 인스턴스 필드를 못 쓰는 진짜 이유

### 처음 생각 (오답)
"인스턴스 필드는 아직 생성이 안 돼서" 못 쓴다고 설명했다.

### 원리
```java
class Dog {
    String name;                       // 객체마다 다른 값

    static void bark() {
        // System.out.println(name);   // 컴파일 에러
    }
}

Dog a = new Dog(); a.name = "바둑이";
Dog b = new Dog(); b.name = "흰둥이";
Dog.bark();     // 이때 name은 누구의 name?
```
객체가 이미 여러 개 있어도 에러다. `Dog.bark()`는 **특정 객체 없이** 불리기 때문에, 어느 객체의 `name`인지 정할 수 없다.

### 깨달음
정확한 이유는 "아직 없어서"가 아니라 **"어느 객체의 필드인지 알 수 없어서"**.

---

## 8. `final`의 세 가지 쓰임

### 처음 생각 (오답)
- `final` 메서드를 "**상속 불가**"로 썼다.
- `static final`을 "상속 방지"로, `final`에 "공유"의 의미를 섞었다.

### 원리
| 붙는 곳 | 뜻 |
|---|---|
| `final` 변수 | 값을 **바꿀 수 없음** (상수) |
| `final` 메서드 | **오버라이딩 불가** (상속은 됨, 고쳐 쓰기만 안 됨) |
| `final` 클래스 | **상속 불가** (`extends` 불가) |
| `static final` | 클래스에 1개 + 바꿀 수 없음 → **공유 상수** (`Math.PI`) |

"공유"는 `static`의 의미이고, `final`은 오직 "**바꿀 수 없음**"이다.

---

## 정리

| 착각 | 바로잡은 규칙 |
|---|---|
| protected = 다른 패키지 누구나 | 같은 패키지 + **다른 패키지의 자식** |
| private 필드는 0 | 이름을 쓸 **위치** 제한일 뿐 |
| 에러 줄 전까지 실행 | 컴파일 에러면 **전부 실행 안 됨** |
| 0 나누기 = 컴파일 에러 | **비체크**, 실행 중 예외 |
| catch 후 종료 | catch → finally → **다음 줄 계속** |
| static 자동 실행 | **호출해야** 실행 |
| static에서 필드 못 쓰는 이유 = 미생성 | **어느 객체인지 모름** |
| final 메서드 = 상속 불가 | **오버라이딩 불가** |
