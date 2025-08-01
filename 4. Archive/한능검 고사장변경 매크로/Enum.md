---
dg-publish: true
---

# 기본 사용법
```python
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

# 사용 예시
print(Color.RED)          # Color.RED
print(Color.RED.name)     # 'RED'
print(Color.RED.value)    # 1

# 비교
if Color.RED == Color.GREEN:
    print("같다")
else:
    print("다르다")  # 출력: 다르다

```

# 자동 값 생성
```python 
from enum import Enum, auto

class Status(Enum):
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()

print(Status.PENDING.value)  # 1
print(Status.RUNNING.value)  # 2

```
