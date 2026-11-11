# 데이터베이스 (SQL)

데이터베이스 설계 수업(2026-2학기)에서 배운 내용을 주차별로 정리한 복습 기록

- 교재: 『데이터베이스 개론』
- 실습 환경: MySQL Workbench, Python(pymysql, pandas, Streamlit)
- 예제 데이터는 모두 직접 만든 것이고, SQL 결과는 sqlite로 실행해 확인했다 (MySQL 전용 문장은 파일 안에 따로 표시)

각 주차는 두 파일로 나뉜다.
- `weekNN.md`: 개념 요약
- `weekNN-deep-dive.md`: 실제로 틀렸던 것 → 처음 생각 → 원리 → 깨달음

## 주차별 목차

| 주차 | 주제 | 교재 범위 | 헷갈린 것 & 해결 |
|---|---|---|---|
| [1주차](week01.md) | 데이터·정보, DB 특징, DBMS 기능, 스키마, 3단계 구조와 데이터 독립성, 데이터 사전 | 1~3장 | [deep-dive](week01-deep-dive.md) |
| [2주차](week02.md) | 데이터 모델링, 데이터 모델 3요소, E-R 모델과 ERD 기호 | 4장 | [deep-dive](week02-deep-dive.md) |
| [3주차](week03.md) | 릴레이션 용어, 릴레이션 특성, 키의 종류, 개체·참조 무결성 | 5장 | [deep-dive](week03-deep-dive.md) |
| [4주차](week04.md) | 관계 대수 연산자·조인, 설계 5단계, ERD → 릴레이션 변환 규칙 | 6장, 8장 | [deep-dive](week04-deep-dive.md) |
| [5주차](week05.md) | 요구사항 분석 실습, 이상 현상, 함수 종속, 정규화(1NF~BCNF) | 8~9장 | [deep-dive](week05-deep-dive.md) |
| [6주차](week06.md) | MySQL Workbench 실습: DB·테이블 만들고 데이터 넣기 (시험 제외) | 7장 실습 | [deep-dive](week06-deep-dive.md) (기록 없음) |
| — | 중간고사 (1~6장, 8장 + 9장 정규화 BCNF까지 / 7장 제외) · 서술형 10문제: 개념 5 + 관계 대수식 5 | | |
| [7주차](week07.md) | SQL: CREATE·ALTER·DROP, SELECT·WHERE·GROUP BY·HAVING, 조인, 부속 질의문, INSERT·UPDATE·DELETE, 뷰 | 7장 | [deep-dive](week07-deep-dive.md) |
| [8주차](week08.md) | 트랜잭션(ACID), 장애와 회복(redo·undo), 병행 제어·로킹·교착 상태, 파이썬 연동 | 10장 | [deep-dive](week08-deep-dive.md) |
| [9주차](week09.md) | 보안 3가지, 사용자·GRANT·REVOKE·역할, Streamlit·Flask로 DB 화면 만들기, 프로젝트 과제 | 11장 | [deep-dive](week09-deep-dive.md) |
