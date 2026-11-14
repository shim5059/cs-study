# JAVA

안드로이드프로그래밍 수업(2026-2학기)에서 배운 자바 내용을 주차별로 정리한 복습 기록

- 교재: 『미라클 자바 프로그래밍』
- 실습 환경: Eclipse

수업 뒤에 다시 복습하면서 실행 결과를 따라가다 헷갈린 부분을 해당 주차에 덧붙였다. 덧붙인 부분은 제목에 **(복습 추가)**로 표시했다.

| 주차 | 덧붙인 내용 |
|---|---|
| 1주차 | 연산자 함정 (정수 나눗셈, 문자열 `+`, char, `++`, 단락 평가, 비트), printf 서식 |
| 2주차 | default가 실행되는 두 경우, 반복문 안 switch의 break, 삼항 연산자 + 후위 증감, do-while과 출력 위치, 레이블 (+ deep-dive) |
| 3주차 | 배열 기본값, 길이 표기, 가변 2차원 배열 (+ deep-dive: `r.length` 다시 틀림) |
| 5주차 | 오버로딩 선택 기준, try-catch-finally 실행 순서, 여러 catch, 주요 예외, return과 finally |
| 6주차 | static은 변수 타입 기준, 필드·static·super가 섞인 다형성 |
| 7주차 | 생성자 체인(this()·super()), 생성자 안의 오버라이딩 호출, 오버로딩은 덮어쓰지 않음, default 메서드 재정의 (+ deep-dive) |
| 8주차 | `+`로 만든 String의 `==`, String 메서드 추가, `replaceAll` 정규식 `[^…]`, 대소문자 철자 규칙, 자주 쓰는 라이브러리 (Math, ArrayList, HashMap) |

각 주차는 두 파일로 나뉜다.
- `weekNN.md`: 개념 요약
- `weekNN-deep-dive.md`: 실제로 틀렸던 것 → 처음 생각 → 원리 → 깨달음

## 주차별 목차

| 주차 | 주제 | 교재 | 헷갈린 것 & 해결 |
|---|---|---|---|
| [1주차](week01.md) | 자바 특징, 자료형, 형 변환, Scanner | 2장 | [deep-dive](week01-deep-dive.md) |
| [2주차](week02.md) | 조건문, switch, 반복문, 배열 입문, 기본형 vs 참조형 | 3장 | [deep-dive](week02-deep-dive.md) |
| [3주차](week03.md) | 배열 심화 (for-each, Arrays, 2차원 배열, 복사) | 3장 | [deep-dive](week03-deep-dive.md) |
| [4주차](week04.md) | 객체지향 4대 특징, 클래스 구조, 생성자, this, final | 5장 | [deep-dive](week04-deep-dive.md) |
| [5주차](week05.md) | 오버로딩/오버라이딩, 메모리, 패키지·접근 제한자, static, 예외 처리 | 5장 | [deep-dive](week05-deep-dive.md) |
| [6주차](week06.md) | 예외 던지기, enum, 상속, 캐스팅, instanceof, 다형성·바인딩 | 5~6장 | [deep-dive](week06-deep-dive.md) |
| — | 중간고사 (3~6장, 추상 클래스 이전까지) | | |
| [7주차](week07.md) | 추상 클래스, 인터페이스, 캐스팅·생성자 흐름 정리, 배송 시스템 | 6장 | [deep-dive](week07-deep-dive.md) |
| [8주차](week08.md) | 자바 기본 패키지: 모듈, Object(equals/toString/getClass), Wrapper, String | 9장 | [deep-dive](week08-deep-dive.md) |
