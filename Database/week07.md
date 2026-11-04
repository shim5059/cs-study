# 7주차 · SQL (데이터 정의어와 데이터 조작어)

> 헷갈렸던 부분과 해결 과정: [week07-deep-dive.md](week07-deep-dive.md)

> 교재 7장 · 중간고사 이후 첫 수업. 수업 메모는 GROUP BY까지만 있어서, 그 뒤(HAVING·조인·부속 질의문·INSERT/UPDATE/DELETE·뷰)는 녹음과 복습 때 풀어 본 문제로 채움
>
> 수업 강조: SELECT문이 가장 중요, 시험에서는 **문장 한 줄을 주고 SQL을 작성**하는 형태가 될 것이라고 함
>
> 아래 예제는 직접 만든 데이터이고, 결과는 모두 sqlite로 실행해 확인했다 (MySQL과 다른 점은 따로 표시)

## 0. 예제 데이터

```
고객                                        제품
고객아이디 고객이름 나이  등급   적립금        제품번호 제품명   재고량 단가  제조업체
cat      김민준  23   gold   3000         p1     초코쿠키  300  1500 달빛제과
dog      이서연  31   vip    8000         p2     매운라면  800  1200 해맑식품
fox      박도윤  NULL silver 0            p3     딸기우유  500  1800 해맑식품
owl      김하은  27   gold   1500         p4     버터과자  150  2500 달빛제과
bee      최지호  35   silver 500

주문
주문번호 주문고객 주문제품 수량 주문일자
o1      cat     p1     10  2026-03-02
o2      dog     p2     20  2026-03-05
o3      cat     p3      5  2026-03-09
o4      owl     p2     15  2026-04-01
o5      dog     p4      8  2026-04-03
o6      cat     p2     12  2026-04-10
```

## 1. SQL 분류

| 분류 | 하는 일 | 명령어 |
|---|---|---|
| DDL (정의어) | 표의 **구조**를 만들고 고치고 지움 | `CREATE`, `ALTER`, `DROP` |
| DML (조작어) | 표 안의 **데이터**를 다룸 | `SELECT`, `INSERT`, `UPDATE`, `DELETE` |
| DCL (제어어) | 권한 관리 | `GRANT`, `REVOKE` |

## 2. CREATE TABLE과 제약조건

```sql
CREATE TABLE 주문 (
    주문번호 CHAR(2) NOT NULL,
    주문고객 VARCHAR(20),
    주문제품 CHAR(2),
    수량     INT,
    주문일자 DATE,
    PRIMARY KEY (주문번호),
    FOREIGN KEY (주문고객) REFERENCES 고객(고객아이디),
    FOREIGN KEY (주문제품) REFERENCES 제품(제품번호)
);
```

| 자료형 | 뜻 |
|---|---|
| `INT` | 정수 |
| `CHAR(n)` | 길이 n 고정 문자 |
| `VARCHAR(n)` | 최대 n 가변 문자 |
| `DATE` | 날짜 `'2026-03-02'` |

| 제약조건 | 뜻 |
|---|---|
| `NOT NULL` | 빈 값(NULL) 금지 |
| `DEFAULT 값` | 값을 안 넣으면 기본값 |
| `PRIMARY KEY` | 기본키 (중복·NULL 불가) |
| `UNIQUE` | 대체키 (**중복만** 불가, NULL은 허용) |
| `FOREIGN KEY (열) REFERENCES 표(열)` | 외래키 |
| `CHECK (조건)` | 값 조건, 예: `CHECK (재고량 >= 0 AND 재고량 <= 10000)` |

**참조되는 행을 지울 때의 처리** (`FOREIGN KEY … ON DELETE …`)

| 옵션 | 부모 행 삭제 시 |
|---|---|
| `NO ACTION` (기본) | 자식이 참조 중이면 **삭제 거부** |
| `CASCADE` | 참조하던 자식 행도 **같이 삭제** |
| `SET NULL` | 자식의 외래키를 **NULL**로 |

실행 확인
- 없는 고객 `'zzz'`로 주문 삽입 → `FOREIGN KEY constraint failed` (참조 무결성)
- 주문이 있는 고객 `cat` 삭제 (NO ACTION) → 거부
- `주문고객`을 NULL로 주문 삽입 → **성공** (외래키는 NULL 가능)
- 재고량을 −5로 수정 → `CHECK constraint failed`
- `ON DELETE CASCADE`로 만든 학생 표에서 학과 d1 삭제 → d1 학생 2명도 같이 삭제
- `UNIQUE` 열에 NULL 두 번 삽입 → 성공

