# 1주차 · 자바 시작하기

> 헷갈렸던 부분과 해결 과정: [week01-deep-dive.md](week01-deep-dive.md)

> 교재: 『미라클 자바 프로그래밍』 2장 (자료형·변수·형 변환)

## 1. 자바의 특징
- 자동 메모리 관리 (가비지 컬렉터)
- 멀티스레딩 지원
- 강력한 보안, 풍부한 표준 라이브러리
- 엄격한 타입 검사와 예외 처리

## 2. 자바 프로그램의 구조
- **객체** = 데이터(변수) + 동작(메서드)
- **클래스**: 객체의 설계도
- **패키지**: 클래스를 묶는 이름 공간

```java
public class Hello {
    public static void main(String[] args) {
        System.out.println("Hello, Java");
    }
}
```

## 3. 이클립스 프로젝트 만들기
1. File → New → Java Project (이름 입력, `Create module-info.java` 체크 해제)
2. `src` → New → Package
3. Package → New → Class (`public static void main` 체크)

## 4. 기본 자료형

| 자료형 | 예 | 비고 |
|---|---|---|
| `int` | `10` | 정수 |
| `double` | `3.14` | 실수 |
| `char` | `'A'` | 문자 1개, 작은따옴표, 비워 둘 수 없음 |
| `boolean` | `true`, `false` | 참/거짓 |
| `String` | `"Java"` | 문자열 (기본형이 아니라 클래스) |

- `var`: 컴파일러가 대입한 값을 보고 타입을 추론 (`var n = 10;` → int)

## 5. 이스케이프 시퀀스
- `\n` 줄바꿈, `\t` 탭

## 6. 형 변환

| 종류 | 방향 | 문법 |
|---|---|---|
| 자동 형 변환 | 작은 타입 → 큰 타입 (`int` → `double`) | 자동 |
| 강제 형 변환 | 큰 타입 → 작은 타입 (`double` → `int`) | `(int) 3.7` → `3` (소수점 유실) |

```java
int i = 10;
double d = i;          // 자동: 10.0
int j = (int) 3.7;     // 강제: 3
char c = 'A';
int code = c;          // 유니코드 값: 65
```

## 7. Scanner로 입력 받기
```java
import java.util.Scanner;

public class InputTest {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        System.out.println(n * 2);
        sc.close();
    }
}
```
- `import java.util.Scanner;` 필요 (C의 `scanf` 역할)
