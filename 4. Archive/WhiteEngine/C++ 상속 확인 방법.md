---
클래스 A, B가 있을때 B가 A를 상속했는지 확인하는 방법
```cpp
#include <type_traits>
std::is_base_of<A, B>::value
```
B가 A를 상속했을 경우1을 리턴하고 아닐 경우 0을 리턴한다.