# 05 · lambda, map, filter, enumerate, zip

> 이 주제는 확인 문제를 한 번에 맞혀서 deep-dive 기록이 없다.

## 1. lambda: def의 한 줄 버전

```python
def f(x):
    return x * 2

f = lambda x: x * 2        # 위와 같음
print(f(3))                # 6

add = lambda a, b: a + b
print(add(2, 5))           # 7
```
| 부분 | 뜻 |
|---|---|
| `lambda` | 함수를 만든다 |
| 콜론 앞 | 매개변수 |
| 콜론 뒤 | **반환값** (return 자동) |

Java의 `x -> x * 2`와 같다.

## 2. map / filter

```python
print(list(map(lambda x: x + 1, [1, 2, 3])))          # [2, 3, 4]
print(list(map(int, ['1', '2', '3'])))                # [1, 2, 3]
print(list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4])))   # [2, 4]
print(list(map(lambda x, y: x * y, [1, 2, 3], [4, 5, 6])))  # [4, 10, 18]
```
| | 결과 개수 | 결과 값 | 컴프리헨션으로 쓰면 |
|---|---|---|---|
| `map(함수, 리스트)` | 같음 | 함수를 적용한 **새 값** | `[x + 1 for x in a]` |
| `filter(조건, 리스트)` | 같거나 줄어듦 | **원래 값 그대로** | `[x for x in a if 조건]` |

- `print(map(...))`만 하면 `<map object at 0x...>`가 나온다 → **`list()`로 감싸기**
- lambda 대신 **함수 이름**을 넣으면 원소마다 그 함수를 한 번씩 부른다

| 코드 | 원소마다 하는 일 | 결과 |
|---|---|---|
| `list(map(str, [1, 2]))` | `str(1)`, `str(2)` | `['1', '2']` (문자열이라 따옴표) |
| `list(map(int, ["3", "4"]))` | `int("3")`, `int("4")` | `[3, 4]` |
| `list(map(len, ["ab", "cde"]))` | `len("ab")`, `len("cde")` | `[2, 3]` |
| `list(map(int, "1 2 3".split()))` | 잘라서 정수로 | `[1, 2, 3]` |
- 괄호가 겹치면 **가장 안쪽부터**

```python
print(sum(map(lambda x: x * x, filter(lambda x: x > 1, [1, 2, 3]))))
# filter → [2, 3], map → [4, 9], sum → 13
```

## 3. enumerate: 번호 붙이기

```python
for i, v in enumerate(['a', 'b', 'c']):
    print(i, v, end=" / ")          # 0 a / 1 b / 2 c /
print()
for i, v in enumerate(['a', 'b'], 1):
    print(i, v, end=" / ")          # 1 a / 2 b /   (시작 번호 1)
```

## 4. zip: 같은 위치끼리 짝

```python
for x, y in zip([1, 2, 3], ['a', 'b']):
    print(x, y, end=" / ")          # 1 a / 2 b /   (짧은 쪽에 맞춰 끝)
print()
print(list(zip([1, 2], [3, 4])))    # [(1, 3), (2, 4)]
```

## 5. sorted의 key

```python
words = ['bb', 'a', 'ccc']
print(sorted(words, key=len))                   # ['a', 'bb', 'ccc']
print(sorted(words, key=lambda w: -len(w)))     # ['ccc', 'bb', 'a']
```

## 확인 문제

```python
nums = [3, 8, 5, 10]
a = list(filter(lambda x: x > 4, nums))   # [8, 5, 10]
b = list(map(lambda x: x // 2, a))        # [4, 2, 5]
for i, v in enumerate(b, 1):
    print(i, v, end=" ")
# 1 4 2 2 3 5
```
