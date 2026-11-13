# 8주차 Deep Dive · String Pool, equals 오버라이딩, 모듈 구조

> 개념 요약: [week08.md](week08.md)
>
> **의문 → 처음 생각 → 원리 → 깨달음** 순서의 기록. 7주차에 잡은 "변수(손잡이)와 객체(풍선)를 나눠 본다"는 관점이 이번 주 내용 전체를 푸는 열쇠였다.

---

## 1. String Pool로 주소를 공유하면 위험하지 않을까?

### 의문
```java
String s1 = "Java";
String s2 = "Java";
System.out.println(s1 == s2);   // true (같은 객체)
```
리터럴은 String Pool에서 **같은 객체를 공유**한다고 배웠다. 그럼 s1을 수정하면 s2도 같이 바뀌는 사고가 나지 않을까? 그래서 실무에서는 안전하게 매번 `new String()`을 써야 하는 것 아닐까?

### 처음 생각 (오답)
```java
String s1 = "Java";
String s2 = s1;
s1 = s1 + "!";
```
같은 객체를 공유하고 있으니 s1과 s2가 **둘 다** `Java!`가 될 거라고 답했다.

### 원리: 객체(풍선)와 참조 변수(손잡이)를 나눠 본다
String은 **불변(Immutable)** 이다. 한 번 만든 객체의 내용은 바꿀 수 없다. 바꾸는 것처럼 보이는 연산은 **새 객체를 만든다.**

```
① String s1 = "Java";  String s2 = s1;

   s1 ──┐
        ├──▶ ("Java")          ← 객체 1개를 공유
   s2 ──┘

② s1 = s1 + "!";

   s1 ─────▶ ("Java!")         ← 새 객체, s1의 화살표만 이동
   s2 ─────▶ ("Java")          ← 원래 객체는 그대로
```

```java
String s1 = "Java";
String s2 = s1;
s1 = s1 + "!";
System.out.println(s1);   // Java!
System.out.println(s2);   // Java
```

### 반환값을 대입하지 않으면?
```java
String s3 = "Hi";
s3.concat("!");           // "Hi!" 새 객체는 만들어지지만 아무도 안 가리킴
System.out.println(s3);   // Hi
s3 = s3.concat("!");      // 대입해야 화살표가 옮겨감
System.out.println(s3);   // Hi!
```

### 깨달음: 인과관계가 반대였다
"공유하니까 위험하다"가 아니라, **불변이기 때문에 안심하고 공유할 수 있다.** 아무도 객체 내용을 바꿀 수 없으니, 같은 문자열을 여러 변수가 함께 가리켜도 서로 영향을 주지 않는다. 그래서 리터럴을 Pool에서 공유해 메모리를 아낄 수 있다.

```java
String a = "Java";
String c = new String("Java");
System.out.println(a == c);        // false  new는 항상 새 객체 (Pool 공유 X)
System.out.println(a.equals(c));   // true   내용 비교
```
→ `new String()`을 쓸 이유는 오히려 없다. 문자열 비교는 `==`가 아니라 `equals()`로 한다.

> 7주차의 "캐스팅은 객체를 안 바꾸고 변수만 바꾼다"와 같은 그림이다. 이번엔 **새 객체가 생기고 화살표가 옮겨 가는** 경우다.

---

## 2. equals는 왜 `Donut`이 아니라 `Object`로 받을까?

### 의문
```java
@Override
public boolean equals(Object obj) {
    Donut other = (Donut) obj;
    return this.name.equals(other.name);
}
```
Donut끼리 비교하는데 왜 매개변수가 `Object obj`일까? 그리고 왜 안에서 굳이 `(Donut)`으로 형 변환을 할까?

### 원리 1: 오버라이딩 규칙 때문에 Object로 받아야 한다
`equals`는 **Object 클래스의 메서드**다. Object는 모든 클래스의 부모라서, 세상의 모든 객체를 받을 수 있게 매개변수가 `Object`로 열려 있다. 오버라이딩은 **부모 메서드와 이름·매개변수가 같아야** 하므로 자식도 `equals(Object obj)`로 써야 한다.

