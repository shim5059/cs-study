# 3주차 · 배열 심화

> 헷갈렸던 부분과 해결 과정: [week03-deep-dive.md](week03-deep-dive.md)

> 교재 3장 · 이 주차는 수업 메모가 없어서, 중간고사 복습 때 정리한 3장 배열 내용으로 채움

## 1. 배열 기본 규칙
```java
int[] arr = new int[3];   // [ ] 안의 3 = 칸의 "개수"
```
- 번호(인덱스)는 `0` ~ `length - 1`
- 없는 칸 접근 → **실행 중** `ArrayIndexOutOfBoundsException`

```java
int[] a = {10, 20, 30};
a[3] = 1;   // 컴파일은 통과, 실행하면 예외
```

### 기본값 (`new`로 만들고 값을 안 넣었을 때)

| 타입 | 기본값 |
|---|---|
| `int`, `long` 등 정수 | `0` |
| `double` | `0.0` |
| `boolean` | `false` |
| `char` | `'\u0000'` (빈 문자) |
| `String` 등 객체 | `null` |

### 길이 표기 정리

| 대상 | 길이 |
|---|---|
| 배열 | `a.length` (괄호 **없음**, 필드) |
| String | `s.length()` (괄호 **있음**, 메서드) |
| ArrayList | `list.size()` |

## 2. for-each문
```java
for (int x : a) {
    x = x * 2;   // x는 칸의 "복사본" → 배열은 안 바뀜
}
```
- 배열 값을 **읽을 때** 사용. 값을 바꾸려면 일반 `for`와 인덱스를 써야 함

## 3. Arrays 클래스 (`import java.util.Arrays;`)

| 메서드 | 기능 | 주의 |
|---|---|---|
| `Arrays.toString(a)` | 배열을 문자열로 | |
| `Arrays.sort(a)` | 오름차순 정렬 | 반환값 없음 (원본이 바뀜) |
| `Arrays.fill(a, 7)` | 모든 칸을 7로 | 반환값 없음 |
| `Arrays.copyOf(a, n)` | 새 배열로 복사 | 두 번째 값 `n`은 **새 배열의 길이** |

## 4. 배열 뒤집기
```java
for (int i = 0; i < a.length / 2; i++) {
    int tmp = a[i];
    a[i] = a[a.length - 1 - i];
    a[a.length - 1 - i] = tmp;
}
```
- 반대편 인덱스는 `length - 1 - i`, 반복은 `length / 2`번

## 5. 2차원 배열
```java
int[][] m = {
    {1, 2, 3},
    {4, 5, 6}
};
System.out.println(m.length);      // 2 (행 수)
System.out.println(m[0].length);   // 3 (0번 행의 열 수)

for (int i = 0; i < m.length; i++) {
    for (int j = 0; j < m[i].length; j++) {
        System.out.print(m[i][j] + " ");
    }
    System.out.println();
}
```

### 가변 배열: 행마다 칸 수가 다를 때 (기능사 실기 대비)
```java
int[][] r = {
    {1, 2, 3, 4},     // r[0]  칸 4개
    {5},              // r[1]  칸 1개
    {6, 7}            // r[2]  칸 2개
};                    // 행 3개
```

| 표현 | 값 | 뜻 |
|---|---|---|
| `r.length` | 3 | **행 수** (r의 원소 = 행의 개수) |
| `r[0].length` | 4 | 0번 행의 칸 수 |
| `r[2][1]` | 7 | 2번 행의 1번 칸 |

- `.length`는 언제나 **점 바로 앞 배열의 원소 개수**
- 행 수와 0번 행 칸 수는 **다를 수 있다** → `r.length`를 `r[0].length`로 착각하면 안 됨

```java
int[][] r2 = {{1, 2, 3}, {4, 5}, {6, 7, 8, 9, 0}, {10}};
int cnt = 0;
for (int i = 0; i < r2.length; i++) {
    cnt += r2[i].length;                  // 행마다 칸 수 더하기
}
System.out.println(r2.length + " " + r2[2].length + " " + cnt + " " + r2[3][0]);
// 4 5 11 10
```

## 6. 배열 대입과 복사

| 코드 | 결과 |
|---|---|
| `int[] b = a;` | **주소 복사**: a, b가 같은 배열을 가리킴 |
| `int[] c = a.clone();` | 새 배열 (1차원이면 값이 따로) |
| `int[][] d = m.clone();` | **얕은 복사**: 바깥 배열만 새로 만들고 각 행은 **공유** |

- `=`는 "붙이기"가 아니라 **갈아끼우기**
  - `a[0] = 5;` → 배열의 **내용** 교체
  - `a = b;` → 변수가 가리키는 **배열 자체**를 교체
