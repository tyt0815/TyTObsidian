---
``` c++
#define M(x) void Token##x();

M(Pasting)
```

위와 같이 매크로를 정의하면 아래와 같은 함수가 생기게 된다.

```c++
void TokenPasting();
```
