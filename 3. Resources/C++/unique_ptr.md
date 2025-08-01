---
dg-publish: true
---

```cpp
#include <memory>
```
단 하나의 포인터만 해당 주소를 가리킬 수 있음.


```cpp
unique_ptr<T> uptr(*T);
// or
unique_ptr<T> uptr = unique_ptr<T>(*T);
// or
T Value;
unique_ptr<T> uptr = make_unique<T>(Value);  
// 이 경우 Value를 유니크 포인터로 만드는 것이 아닌 값만 복사해서 새로운 포인터를 만듦
```
