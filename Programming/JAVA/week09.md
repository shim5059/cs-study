# 9주차 · 제네릭, ArrayList·LinkedList, StringBuilder, Math

> 헷갈렸던 부분과 해결 과정: [week09-deep-dive.md](week09-deep-dive.md)

> 교재 7~8장 · 수업 뒤에 복습하며 정리한 내용. `Math`의 메서드 표와 `ArrayList` 기본 사용법은 [8주차 §5](week08.md)에 있어서 여기서는 **반환 타입**과 **끼우기·지우기**에 집중했다. 모든 코드는 직접 실행해서 결과를 확인했다

## 1. 제네릭 `Box<T>`
- **제네릭**: 클래스 안에서 쓸 타입을 미리 정하지 않고 **사용할 때 정하는** 문법 (C++의 템플릿과 비슷)
- **`T`**: 타입이 들어갈 빈자리 이름표 (관례로 Type의 T)
- **`<>` 안에는 값이 아니라 타입**이 들어간다

```java
class Box<T> {
    private T item;

    public Box(T item) { this.item = item; }
    public T getItem() { return item; }
    public void setItem(T item) { this.item = item; }
}

Box<String> b = new Box<>("초코");    // T = String
String s = b.getItem();               // 꺼낼 때 형 변환 없이 String으로 받음
```

| 규칙 | 설명 |
|---|---|
| `<>` 안은 타입 | `Box<String>`의 `T`는 `String`이고, `"초코"`는 값이다 |
| 꺼낸 값은 라벨 타입 | `Box<Integer>`에서 꺼낸 값을 `String` 변수에 바로 담으면 **컴파일 에러** |
| 대입은 상자를 복사하지 않음 | `Box<String> b2 = b;`는 같은 상자를 가리키는 리모컨이 하나 더 생긴 것 |

```java
Box<Integer> a = new Box<>(10);
Integer x = a.getItem();      // OK (Integer → Integer)
String y = a.getItem();       // 컴파일 에러: incompatible types: Integer cannot be converted to String
String z = String.valueOf(a.getItem());   // 문자열로 바꿔서 담으면 OK
```

```java
Box<String> b = new Box<>("초코");
b.setItem("딸기");
System.out.println(b.getItem());   // 딸기

Box<String> b2 = b;                // 같은 상자
b2.setItem("크림");
System.out.println(b.getItem());   // 크림 (b로 봐도 바뀌어 있음)
```

## 2. ArrayList
- 속에서 **배열**을 쓰는 리스트, 번호는 0번부터, 크기가 자동으로 늘고 줄어든다
- `ArrayList<String>`의 `<String>`이 위의 제네릭이다 (`ArrayList`도 제네릭 클래스)
- **끼우면 뒤가 한 칸씩 밀리고, 지우면 뒤가 한 칸씩 당겨진다**

```java
import java.util.ArrayList;

public class Arraylist {
    public static void main(String[] args) {
        ArrayList<String> al = new ArrayList<>();

        al.add("초코 도넛");          // [초코]
        al.add("딸기 도넛");          // [초코, 딸기]
        al.add("크림 도넛");          // [초코, 딸기, 크림]
        al.add(1, "기본 도넛");       // 1번에 끼움(덮어쓰기 아님) → [초코, 기본, 딸기, 크림]

        System.out.println("총 주문 수: " + al.size());     // 4
        for (int i = 0; i < al.size(); i++) {
            System.out.println(i + "번 위치: " + al.get(i));
        }

        al.remove("딸기 도넛");        // 값으로 삭제 → [초코, 기본, 크림]
        al.remove(0);                  // 지금 0번(초코) 삭제 → [기본, 크림]

        System.out.println("\n도넛 삭제 후 주문 목록:");
        for (String order : al) {      // for-each: 번호 없이 처음부터 하나씩
            System.out.println(order);
        }
    }
}
```
```
총 주문 수: 4
0번 위치: 초코 도넛
1번 위치: 기본 도넛
2번 위치: 딸기 도넛
3번 위치: 크림 도넛

도넛 삭제 후 주문 목록:
기본 도넛
크림 도넛
```
- `remove(0)`은 "처음 만든 것"이 아니라 **그 시점의 0번**을 지운다. 앞에서 지운 만큼 번호가 당겨져 있다

## 3. LinkedList
- **노드**(값 + 다음 노드를 가리키는 연결)를 줄줄이 이은 리스트
- 사용법(`add`, `get`, `remove`, `size`)은 `ArrayList`와 같고 만들 때 이름만 바뀐다

