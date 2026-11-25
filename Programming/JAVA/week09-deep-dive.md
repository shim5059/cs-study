# 9주차 Deep Dive · 제네릭 타입 라벨, LinkedList, String 불변, Math 반환 타입

> 개념 요약: [week09.md](week09.md)
>
> **의문 → 처음 생각 → 원리 → 깨달음** 순서의 기록. 8주차에 정리한 "String은 불변이라 새 객체가 생기고 화살표만 옮겨 간다"가 이번에도 그대로 나왔다.

---

## 1. `String y = a.getItem();`은 `a`의 타입을 바꿔주는 걸까?

### 의문
```java
Box<Integer> a = new Box<>(10);        // ①
Integer x = a.getItem();               // ②
String y = a.getItem();                // ③  ← 컴파일 에러가 나는 줄
Box<String> c = new Box<>("A");        // ④
```
③이 에러라는 건 맞혔는데, 이유를 "③번 줄은 객체 `a`에 들어 있는 자료형을 `String` 타입으로 바꿔주는 건가?"라고 생각했다.

### 처음 생각 (오답)
③이 `a` 안의 자료형을 `String`으로 바꿔 버린다고 봤다.

### 원리: `y`는 새 변수이고 `a`는 그대로다
| 줄 | 읽는 법 |
|---|---|
| ① | `T` = `Integer`. 상자 `a`는 숫자 전용이고 이 라벨은 변하지 않는다 |
| ② | `getItem()`이 `Integer`를 돌려주고 `Integer` 변수가 받는다 → 타입이 같아서 OK |
| ③ | `y`는 **새로 만드는 `String` 변수**다. `a`는 건드리지 않는다. 돌려받는 `Integer`를 `String` 칸에 담으려 해서 에러 |
| ④ | `c`는 `String` 라벨로 따로 만든 새 상자. `a`와 상관없다 |

```
Integer 접시 x ◀── getItem() 의 결과(Integer)   OK
String  접시 y ◀── getItem() 의 결과(Integer)   ✗ 타입이 다름
```
컴파일러는 값(`10`)을 실행하지 않고 **왼쪽 타입과 오른쪽 타입이 맞는지**만 검사한다. 12주차 전의 "컴파일은 규칙만 검사한다"와 같은 원리다.

```java
String y = String.valueOf(a.getItem());   // Integer 값을 문자열로 바꿔서 담음 → OK
```

### 깨달음
`String y = ...`는 **`a`를 바꾸는 코드가 아니라 `y`를 새로 만드는 코드**다. 오른쪽에서 나온 값의 타입과 왼쪽 변수의 타입이 맞아야 한다. `a`는 끝까지 `Box<Integer>`다.

---

## 2. 끼워 넣기만 LinkedList가 유리할까?

### 의문
`ArrayList`와 `LinkedList` 중 "맨 앞에 값을 계속 끼워 넣기"가 `LinkedList`에 유리하다는 건 맞혔다. 그런데 **끼워 넣기만** 유리한 건가?

### 원리
```
ArrayList (칸이 붙어 있음)       LinkedList (노드가 화살표로 이어짐)
[초코][딸기][크림]               [초코]→[딸기]→[크림]→끝
맨 앞에 끼우면 전부 한 칸씩 밀림   맨 앞에 끼우면 화살표만 바꿈
```
- 끼우기뿐 아니라 **지우기**도 유리하다. 정확히는 "앞이나 중간에서 넣고 빼는 작업"
- 단, "5000번째에 끼우기"는 그 자리까지 **걸어가는 비용**이 든다. 위치가 이미 정해진 맨 앞 같은 경우가 가장 확실하다
- 맨 뒤 추가는 `ArrayList`도 빨라서 차이가 작다

| 상황 | 선택 |
|---|---|
| 번호로 읽는 일이 많다 | `ArrayList` |
| 앞이나 중간에서 넣고 빼는 일이 많다 | `LinkedList` |

### 깨달음
속도 차이는 "메서드가 다르다"가 아니라 **속 구조가 다르다**에서 나온다. 11일에 본 "끼우면 밀리고 지우면 당겨진다"가 `ArrayList` 속에서 실제로 일어나는 일이었고, `LinkedList`는 칸이 붙어 있지 않아서 밀 필요가 없다. 현업에서는 `ArrayList`를 기본으로 쓰는 경우가 훨씬 많다.

---

## 3. `s.concat("!")` 결과를 받지 않으면?