## 3. ALTER TABLE / DROP TABLE

```sql
ALTER TABLE 고객 ADD 가입날짜 DATE;              -- 열 추가 (기존 행은 NULL)
ALTER TABLE 고객 DROP COLUMN 가입날짜;           -- 열 삭제
ALTER TABLE 고객 ADD CONSTRAINT CHK_AGE CHECK (나이 >= 20);   -- 제약조건 추가 (※)
DROP TABLE 배송업체;                              -- 표 자체를 삭제
```
> ※ `ADD CONSTRAINT`는 sqlite가 지원하지 않아 실행 확인을 못 했다 (MySQL 문법)

| | 지우는 것 | 분류 |
|---|---|---|
| `DELETE FROM 표` | 데이터(행)만, **표는 남음** | DML |
| `DROP TABLE 표` | 표 **구조까지** 통째로 | DDL |

## 4. SELECT 기본

```sql
SELECT [ALL | DISTINCT] 열 리스트
FROM   테이블 리스트
[WHERE  조건]
[GROUP BY 열 [HAVING 조건]]
[ORDER BY 열 [ASC | DESC]];
```

| SQL | 결과 |
|---|---|
| `SELECT * FROM 고객;` | 모든 열 (`*` = 전체) |
| `SELECT 고객이름, 등급 FROM 고객;` | 두 열만 |
| `SELECT ALL 제조업체 FROM 제품;` | 달빛제과, 해맑식품, 해맑식품, 달빛제과 (ALL은 기본값) |
| `SELECT DISTINCT 제조업체 FROM 제품;` | 달빛제과, 해맑식품 (중복 제거) |

```sql
SELECT 제품명, 단가, 단가 + 500 AS "조정단가" FROM 제품;
```
```
제품명   | 단가 | 조정단가
초코쿠키 | 1500 | 2000
매운라면 | 1200 | 1700
딸기우유 | 1800 | 2300
버터과자 | 2500 | 3000
```
- `AS`: 결과 화면에서만 열 이름을 바꿈 (표는 그대로)
- 따옴표: `'작은따옴표'` = **값**(문자열), `"큰따옴표"` = **이름**(별명)

## 5. WHERE

| 연산자 | |
|---|---|
| 비교 | `=` `<>` `<` `>` `<=` `>=` (같다는 `=` 하나) |
| 논리 | `AND` `OR` `NOT` |

```sql
SELECT 주문제품, 수량 FROM 주문 WHERE 주문고객 = 'cat' AND 수량 >= 10;
-- p1 10 / p2 12
```

**LIKE**: `%` = 0개 이상 아무 문자, `_` = 정확히 1개

| 조건 | 뜻 | 결과 |
|---|---|---|
| `고객이름 LIKE '김%'` | 김으로 시작 | 김민준, 김하은 |
| `고객아이디 LIKE '_o_'` | 3글자, 가운데 o | dog, fox |

**NULL 검색**은 `IS NULL` / `IS NOT NULL`
```sql
SELECT 고객이름 FROM 고객 WHERE 나이 IS NULL;   -- 박도윤
SELECT 고객이름 FROM 고객 WHERE 나이 = NULL;    -- 결과 0행 (= 로는 NULL을 못 찾음)
```

## 6. ORDER BY

```sql
SELECT 고객이름, 등급, 적립금 FROM 고객 ORDER BY 등급 ASC, 적립금 DESC;
```
```
김민준 | gold   | 3000
김하은 | gold   | 1500     ← 등급이 같으면 적립금 내림차순
최지호 | silver | 500
박도윤 | silver | 0
이서연 | vip    | 8000
```
- `ASC` 오름차순(기본값), `DESC` 내림차순, 항상 **맨 마지막**

## 7. 집계 함수

| 함수 | 뜻 |
|---|---|
| `COUNT` | 개수 |
| `MAX` / `MIN` | 최댓값 / 최솟값 |
| `SUM` / `AVG` | 합계 / 평균 (숫자만) |