```java
public boolean equals(Donut obj) { ... }   // 매개변수가 다름 → 오버라이딩이 아니라 오버로딩
```

### 원리 2: 들어올 때 업캐스팅, 쓰려면 다운캐스팅
```java
d1.equals(d2);
// 메서드 안에서 일어나는 일: Object obj = d2;   ← 업캐스팅
```
```
obj [Object]  ──▶ ( Donut 객체 : name = "초코" )
   허락: equals, toString, getClass ...   (Object가 가진 것만)
   obj.name  →  컴파일 에러 (Object에 name 없음)

other [Donut] ──▶ ( 같은 Donut 객체 )
   허락: name, ...
   other.name  →  OK
```
7주차에서 정리한 "변수 타입이 **허락**, 객체가 **실행**" 그대로다. `obj`의 변수 타입이 Object라서 `name`을 허락받지 못한다. 그래서 `(Donut) obj`로 다운캐스팅해서 **Donut 리모컨**으로 바꿔 쥐어야 한다.

### 안전하게 쓰기
```java
@Override
public boolean equals(Object obj) {
    if (obj instanceof Donut) {          // Donut이 아닌 게 들어오면 ClassCastException 방지
        Donut other = (Donut) obj;
        return this.name.equals(other.name);
    }
    return false;
}
```

### 결과 비교
```java
Donut d1 = new Donut("초코");
Donut d2 = new Donut("초코");
```
| | 오버라이딩 전 | 오버라이딩 후 |
|---|---|---|
| `d1 == d2` | false (다른 객체) | false (다른 객체) |
| `d1.equals(d2)` | false (Object의 equals = 주소 비교) | **true** (name 비교) |

### 깨달음
equals 오버라이딩은 **다형성(업캐스팅)과 다운캐스팅을 실제로 쓰는 대표 예**였다. 6~7주차에 배운 캐스팅이 왜 필요한지 여기서 처음 와닿았다.

---

## 3. 모듈은 이클립스 어디에 "있는" 걸까?

### 의문
프로젝트, 패키지, 클래스는 패키지 탐색기에서 폴더나 파일로 보이는데, 모듈은 개념만 있고 실체가 어디 있는지 몰랐다.

### 처음 생각 (오답)
- 크기 순서를 작은 것부터 쓰라는 질문에 **프로젝트 → 모듈 → 패키지 → 클래스**로 거꾸로 썼다.
- 패키지를 밖으로 공개하는 키워드 `exports`를 떠올리지 못했다.

### 원리
```
클래스 < 패키지 < 모듈 (= 이클립스 프로젝트 1개)

MyLib (프로젝트 = 모듈)
 └ src
    ├ module-info.java        ← 모듈의 "실체": 경계와 공개 범위를 적은 파일
    └ com.example.lib.util    ← 패키지
       └ Calculator.java      ← 클래스
```
이클립스는 **1 프로젝트 = 1 모듈**이라 모듈 폴더가 따로 생기지 않는다. 대신 `src` 바로 아래의 **`module-info.java` 파일 하나**가 모듈의 경계를 정한다.