### 의문
```java
String s = "Hi";
s.concat("!");

StringBuilder t = new StringBuilder("Hi");
t.append("!");

System.out.println(s + " " + t);
```

### 처음 생각 (오답)
내 답: `Hi! Hi!` (정답: `Hi Hi!`)

`s.concat("!")`을 하면 `s`도 `Hi!`가 된다고 본 듯하다.

### 원리
`String`은 **불변**이다. `concat`은 `s`를 바꾸지 않고 "뒤에 붙인 **새 문자열**"을 만들어 돌려줄 뿐이고, 받는 변수가 없으면 그 새 문자열은 사라진다.

| 변수 | 조작 | 결과 |
|---|---|---|
| `s` (`String`) | `s.concat("!")` | 새 문자열이 만들어질 뿐 `s`는 `"Hi"` 그대로 |
| `t` (`StringBuilder`) | `t.append("!")` | 객체 자체가 바뀌어 `"Hi!"` |

```java
s = s.concat("!");   // 새 문자열을 s에 다시 담아야 s가 "Hi!"가 됨 → 출력 Hi! Hi!
```

### 깨달음
`String` 메서드는 전부 **"새 걸 돌려줄 뿐 원본은 그대로"**다. 8주차 deep-dive §1(`s3.concat("!")` → `Hi`)에서 정리했던 것과 똑같은 함정을 `StringBuilder`와 나란히 놓으니 차이가 더 선명해졌다. 바뀌는 쪽(`StringBuilder`)과 새로 돌려주는 쪽(`String`)을 구분해서 읽는다.

---

## 4. `Math.pow(2, 3)`의 출력은 `8`일까 `8.0`일까?

### 의문
```java
System.out.println(Math.pow(2, 3));
System.out.println(Math.round(2.5));
System.out.println(Math.max(3, 8));
```

### 처음 생각 (오답)
내 답: `8` / `3` / `8` (정답: `8.0` / `3` / `8`)

둘째 줄(`round`)과 셋째 줄(`max`)은 맞혔고, `pow`에 정수를 넣었으니 정수가 나올 거라고 본 듯하다.

### 원리
출력 모양은 **넣은 값이 아니라 메서드의 반환 타입**이 정한다.

| 메서드 | 반환 타입 | 이유 |
|---|---|---|
| `Math.pow`, `Math.sqrt` | 항상 `double` | 제곱·제곱근은 정수가 안 나올 수 있어서 |
| `Math.max`, `Math.min`, `Math.abs` | 넣은 타입 그대로 | `int`를 넣으면 `int` |
| `Math.round` | 정수 | 소수점 없이 나옴 |
| `Math.floor`, `Math.ceil` | `double` | 정수 값이어도 `3.0`처럼 나옴 |

```java
System.out.println(Math.sqrt(16));                  // 4.0
System.out.println((int) Math.sqrt(10));            // 3  (3.16…에서 (int)가 소수점을 버림)
System.out.println(Math.abs(-7) + Math.max(2, 5));  // 12 (둘 다 int)
```

### 깨달음
중간고사에서 틀렸던 "double 출력 3.0"과 같은 유형이 다시 나왔다. 출력을 쓰기 전에 **줄마다 "돌려주는 타입이 `double`인가 `int`인가"를 먼저 적으면** 틀리지 않았다. `pow`·`sqrt`는 이름이 "제곱·제곱근"이라 소수가 나올 수 있어서 `double`이고, `max`·`min`·`abs`는 넣은 타입을 따라간다.

---

## 정리

| 의문 / 착각 | 바로잡은 규칙 |
|---|---|
| `String y = a.getItem();`가 `a`의 타입을 바꿈 | `y`는 **새 변수**. `a`는 그대로 `Box<Integer>` |
| `<>` 안에는 `"초코"` 같은 값이 들어감 | `<>` 안은 **타입** (`String`), 값은 생성자 괄호 안 |
| `Box<String> b2 = b;`는 상자 복사 | 같은 상자를 가리키는 **리모컨이 하나 더** |
| 끼워 넣기만 LinkedList가 유리 | **앞이나 중간에서 넣고 빼기** (찾아가는 비용은 별도) |
| `s.concat("!")`면 `s`도 바뀜 | **새 문자열을 돌려줄 뿐**, 다시 담아야 바뀜 |
| `Math.pow(2, 3)` → `8` | 반환 타입이 `double`이라 **`8.0`** |
| `delete(시작, 끝)`의 끝도 지움 | 끝 번호는 **포함하지 않음** (`substring`과 같은 규칙) |