```sql
SELECT COUNT(*), COUNT(나이), AVG(나이) FROM 고객;
-- 5 | 4 | 29        COUNT(*)는 행 수, COUNT(나이)는 NULL 제외
SELECT COUNT(DISTINCT 제조업체) AS "제조업체 수" FROM 제품;
-- 2
```
- 집계 함수는 **NULL을 빼고** 계산한다
- 집계 함수는 `WHERE`에 쓸 수 없다 (`WHERE 적립금 > AVG(적립금)` → 에러). 그룹 조건은 `HAVING`, 전체 평균과 비교는 부속 질의문

## 8. GROUP BY와 HAVING

```sql
SELECT 주문제품, SUM(수량) AS "총주문수량" FROM 주문 GROUP BY 주문제품;
```
```
주문제품 | 총주문수량
p1      | 10
p2      | 47      ← 20 + 15 + 12
p3      | 5
p4      | 8
```

```sql
SELECT 주문고객, COUNT(*) AS 주문횟수, SUM(수량) AS 총수량
FROM 주문
GROUP BY 주문고객
HAVING COUNT(*) >= 2;
```
```
cat | 3 | 27
dog | 2 | 28
```
- `GROUP BY 기준열`: 기준열 값이 같은 행끼리 묶음
- `SELECT`에는 **기준열**과 **집계 함수**만 쓴다
- `WHERE` = 묶기 **전** 행 조건, `HAVING` = 묶은 **후** 그룹 조건

**실행 순서**
```
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
```
그래서 `SELECT`에서 만든 별명은 `ORDER BY`에서 쓸 수 있다.

## 9. 조인

**쉼표 + WHERE** (교재 방식)
```sql
SELECT 고객.고객이름, 제품.제품명, 주문.수량
FROM   고객, 주문, 제품
WHERE  고객.고객아이디 = 주문.주문고객
  AND  주문.주문제품 = 제품.제품번호
  AND  제품.제조업체 = '해맑식품';
```
```
이서연 | 매운라면 | 20
김민준 | 딸기우유 | 5
김하은 | 매운라면 | 15
김민준 | 매운라면 | 12
```
- 표 n개를 이으면 조인 조건은 **n − 1개** (위: 3개 → 2개)
- 조인 조건을 빼면 카티션 프로덕트: `SELECT COUNT(*) FROM 고객, 주문;` → 5 × 6 = **30**
- `표이름.열이름`: 두 표에 같은 이름의 열이 있을 때는 꼭 붙이고, 이름이 겹치지 않으면 생략 가능 (붙이면 읽기 쉬움)

**INNER JOIN** (같은 결과, 조인 조건을 `ON`에 분리)
```sql
SELECT 고객.고객이름, 주문.주문제품, 주문.수량
FROM   고객 INNER JOIN 주문 ON 고객.고객아이디 = 주문.주문고객
WHERE  고객.고객아이디 = 'cat';
-- 김민준 p1 10 / 김민준 p3 5 / 김민준 p2 12
```

| 조인 | 결과 |
|---|---|
| `INNER JOIN` | 양쪽에 짝이 있는 행만 |
| `LEFT OUTER JOIN` | 왼쪽 표는 전부, 짝 없으면 오른쪽을 NULL |
| `RIGHT OUTER JOIN` | 오른쪽 표는 전부 |
| `FULL OUTER JOIN` | 양쪽 전부 (MySQL은 이 문법이 없어 LEFT와 RIGHT를 `UNION`으로 합침) |

```sql
SELECT 고객.고객이름, 주문.주문번호
FROM 고객 LEFT OUTER JOIN 주문 ON 고객.고객아이디 = 주문.주문고객;
```
```
김민준 o1 / 김민준 o3 / 김민준 o6 / 김하은 o4 / 이서연 o2 / 이서연 o5
박도윤 NULL / 최지호 NULL      ← 주문이 없는 고객도 나옴
```

**조인 + 그룹 + 정렬** (고객별 총주문수량, 많은 순)
```sql
SELECT   고객.고객이름, SUM(주문.수량) AS "총주문수량"
FROM     고객, 주문
WHERE    고객.고객아이디 = 주문.주문고객
GROUP BY 고객.고객이름
ORDER BY "총주문수량" DESC;
```
```
이서연 | 28
김민준 | 27
김하은 | 15
```

## 10. 부속 질의문 (서브쿼리)

괄호 안 `SELECT`가 **먼저** 실행되고, 그 결과를 바깥 `WHERE`가 쓴다.