### 두 프로젝트로 직접 실습하며 확인한 4단계 권한
```java
// [제공자] MyLib/src/module-info.java
module com.example.lib {
    exports com.example.lib.util;        // ① 이 패키지를 밖에 공개
}

// [제공자] Calculator.java
package com.example.lib.util;
public class Calculator {                // ② 클래스와 메서드가 public
    public static int add(int a, int b) { return a + b; }
}

// [사용자] MyApp/src/module-info.java
module com.example.app {
    requires com.example.lib;            // ③ 이 모듈이 필요하다 (+ Build Path의 Modulepath에 MyLib 추가)
}

// [사용자] Main.java
package com.example.app;
import com.example.lib.util.Calculator;  // ④ import
public class Main {
    public static void main(String[] args) {
        System.out.println(Calculator.add(3, 5));   // 8
    }
}
```
```
 ① exports ──▶ ② public ──▶ ③ requires + Build Path ──▶ ④ import
 (모듈 문 열기)  (클래스 문 열기)  (상대 모듈 연결)          (이름 가져오기)
```
네 개가 **전부** 맞물려야 쓸 수 있다. 실습에서 ①의 `exports`를 지우니 Main의 **`import` 줄부터** 컴파일 에러가 났다. 패키지가 모듈 밖으로 공개되지 않았으니, 클래스가 public이어도 바깥에서는 그 패키지 자체를 볼 수 없기 때문이다.

---

## 4. String 메서드에서 틀린 것

### `replace`
- **처음 생각 (오답)**: `"Java is fun".replace("a", "o")`에서 특정 `a` 하나만 바뀐다고 보고 `Javo is fun`이라고 썼다.
- **원리**: 일치하는 것을 **전부** 바꾼다.
```java
System.out.println("Java is fun".replace("a", "o"));   // Jovo is fun
```

### `substring(시작, 끝)`
- **처음 생각 (오답)**: `substring(0, 4)`가 0~3번을 **지우고** 나머지 `is fun`을 남긴다고 봤다.
- **원리**: 시작부터 끝 **직전까지를 꺼낸다(추출)**. 끝 번호는 포함하지 않는다.
```
 J  a  v  a  _  i  s  _  f  u  n
 0  1  2  3  4  5  6  7  8  9  10
[0 ─────── 4)   → "Java"
```
```java
String s = "Java is fun";
System.out.println(s.substring(0, 4));   // Java
System.out.println(s.substring(8));      // fun
System.out.println(s);                   // Java is fun (불변이라 원본 그대로)
```

### `getClass().getName()`
- **처음 생각 (오답)**: `equals()`처럼 무언가를 비교하는 메서드로 헷갈렸다.
- **원리**: 비교가 아니라, 변수 타입과 상관없이 **실제 객체가 어떤 클래스로 만들어졌는지** 이름을 돌려준다.
```java
Object o = new Donut("초코");
System.out.println(o.getClass().getName());   // Donut (변수 타입 Object가 아니라 실제 객체)
```

---

## 정리

| 의문 / 착각 | 바로잡은 규칙 |
|---|---|
| Pool 공유 = 수정 충돌 위험 | **불변이라서** 안전하게 공유 가능 |
| `s1 = s1 + "!"`면 s2도 바뀜 | 새 객체 생성, **s1 화살표만 이동** |
| equals를 Donut으로 받으면 되지 않나 | 오버라이딩은 부모와 같은 **`Object` 매개변수** |
| 왜 `(Donut) obj`? | Object 변수 타입은 `name`을 **허락 안 함** → 다운캐스팅 |
| 모듈의 실체? | `src`의 **module-info.java** (1 프로젝트 = 1 모듈) |
| 크기 순서 거꾸로 | 클래스 < 패키지 < 모듈 |
| replace는 하나만 | **전부** 치환 |
| substring은 지우기 | 끝 직전까지 **추출** |
| getClass = 비교 | **실제 객체의 클래스 이름** |

---

### 기능사 실기 모의고사 1회에서 틀린 것 (2026-11-13): `==`와 `equals`를 반대로
```java
String a = "ab";
String b = "a";
String c = b + "b";
System.out.println((a == c) + " " + a.equals(c));
```
내 답: `true false` (정답: `false true`)

판단 질문은 하나: **"새 객체가 만들어졌나?"** `b + "b"`는 변수가 섞인 `+`라 실행 중 새 객체 → `==` false, 내용은 같으니 `equals` true. 2회(`new String`, `"ja" + "va"`)에서는 맞혔다.
