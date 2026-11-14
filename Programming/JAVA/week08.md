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

#### `+`로 만든 문자열 (복습 추가)
```java
String a = "hi";
String d = "h";
String e = d + "i";        // 변수가 섞인 + → 실행 중 새 객체
String f = "h" + "i";      // 리터럴끼리 + → 컴파일 때 "hi"로 합쳐짐 → 풀 재사용
System.out.println(a == e);        // false
System.out.println(a == f);        // true
System.out.println(a.equals(e));   // true
```

| 만드는 방법 | 위치 | `"hi"` 리터럴과 `==` |
|---|---|---|
| `"hi"` | 스트링 풀 | true |
| `"h" + "i"` | 컴파일 때 합쳐져 풀 | true |
| `d + "i"` | 실행 중 힙에 새 객체 | **false** |
| `new String("hi")` | 힙에 새 객체 | **false** |

- 예: `new String("ASDF") == new String("ASDF")` → false → `ASDFASDF` 출력
- 수정 가능한 문자열: `StringBuilder`, `StringBuffer`(동기화 지원)

### 주요 메서드 (`s = "Java is fun"`)

| 메서드 | 결과 | 포인트 |
|---|---|---|
| `s.length()` | 11 | 공백 포함 |
| `s.charAt(5)` | `i` | 0번부터 |
| `s.indexOf("a")` | 1 | 없으면 -1 |
| `s.lastIndexOf("a")` | 3 | 뒤에서부터 찾은 위치 |
| `s.contains("fun")` | true | 포함 여부 |
| `"ABC".equalsIgnoreCase("abc")` | true | 대소문자 무시 비교 |
| `s.replace("a", "o")` | `Jovo is fun` | 해당 문자 **전부** 바꿈 |
| `"ABC!@#def*&^123".replaceAll("[^a-zA-Z0-9]", "*")` | `ABC***def***123` | **정규식**에 맞는 글자를 전부 바꿈 |
| `s.substring(8)` | `fun` | 8번부터 끝까지 |
| `s.substring(0, 4)` | `Java` | 0 ~ **3**번 추출 (끝 번호 **미포함**) |
| `s.toUpperCase()` | `JAVA IS FUN` | |
| `"  Java  ".trim()` | `Java` | 양 끝 공백 제거 |
| `"사과,배,포도".split(",")[1]` | `배` | 배열로 쪼갬 |
| `String.join("-", "2026", "11", "04")` | `2026-11-04` | |
| `String.valueOf(100) + 1` | `1001` | 문자열 연결 |
| `"Java".compareTo("Kotlin")` | -1 | 사전 순 비교 (같으면 0) |

**정규식 `[ ]`과 `[^ ]`** (복습 추가)

| 표기 | 뜻 |
|---|---|
| `[a-zA-Z0-9]` | 괄호 안의 글자 중 하나 (영문·숫자) |
| `[^a-zA-Z0-9]` | 괄호 안 맨 앞의 `^` = 괄호 안의 것이 **아닌** 글자 |
| `ㄱ-ㅎ` `ㅏ-ㅣ` `가-힣` | 한글 자음, 모음, 완성형 한글 |

- `replaceAll("[^ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9,.]", "*")` = 한글·영문·숫자·쉼표·마침표가 **아닌** 글자(특수문자)만 `*`로. 원래 있던 `*`도 한 칸으로 바뀐다
- `^`를 빼면 정반대(영문·숫자를 가림)가 된다. 실행해 보면 `***!@#****&^***`

**대소문자 철자 규칙**: 클래스는 대문자로 시작(`String`, `System`, `Integer`, `Math`), 메서드는 소문자로 시작하고 이어지는 단어 첫 글자만 대문자(`toUpperCase`, `equalsIgnoreCase`, `indexOf`, `charAt`, `parseInt`). `substring`은 한 단어, `println`은 print + ln(소문자 L)

## 5. 자주 쓰는 라이브러리 (복습 추가)

> 다 외울 필요는 없고 **이름을 보고 뜻이 떠오르면** 충분하다. 모두 직접 실행해 확인

### 패키지와 import
| 패키지 | 들어 있는 것 | import |
|---|---|---|
| `java.lang` | `String`, `Math`, `System`, `Integer`, `Object` | **자동** |
| `java.util` | `ArrayList`, `HashMap`, `Scanner`, `Random`, `Arrays` | 필요 |
| `java.io` / `java.net` | 입출력 / 네트워크 | 필요 |

```java
import java.util.ArrayList;   // 클래스 하나만
import java.util.*;           // 패키지 전체
```

### Math
| 메서드 | 무엇을 하나 | 결과 |
|---|---|---|
| `Math.abs(-3)` | 절댓값 | `3` |
| `Math.max(3, 7)` / `Math.min(3, 7)` | 큰 값 / 작은 값 | `7` / `3` |
| `Math.pow(2, 3)` | 거듭제곱 | `8.0` (**double**) |
| `Math.sqrt(16)` | 제곱근 | `4.0` (**double**) |
| `Math.ceil(2.1)` / `Math.floor(2.9)` | 올림 / 내림 | `3.0` / `2.0` (**double**) |
| `Math.ceil(-2.1)` / `Math.floor(-2.1)` | 수직선 위 / 아래 | `-2.0` / `-3.0` |
| `Math.round(2.5)` / `Math.round(-2.5)` | 반올림 (0.5 더해 내림) | `3` / `-2` (**정수**) |
| `(int)(Math.random() * 6) + 1` | 0.0 이상 1.0 미만 난수 → 1~6 | |

### ArrayList (Python 리스트와 비교)
```java
ArrayList<Integer> list = new ArrayList<>();
list.add(5);              // [5]               append
list.add(8);              // [5, 8]
list.add(0, 3);           // [3, 5, 8]         insert(0, 3)
list.remove(1);           // [3, 8]            pop(1): int는 "위치"
list.remove(Integer.valueOf(8));   // [3]      remove(8): 값으로 지우려면 감싸기
list.get(0);              // 3                 a[0]
list.set(0, 9);           // [9]               a[0] = 9
list.size();              // 1                 len(a)
list.contains(9);         // true              9 in a
```

### HashMap (Python 딕셔너리와 비교)
```java
HashMap<String, Integer> map = new HashMap<>();
map.put("a", 1);
map.put("a", 5);               // 같은 키 → 덮어쓰기
map.get("a");                  // 5
map.get("z");                  // null (Python d['z']는 에러)
map.getOrDefault("z", 0);      // 0    (d.get('z', 0))
map.containsKey("a");          // true ('a' in d)
map.size();                    // 1
map.remove("a");
```

### 기타
| 코드 | 결과 |
|---|---|
| `new Random().nextInt(10)` | 0 이상 10 **미만** 정수 |
| `Arrays.sort(arr)` / `Arrays.toString(arr)` | 배열 정렬 (void) / `[2, 5, 9]` 문자열 |
| `Integer.parseInt("42") + 1` | `43` |
| `Character.isDigit('7')` / `Character.toUpperCase('a')` | `true` / `A` |