| 부속 질의 결과 | 연산자 |
|---|---|
| 값 **하나** (단일 행) | `=`, `>`, `<` … |
| 값 **여러 개** (다중 행) | `IN`, `NOT IN`, `EXISTS`, `NOT EXISTS` |

```sql
-- 매운라면과 같은 제조업체의 제품
SELECT 제품명, 단가 FROM 제품
WHERE 제조업체 = (SELECT 제조업체 FROM 제품 WHERE 제품명 = '매운라면');
-- 매운라면 1200 / 딸기우유 1800

-- 평균 단가보다 비싼 제품 (집계 함수는 부속 질의에서)
SELECT 제품명, 단가 FROM 제품 WHERE 단가 > (SELECT AVG(단가) FROM 제품);
-- 딸기우유 1800 / 버터과자 2500   (평균 1750)

-- p2를 주문한 고객 (여러 명 → IN)
SELECT 고객이름 FROM 고객
WHERE 고객아이디 IN (SELECT 주문고객 FROM 주문 WHERE 주문제품 = 'p2');
-- 김민준 / 이서연 / 김하은

-- 한 번도 주문하지 않은 고객
SELECT 고객이름 FROM 고객
WHERE 고객아이디 NOT IN (SELECT 주문고객 FROM 주문);
-- 박도윤 / 최지호

-- 15개 이상 주문한 적이 있는 고객 (바깥 행마다 확인)
SELECT 고객이름 FROM 고객
WHERE EXISTS (SELECT * FROM 주문
              WHERE 주문.주문고객 = 고객.고객아이디 AND 주문.수량 >= 15);
-- 이서연 / 김하은
```
- 결과가 여러 행인데 `=`를 쓰면 MySQL은 에러를 낸다 → `IN` 사용 (sqlite는 첫 행만 써서 에러가 안 나니 주의)
- 부속 질의문 안에는 `ORDER BY`를 쓰지 않는다
- 해석 요령: "~한 고객의 이름" → 바깥 = 고객, 괄호 안 = "~한" 조건을 가진 표

## 11. INSERT / UPDATE / DELETE

```sql
INSERT INTO 고객 (고객아이디, 고객이름, 등급) VALUES ('ant', '정유나', 'silver');
-- 빠진 열: 나이 → NULL, 적립금 → DEFAULT 0

UPDATE 제품 SET 단가 = 단가 + 100 WHERE 제조업체 = '달빛제과';
-- 초코쿠키 1500 → 1600, 버터과자 2500 → 2600

DELETE FROM 고객 WHERE 고객아이디 = 'ant';
```
- `UPDATE`·`DELETE`에서 **WHERE를 빼면 모든 행**이 바뀌거나 지워진다
- Workbench는 기본으로 safe update 모드가 켜져 있어서, 키 조건이 없는 `UPDATE`/`DELETE`를 막는다

## 12. 뷰 (VIEW)

- 다른 테이블을 기반으로 만든 **가상 테이블** (데이터를 따로 저장하지 않고, 조회할 때마다 기반 테이블에서 계산)
- 쓰는 이유: 복잡한 질의를 간단히, 필요한 열만 보여 줘 **보안**에 도움

```sql
CREATE VIEW 우수고객 AS
SELECT 고객아이디, 고객이름, 적립금 FROM 고객 WHERE 등급 = 'gold';

SELECT * FROM 우수고객;
-- cat 김민준 3000 / owl 김하은 1500
```
- 기반 테이블에서 최지호의 등급을 gold로 바꾸면 뷰에도 **바로** 나타남 (확인함)
- 뷰는 주로 **조회용**. 기본키가 빠졌거나 집계·조인으로 만든 뷰는 수정이 안 된다
- `WITH CHECK OPTION`: 뷰를 통한 삽입·수정이 뷰의 조건(`등급 = 'gold'`)을 벗어나지 못하게 막음 (sqlite 미지원이라 실행 확인 못 함)
- 삭제: `DROP VIEW 우수고객;`

## 13. 삽입 SQL (프로그램 속 SQL)

- 일반 프로그래밍 언어 코드 안에 SQL을 넣어 쓰는 것
- `SELECT` 결과가 여러 행이면 **커서**로 한 행씩 차례로 꺼낸다
- 8주차에 파이썬(pymysql)으로 실습 → [week08.md](week08.md)
