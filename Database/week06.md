# 6주차 · MySQL Workbench 실습 (DB 만들고 데이터 넣기)

> 헷갈렸던 부분과 해결 과정: [week06-deep-dive.md](week06-deep-dive.md)

> 교재 7장 실습 준비 · 수업에서 **시험에는 안 나온다**고 한 실습 주차 (DDL → DML 흐름 맛보기)

## 1. 작업 흐름

```
DB 만들기 ─▶ 테이블 만들기 ─▶ 데이터 넣기 ─▶ 조회해서 확인
CREATE DATABASE  CREATE TABLE     INSERT          SELECT
└──────── DDL ────────┘          └──── DML ────┘
```

## 2. Workbench 화면

| 위치 | 이름 | 하는 일 |
|---|---|---|
| 가운데 흰 칸 | 쿼리 편집기 | SQL을 쓰는 곳 |
| 왼쪽 아래 Schemas 탭 | 스키마 목록 | 만든 DB와 테이블 확인 |
| 왼쪽 아래 Administration 탭 | 관리 메뉴 | 서버 관리 |
| 편집기 아래 | 결과 표 (Result Grid) | `SELECT` 결과가 표로 나옴 |
| 맨 아래 Output | 실행 기록 | 초록 = 성공, 빨강 = 실패 |

| 단축키 | 동작 |
|---|---|
| `Ctrl + Shift + Enter` (번개) | 전체 실행 |
| `Ctrl + Enter` (번개 + I) | 커서가 있는 문장 하나만 실행 |
| `Ctrl + S` | `.sql` 파일로 저장 |

- MySQL 서버가 꺼져 있으면 Windows `services.msc`에서 MySQL 서비스를 시작

## 3. SQL 기본 규칙

1. 문장 끝에 세미콜론 `;`
2. 키워드는 대소문자 구분 안 함 (`select` = `SELECT`, 보통 대문자)
3. 문자 **값**은 작은따옴표 `'…'`
4. 줄바꿈은 자유, `;`가 나와야 문장 끝

## 4. DB 만들기 (MySQL 전용 문장)

```sql
DROP DATABASE IF EXISTS shop;   -- 같은 이름이 있으면 지우고
CREATE DATABASE shop;           -- 새로 만들고
USE shop;                       -- 앞으로 이 DB를 사용
```
> 이 세 줄은 MySQL 전용이라, 이 저장소를 정리한 환경(sqlite)에서는 실행하지 못했다. 아래 테이블·데이터 부분은 sqlite로 실행해 확인했다.

## 5. 테이블 만들기와 데이터 넣기 (직접 만든 예)

```sql
CREATE TABLE 고객 (
    고객아이디 VARCHAR(20) NOT NULL,
    고객이름   VARCHAR(10) NOT NULL,
    나이       INT,
    등급       VARCHAR(10) NOT NULL,
    적립금     INT DEFAULT 0,
    PRIMARY KEY (고객아이디)
);

INSERT INTO 고객 VALUES ('cat', '김민준', 23, 'gold',   3000);
INSERT INTO 고객 VALUES ('dog', '이서연', 31, 'vip',    8000);
INSERT INTO 고객 VALUES ('fox', '박도윤', NULL, 'silver', 0);   -- 나이 모름 → NULL

SELECT * FROM 고객;
```
```
고객아이디 | 고객이름 | 나이 | 등급   | 적립금
cat       | 김민준   | 23   | gold   | 3000
dog       | 이서연   | 31   | vip    | 8000
fox       | 박도윤   | NULL | silver | 0
```

- 외래키로 연결된 테이블은 **부모(참조되는 쪽)를 먼저** 만들고 데이터도 부모부터 넣는다
  (주문의 `주문고객`이 고객을 참조하면 고객 → 주문 순서)
- 이 실습 DB(고객·제품·주문)를 7주차 SQL 복습에서 계속 사용
