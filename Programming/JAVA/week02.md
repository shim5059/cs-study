# 2주차 · 조건문, 반복문, 배열 입문

> 헷갈렸던 부분과 해결 과정: [week02-deep-dive.md](week02-deep-dive.md)

> 교재 3장

## 1. 조건문

```java
int score = 85;
if (score >= 90) {
    System.out.println("A");
} else if (score >= 80) {
    System.out.println("B");     // 출력: B
} else {
    System.out.println("C");
}
```
- `if ~ else if` 묶음은 **처음으로 참인 블록 하나만** 실행

### switch
```java
int n = 2;
switch (n) {
    case 1:
        System.out.println("one");
    case 2:
        System.out.println("two");     // 여기서 시작
    case 3:
        System.out.println("three");   // break가 없어서 계속 실행 (폴스루)
        break;
    default:
        System.out.println("etc");
}
// 출력: two, three
```
- **폴스루**: `break`가 없으면 맞는 case부터 **아래로 계속** 실행 (모든 case가 실행되는 것이 아님)
- `case` 뒤에는 **값**만 올 수 있음 (String도 가능: `case "A":`)

#### default가 위에 있어도 같은 규칙 (기능사 실기 대비)
```java
int m = 9, t = 0;
switch (m) {
    default: t += 10;         // 맞는 case가 없어서 여기로 들어옴
    case 1:  t += 1;          // break 없음 → 계속
    case 2:  t += 2; break;
}
System.out.println(t);        // 13
```
- default는 위치와 상관없이 "맞는 게 없을 때 들어가는 **입구**"일 뿐, 들어간 뒤엔 똑같이 아래로 흐름

#### 반복문 안의 switch: break는 switch만 빠져나감
```java
int s = 0;
for (int i = 1; i <= 3; i++) {
    switch (i) {
        case 1: s += 1;               // i=1: +1 → 폴스루
        case 2: s += 10; break;       // i=1: +10 (11), i=2: +10 (21) → switch만 종료
        default: s += 100;            // i=3: +100 (121)
    }
}
System.out.println(s);                // 121 (for는 끝까지 돈다)
```

### 삼항 연산자
```java
int max = (a > b) ? a : b;
```

## 2. 반복문

```java
for (int i = 0; i < 3; i++) { ... }   // 0, 1, 2

int i = 0;
while (i < 3) { i++; }

do {
    // 조건과 상관없이 최소 1번 실행
} while (조건);
```
- 중괄호 없는 `for`는 **바로 다음 한 문장만** 반복
- `break`: 반복 종료 (중첩 반복이면 **안쪽 반복만** 종료)
- `continue`: 이번 바퀴만 건너뛰고 다음 바퀴로 (`while`에서 증가식을 건너뛰면 무한 루프 주의)

```java
int k = 10;
do {
    System.out.print(k + " ");    // 10 (조건 검사 전에 1번 실행)
    k++;
} while (k < 5);

for (int i = 0; i < 5; i++) {
    if (i == 1) continue;         // 1 건너뜀 (for의 i++는 실행됨)
    if (i == 3) break;
    System.out.print(i + " ");    // 0 2
}
```

### 레이블 break / continue (기능사 실기 대비)
```java
outer:
for (int i = 0; i < 3; i++) {
    for (int j = 0; j < 3; j++) {
        if (j == 1) continue outer;   // 바깥 for의 다음 회차로
        if (i == 2) break outer;      // 바깥 for까지 종료
        System.out.print(i + "" + j + " ");
    }
}
// 00 10
```
- 레이블 없는 break / continue는 **가장 가까운 반복 하나**에만 적용

### 구구단 (중첩 for)
```java
for (int dan = 2; dan <= 9; dan++) {
    for (int k = 1; k <= 9; k++) {
        System.out.println(dan + " * " + k + " = " + (dan * k));
    }
}
```

## 3. 배열 입문
- **같은 자료형**의 데이터를 하나로 묶어 관리
- 배열은 **참조형(객체)** → `length` 필드가 있음

```java
int[] arr = new int[3];       // 칸 3개, 기본값 0
int[] nums = {10, 20, 30};
System.out.println(nums.length);   // 3
```

## 4. 기본형 vs 참조형

| | 기본형 (`int`, `double` …) | 참조형 (배열, 객체, `String`) |
|---|---|---|
| 변수에 저장되는 것 | **값 자체** | 객체의 **주소** |
| 저장 위치 | 스택 | 객체는 힙, 변수(주소)는 스택 |
| 대입 `b = a` | 값 복사 | 주소 복사 (같은 객체를 가리킴) |
