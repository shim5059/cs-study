# 07 · 라이브러리 (import, math, random)

> 출제기준의 "라이브러리 활용". 이 주제는 확인 문제를 한 번에 맞혀서 deep-dive 기록이 없다
>
> 다 외우지 않고 **이름을 보고 뜻이 떠오르는** 정도면 충분하다. **Java와 반대인 곳**만 확실히

## 1. import 네 가지

| 문법 | 호출 | Java로 치면 |
|---|---|---|
| `import math` | `math.sqrt(16)` | `Math.sqrt(16)` |
| `import math as m` | `m.sqrt(16)` | |
| `from math import sqrt` | `sqrt(16)` (모듈 이름 없이) | |
| `from math import *` | `sqrt(16)`, `floor(2.7)` 등 전부 | `import java.util.*;` |

- `from math import sqrt`만 했으면 `math.sqrt(16)`은 에러 (`math`라는 이름은 안 가져옴)
- 모듈 = 함수·변수를 모아 둔 **파일 하나**

## 2. math

| 함수 | 무엇을 하나 | 결과 | Java |
|---|---|---|---|
| `math.ceil(2.1)` | 올림 | `3` (**정수**) | `3.0` |
| `math.floor(2.9)` | 내림 | `2` (**정수**) | `2.0` |
| `math.floor(-1.5)` | 수직선 아래쪽 | `-2` | |
| `math.sqrt(16)` | 제곱근 | `4.0` | 같음 |
| `math.pow(2, 3)` | 거듭제곱 | `8.0` | 같음 |
| `math.pi` | 원주율 | `3.141592653589793` | `Math.PI` |
| `math.factorial(5)` | 팩토리얼 | `120` | |
| `math.gcd(12, 18)` | 최대공약수 | `6` | |

## 3. 내장 함수 (import 없이)

| 함수 | 결과 | 주의 |
|---|---|---|
| `abs(-3)`, `max(3, 7)`, `min([4, 1, 8])` | `3`, `7`, `1` | |
| `pow(2, 3)` | `8` | 내장 pow는 **정수** (math.pow는 `8.0`) |
| `round(2.567, 2)` | `2.57` | |
| `round(2.5)` / `round(3.5)` / `round(4.5)` | `2` / `4` / `4` | 정확히 .5면 **가까운 짝수** 쪽 (Java `Math.round(2.5)`는 `3`) |

## 4. random

| 함수 | 범위 | 주의 |
|---|---|---|
| `random.random()` | 0.0 이상 1.0 미만 | |
| `random.randint(1, 3)` | 1, 2, **3** | **끝 포함** (range와 다름) |
| `random.randrange(1, 3)` | 1, 2 | 끝 미포함 (range와 같음) |
| `random.choice([7, 8])` | 하나 고르기 | |
| `random.shuffle(a)` | a 자체를 섞음 | 반환값 None |

## 확인 문제

```python
import math

a = math.ceil(4.2)      # 5
b = math.floor(-1.5)    # -2
c = round(4.5)          # 4
d = math.sqrt(9)        # 3.0
print(a, b, c, d)       # 5 -2 4 3.0
```