```java
LinkedList<String> list = new LinkedList<>();
```

| 작업 | `ArrayList` | `LinkedList` | 이유 |
|---|---|---|---|
| 번호로 읽기 `get(i)` | 빠름 | 느림 | 배열은 번호로 점프, 연결 구조는 처음부터 따라감 |
| 앞이나 중간에서 끼우기·지우기 | 느림 | 빠름 | 배열은 뒤 칸을 전부 밀고 당김, 연결 구조는 화살표만 바꿈 |
| `size()` | 같음 | 같음 | 둘 다 개수를 저장해 둠 |

- 맨 뒤에 추가하는 건 `ArrayList`도 빨라서 차이가 크지 않다
- 중간 삽입은 **그 자리까지 찾아가는 비용**이 따로 든다. 위치가 이미 정해진 맨 앞 같은 경우가 가장 확실한 이점이다
- 현업에서는 `LinkedList`가 이기는 상황이 좁아서 `ArrayList`를 기본으로 쓰는 경우가 훨씬 많다

```java
LinkedList<String> list = new LinkedList<>();
list.add("A");          // [A]
list.add("B");          // [A, B]
list.add("C");          // [A, B, C]
list.add(1, "X");       // [A, X, B, C]
list.remove("B");       // [A, X, C]
list.remove(0);         // [X, C]
System.out.println(list.size() + " " + list.get(0));   // 2 X
```

## 4. StringBuilder
- `String`은 **불변**이라 메서드 결과를 다시 받아야 바뀌고, `StringBuilder`는 **그 객체 자체가 바뀐다**
- 반복문에서 문자열을 계속 이어 붙일 때 `String`은 매번 새 문자열을 만들어서 비효율적이라 `StringBuilder`를 쓴다

| | `String` | `StringBuilder` |
|---|---|---|
| `s.concat("!")` / `sb.append("!")` | 새 문자열을 **돌려줌**. 원본 그대로 | 객체 자체가 바뀜 |
| 바꾸려면 | `s = s.concat("!");` 다시 담기 | 그냥 호출 |

| 메서드 | 하는 일 |
|---|---|
| `append(값)` | 뒤에 붙이기 |
| `insert(번호, 값)` | 그 번호 자리에 끼우기 |
| `delete(시작, 끝)` | 시작부터 끝 **직전까지** 지우기 (끝 번호 미포함, `substring`과 같은 규칙) |
| `reverse()` | 거꾸로 뒤집기 |
| `toString()` | `String`으로 바꾸기 |

```java
StringBuilder sb = new StringBuilder("Hello");
sb.append(" Java");     // Hello Java
sb.insert(5, ",");      // Hello, Java
sb.delete(0, 7);        // 0~6번 삭제 → Java
sb.reverse();           // avaJ
```
```java
String s = "Hi";
s.concat("!");              // 받는 곳이 없어서 버려짐
System.out.println(s);      // Hi
s = s.concat("!");          // 다시 담아야 바뀜
System.out.println(s);      // Hi!
```

## 5. Math 반환 타입 (복습)
- `Math`는 `static` 메서드 모음이라 `new` 없이 `Math.메서드()`로 쓴다 (`java.lang`이라 import 불필요)
- 출력이 `8`인지 `8.0`인지는 **반환 타입**으로 정해진다

| 메서드 | 반환 타입 | 예 |
|---|---|---|
| `Math.pow(2, 3)` | **항상 `double`** | `8.0` |
| `Math.sqrt(16)` | **항상 `double`** | `4.0` |
| `Math.floor(3.7)` / `Math.ceil(3.2)` | `double` | `3.0` / `4.0` |
| `Math.round(2.5)` | 정수 | `3` |
| `Math.max(3, 8)`, `Math.min`, `Math.abs(-7)` | **넣은 타입 그대로** | `8`, `7` |

```java
System.out.println((int) Math.sqrt(10));              // 3  (3.16…을 (int)로 소수점 버림)
System.out.println(Math.abs(-7) + Math.max(2, 5));    // 12 (7 + 5, 둘 다 int)
```
- `pow`와 `sqrt`는 정수를 넣어도 `.0`이 붙는다. `max`·`min`·`abs`는 `int`를 넣으면 `int`가 나온다
- 주사위: `(int)(Math.random() * 6) + 1` → 0.0 이상 1.0 미만에 6을 곱하면 0~5.999…, `(int)`로 0~5, 1을 더해 1~6
