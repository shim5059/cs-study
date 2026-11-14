# 9주차 Deep Dive · 권한 실습과 Streamlit 실행에서 막혔던 것

> 개념 요약: [week09.md](week09.md)
>
> **틀렸던 것 → 처음 생각 → 원리 → 깨달음** 순서의 기록

---

## 1. `Table '학교.학생' doesn't exist` (Error 1146)

### 처음 생각 (오답)
예시로 받은 `GRANT SELECT, INSERT ON 학교.학생 TO ...`를 **그대로** 실행했다.

### 원리
```
GRANT 권한 ON  DB이름.테이블이름  TO 사용자
                 ▲
                 실제로 있는 테이블이어야 함
```
`학교.학생`은 자리표시용 이름이라 내 MySQL에는 없다. 내 테이블은 `sales` DB의 `고객`·`제품`·`주문`.
현재 DB를 `USE sales;`로 잡아뒀다면 `ON 고객`, 아니면 `ON sales.고객`.
지금 DB가 뭔지 모르면 `SELECT DATABASE();`

### 깨달음
GRANT의 객체 자리 = **내 DB에 실제로 있는 `DB.테이블`**. 예제 이름은 반드시 내 것으로 바꾼다.

---

## 2. `Operation CREATE USER failed` (Error 1396)

### 처음 생각 (오답)
GRANT를 고친 뒤 **번개 아이콘(전체 실행)**으로 다시 돌렸다.

### 원리
```
1차 실행:      CREATE USER kim ✔  GRANT ✘(1146)
2차 전체 실행:  CREATE USER kim ✘(1396, 이미 있음) → 여기서 멈춤 → 아래 GRANT는 실행조차 안 됨
```
CREATE USER는 1차 때 이미 성공했다. 전체 실행은 위에서부터 다시 돌리므로 같은 유저를 또 만들려다 실패하고, 그 아래 줄까지 가지 못한다.

### 깨달음
실습 스크립트는 **한 줄씩 `Ctrl + Enter`**. 다시 돌려도 되게 하려면 `CREATE USER IF NOT EXISTS`, 처음부터 깨끗하게 하려면 `DROP USER IF EXISTS` 먼저.

---

## 3. "주문은 조회 + 추가"가 무슨 뜻?

### 처음 생각
`GRANT SELECT, INSERT ON sales.주문`의 설명 "조회 + 추가"가 무슨 말인지 몰랐다.

### 원리
권한 이름 = **DML 명령어 이름**

```
GRANT SELECT, INSERT ON sales.주문 TO kim

 kim 창에서:
 SELECT * FROM sales.주문;            ⭕ 조회
 INSERT INTO sales.주문 VALUES (…);   ⭕ 추가
 UPDATE sales.주문 SET …;             ❌ command denied
 DELETE FROM sales.주문 …;            ❌ command denied
 SELECT * FROM sales.제품;            ❌ 제품은 권한 없음 → Navigator에도 안 보임
```

### 깨달음
`GRANT 명령어들 ON 테이블` = **그 테이블에 그 명령어만 써도 된다**는 허가. 테이블마다 따로 준다.

---

## 4. Streamlit이 안 켜짐: `pip` 인식 안 됨 → `missing ScriptRunContext`

### 처음 생각 (오답)
- 터미널에 `pip install pandas` → `'pip'은(는) 내부 또는 외부 명령 … 이 아닙니다`
- 설치 후 VSCode **▶ 실행 버튼**으로 실행 → 경고만 잔뜩 나오고 브라우저가 안 열림

### 원리
```
pip install …              ✘  pip 위치가 PATH에 없음
py -m pip install …        ✔  파이썬에게 "네 안의 pip 모듈 실행해"

▶ 버튼 = python db_streamlit.py     → 스크립트만 한 번 돌고 끝 (bare mode, 웹 서버 없음)
py -m streamlit run db_streamlit.py → 웹 서버를 켜고 localhost:8501 에서 대기
```
- 첫 실행 때 묻는 `Email:`은 엔터로 넘김
- 켜져 있는 동안 터미널은 멈춘 것처럼 대기, 끌 때 `Ctrl + C`
- 코드 저장 후 브라우저의 **Rerun**으로 반영

### 깨달음
명령을 못 찾으면 **`py -m 모듈`**. Streamlit은 파이썬 파일이지만 실행은 **`streamlit run`**.

---

## REVOKE 순서를 섞었다 (2026-11-14)

### 처음 생각 (오답)
"user1에게 부여했던 student 테이블의 SELECT 권한을 회수" → `REVOKE user1 FROM student SELECT`

### 원리
순서는 **무엇을(권한) → 어디에 대해(ON 표) → 누구에게서(FROM 사용자)** 하나뿐이다.
```sql
REVOKE SELECT ON student FROM user1;
GRANT  SELECT ON student TO   user1;   -- 앞부분은 같고 마지막 전치사만 다름
```
영어 문장처럼 읽는다: "revoke select on student from user1"

### 깨달음
REVOKE와 FROM은 기억했는데 자리를 몰랐다. `권한 ON 표`까지는 GRANT와 REVOKE가 똑같다.

---

## 정리

| 착각 | 바로잡은 규칙 |
|---|---|
| 예시 테이블 이름 그대로 GRANT | 객체 자리 = 내 DB에 **실제로 있는** `DB.테이블` |
| 고친 뒤 전체 실행 | 이미 성공한 CREATE USER가 1396 → **한 줄씩 실행** / `IF NOT EXISTS` |
| "조회 + 추가"가 뭔지 모름 | 권한 이름 = DML 이름, **테이블마다 따로** |
| `pip`, ▶ 버튼으로 Streamlit | `py -m pip`, `py -m streamlit run` |
| REVOKE 순서를 섞음 | `REVOKE 권한 ON 표 FROM 사용자` (GRANT와 같은 순서, TO ↔ FROM만 다름) |
