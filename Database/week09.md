# 9주차 · 보안과 권한 관리, 파이썬 웹 화면(Streamlit·Flask)

> 헷갈렸던 부분과 해결 과정: [week09-deep-dive.md](week09-deep-dive.md)

> 교재 11장 + 파이썬 실습 · 수업 메모와 녹음으로 채움
>
> 이 주차의 SQL(`CREATE USER`, `GRANT`, `REVOKE`, `ROLE`)은 MySQL 전용 문장이라, 이 저장소를 정리한 환경(sqlite)에서는 실행하지 못했다. 수업에서 Workbench로 실습한 문법을 정리한 것이다.

## 1. 데이터베이스 보안 3가지

| 보안 | 무엇으로부터 | 방법 |
|---|---|---|
| 물리적 환경 보안 | 자연재해 등 **물리적 피해** | 백업, 다른 지역에 복사본(재해 복구) |
| 권한 관리를 통한 보안 | **권한 없는 사용자**의 접근 | 계정·로그인, `GRANT` / `REVOKE` |
| 운영 관리를 통한 보안 | 권한이 있는 사용자가 **제약조건을 위반**하는 것 | 무결성 제약조건(기본키, 외래키 등), 중요한 값 암호화 |

## 2. 권한 관리 (접근 제어)

- 계정이 발급된 사용자가 **로그인에 성공**해야만 DB에 접근할 수 있다
- 로그인한 사용자도 **허용된 권한 안에서만** DB를 쓸 수 있다
- DB의 모든 객체(테이블 등)는 **만든 사용자만** 처음에 사용 권한을 가진다 → 다른 사람에게는 `GRANT`로 나눠 준다

```
로그인 실패 ──▶ 접근 거부
로그인 성공 ──▶ 권한 확인 ──▶ 권한 있음: 실행
                          └─▶ 권한 없음: command denied
```

## 3. 사용자 만들기 (MySQL)

```sql
CREATE USER 'kim'@'localhost' IDENTIFIED BY '비밀번호';   -- 내 컴퓨터에서만 접속
CREATE USER 'kim2'@'%' IDENTIFIED BY '비밀번호';          -- % = 어디서든 접속 (외부 허용)
CREATE USER IF NOT EXISTS 'kim'@'localhost' IDENTIFIED BY '비밀번호';  -- 이미 있으면 건너뜀
DROP USER 'kim'@'localhost';                              -- 사용자 삭제
SELECT user, host FROM mysql.user;                        -- 사용자 목록 (mysql DB의 user 표)
```
- 막 만든 사용자는 `USAGE` 권한만 있다 = **로그인만 가능, 열쇠는 하나도 없음**
- 실습 때는 root로 다 되기 때문에, 권한을 확인하려면 Workbench에서 그 사용자로 **새 커넥션**을 만들어 접속해 봐야 한다

## 4. 권한 부여: GRANT

```
GRANT 권한 ON 객체 TO 사용자 [WITH GRANT OPTION];
```

| 자리 | 들어가는 것 |
|---|---|
| 권한 | `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `REFERENCES`(외래키 제약조건 정의), `ALL PRIVILEGES` |
| 객체 | 실제로 있는 `DB이름.테이블이름` (`USE`로 DB를 잡았으면 테이블 이름만) |
| 사용자 | `'kim'@'localhost'`, 모든 사용자는 `PUBLIC` |

```sql
GRANT SELECT ON sales.고객 TO 'kim'@'localhost';                 -- 고객: 조회만
GRANT SELECT, INSERT ON sales.주문 TO 'kim'@'localhost';         -- 주문: 조회 + 추가
GRANT UPDATE(등급, 적립금) ON sales.고객 TO 'kim'@'localhost';   -- 특정 열만 수정
GRANT SELECT ON sales.제품 TO 'lee'@'localhost' WITH GRANT OPTION;  -- 받은 권한을 남에게 줄 수 있음
```
- 권한 이름 = **DML 명령어 이름**. 받은 명령어만 그 테이블에 쓸 수 있다
- `WITH GRANT OPTION`: 내가 받은 권한을 **다른 사용자에게 다시 줄 수 있는** 권한. 안 주면 받은 사람은 남에게 못 준다
- 시스템 권한(테이블·뷰를 **만드는** 권한)은 특정 객체를 지정하지 않는다
  - 교재 문법: `GRANT CREATE TABLE TO 사용자;` — `ON`이 없음
  - MySQL은 `GRANT CREATE ON sales.* TO …;`처럼 DB 단위로 준다

## 5. 권한 취소: REVOKE

```
REVOKE 권한 ON 객체 FROM 사용자 CASCADE | RESTRICT;
```
```
관리자 ──WITH GRANT OPTION──▶ A ──▶ B ──▶ C

