# 8주차 · 자바 기본 패키지 (Object, Wrapper, String)

> 헷갈렸던 부분과 해결 과정: [week08-deep-dive.md](week08-deep-dive.md)

> 교재 9장 · 시험 강조: **Object(equals와 ==, equals 오버라이딩)**, **Wrapper 클래스**

## 1. 클래스 · 패키지 · 모듈
- 크기: **클래스 < 패키지 < 모듈** (이클립스는 1 프로젝트 = 1 모듈)
- `java.lang` 패키지(`String`, `Object`, `Math`, Wrapper 등)는 **import 없이** 사용
- `Scanner`, `ArrayList` 등 다른 패키지는 `import` 필요

### module-info.java
```java
// 내보내는 쪽
module com.example.lib {
    exports com.example.lib.util;     // 이 패키지를 외부에 공개
}

// 가져다 쓰는 쪽
module com.example.app {
    requires com.example.lib;         // 이 모듈이 필요하다
}
```
- `exports`를 지우면 외부 모듈에서 그 패키지를 못 써서 **컴파일 에러**
- 이클립스: Build Path → **Modulepath**에 상대 프로젝트 추가

## 2. Object 클래스
- 모든 클래스의 **최상위 부모** (컴파일러가 `extends Object` 자동 추가)
- 그래서 빈 클래스도 `toString()`, `equals()`, `getClass()`를 가짐

### equals()와 == (시험 1순위)

| | 비교 대상 |
|---|---|
| `==` (기본형) | 값 |
| `==` (참조형) | **주소** (같은 객체인지) |
| `Object`의 `equals()` (오버라이딩 안 함) | **주소** (`==`와 같음) |
| 오버라이딩한 `equals()` | 내가 정한 **내용(값)** |

```java
class Donut {
    String name;
    Donut(String name) { this.name = name; }

    @Override
    public boolean equals(Object obj) {
        // 매개변수가 Object라 업캐스팅되어 들어옴 → 필드를 쓰려면 다운캐스팅
        if (obj instanceof Donut) {
            Donut other = (Donut) obj;
            return this.name.equals(other.name);
        }
        return false;
    }

    @Override
    public String toString() {
        return "Donut: " + name;
    }
}

Donut d1 = new Donut("초코");
Donut d2 = new Donut("초코");
System.out.println(d1 == d2);        // false (다른 객체)
System.out.println(d1.equals(d2));   // true  (오버라이딩: 이름 비교)
System.out.println(d1);              // Donut: 초코 (toString 자동 호출)
System.out.println(d1.getClass().getName());   // Donut
```
- `println(참조변수)` → `toString()` 자동 호출
  - 오버라이딩 안 하면 `클래스이름@해시코드`
- `getClass().getName()`: 비교가 아니라 **실제 객체의 클래스 이름**을 돌려줌

## 3. Wrapper 클래스
- 기본형 값을 **객체로 포장**하는 클래스 (`int` → `Integer`, `double` → `Double` …)
- 필요한 이유: `ArrayList` 같은 컬렉션(제네릭)은 **객체만** 받음, 입력값은 문자열로 들어옴

```java
Integer n = 100;          // 오토 박싱 (int → Integer)
int m = n;                // 오토 언박싱 (Integer → int)

int a = Integer.parseInt("100");       // 문자열 → int
double b = Double.parseDouble("3.5");  // 문자열 → double
Integer c = Integer.valueOf("100");    // 문자열 → Integer 객체
String s = Integer.toString(100);      // int → 문자열

System.out.println(Integer.parseInt("100") + 1);   // 101 (숫자 덧셈)
System.out.println(Integer.toString(100) + 1);     // 1001 (문자열 연결)
```

## 4. String 클래스

### 불변(Immutable)
- 한 번 만든 String 객체의 내용은 **바꿀 수 없음**
- 바꾸는 것처럼 보이는 메서드는 **새 객체를 반환**

```java
String s1 = "Java";
String s2 = s1;
s1 = s1 + "!";        // 새 객체 "Java!"가 생기고 s1만 그쪽을 가리킴
System.out.println(s1);   // Java!
System.out.println(s2);   // Java (원래 객체 그대로)

String s3 = "Hi";
s3.concat("!");           // 반환값을 대입 안 함 → s3은 그대로
System.out.println(s3);   // Hi
```

### 스트링 풀
```java
String a = "Java";
String b = "Java";
String c = new String("Java");
System.out.println(a == b);        // true  (리터럴은 스트링 풀에서 같은 객체 공유)
System.out.println(a == c);        // false (new는 항상 새 객체)
System.out.println(a.equals(c));   // true  (String은 equals가 내용 비교로 오버라이딩됨)
```
- 수정 가능한 문자열: `StringBuilder`, `StringBuffer`(동기화 지원)

### 주요 메서드 (`s = "Java is fun"`)

| 메서드 | 결과 | 포인트 |
|---|---|---|
| `s.length()` | 11 | 공백 포함 |
| `s.charAt(5)` | `i` | 0번부터 |
| `s.indexOf("a")` | 1 | 없으면 -1 |
| `s.replace("a", "o")` | `Jovo is fun` | 해당 문자 **전부** 바꿈 |
| `s.substring(8)` | `fun` | 8번부터 끝까지 |
| `s.substring(0, 4)` | `Java` | 0 ~ **3**번 추출 (끝 번호 **미포함**) |
| `s.toUpperCase()` | `JAVA IS FUN` | |
| `"  Java  ".trim()` | `Java` | 양 끝 공백 제거 |
| `"사과,배,포도".split(",")[1]` | `배` | 배열로 쪼갬 |
| `String.join("-", "2026", "11", "04")` | `2026-11-04` | |
| `String.valueOf(100) + 1` | `1001` | 문자열 연결 |
| `"Java".compareTo("Kotlin")` | -1 | 사전 순 비교 (같으면 0) |