REVOKE … FROM A CASCADE   →  A, B, C 권한이 연쇄적으로 모두 취소
REVOKE … FROM A RESTRICT  →  A가 남에게 준 권한이 있으면 취소하지 않음(거부)
```
- `GRANT … TO`, `REVOKE … FROM` (전치사가 다르다)
- `CASCADE`/`RESTRICT`는 교재(표준 SQL) 문법이다. MySQL의 `REVOKE`는 이 옵션 없이 쓴다

## 6. 역할 (ROLE)

사용자마다 권한을 하나씩 주면 번거로우니, **권한 바구니(역할)**를 먼저 만들고 사용자에게 바구니를 준다.
```sql
CREATE ROLE 'clerk';                                          -- ① 바구니 만들기
GRANT SELECT, INSERT, DELETE ON sales.고객 TO 'clerk';        -- ② 바구니에 권한 담기
GRANT 'clerk' TO 'kim'@'localhost';                           -- ③ 사용자에게 바구니 주기
DROP ROLE 'clerk';                                            -- 역할 삭제
```
```
사용자별 부여        kim ← SELECT, INSERT, DELETE
                    lee ← SELECT, INSERT, DELETE      (반복)
역할 사용            clerk = {SELECT, INSERT, DELETE}
                    kim ← clerk,  lee ← clerk        (한 번에)
```
- MySQL 8은 받은 역할이 바로 켜지지 않아서 `SET DEFAULT ROLE 'clerk' TO 'kim'@'localhost';`를 해야 로그인 때 적용된다
- 수업: 현업에서 주로 **DBA**가 쓰는 기능이니 "이런 게 있다" 정도로 알면 된다

## 7. 파이썬 실습 흐름

8주차(pymysql로 INSERT, 커서로 fetch) 이어서 화면을 붙였다.

| 단계 | 도구 | 하는 일 |
|---|---|---|
| 1 | pymysql | DB 연결, `SELECT` 실행 |
| 2 | pandas | 결과를 표(DataFrame)로 |
| 3 | Streamlit | 웹 화면에 스크롤 가능한 표 출력 (와이드 모드, 행 수 표시, CSV 다운로드) |
| 4 | Flask (수업 시연) | 웹 프레임워크, `127.0.0.1:5000`에서 상품 등록·주문·수정·삭제 화면 |

```
설치    py -m pip install pymysql pandas streamlit
실행    py -m streamlit run 파일이름.py      → 브라우저 localhost:8501
종료    터미널에서 Ctrl + C
```
- 프로그램 안 접속 계정은 **root를 쓰지 않고** 권한을 준 사용자 계정으로
- Streamlit은 ▶ 버튼(`python 파일.py`)으로 실행하면 웹 서버가 켜지지 않는다 → `streamlit run`
- 이 환경에서는 Streamlit을 설치할 수 없어 화면 코드는 실행 확인을 못 해서 코드는 싣지 않았다

## 8. 프로젝트 과제 (녹음 기준)

- SQL로 DB를 만들고, **웹에서 조회·입력·수정·삭제**가 되는 프로그램을 만든다 (화면 구성은 자유)
- **업무(요구사항) 분석부터** 시작한다
- 주제는 자유지만 **온라인 쇼핑몰은 제외**(수업 공통 예제로 이미 함), 다른 사람과 주제가 **겹치지 않게**
- AI로 코드를 만들 수는 있지만 발표 때 **소스 코드를 한 줄씩 본인이 설명**할 수 있어야 한다
- 다음 주: 남은 교재 내용(분산 데이터베이스 등) 간단히 소개 후 프로젝트 진행
