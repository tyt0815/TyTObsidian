---
# priority_queue 
**Created at : 2023-10-24 13:48**

```cpp
#include <queue>
priority_queue<int> MaxHeap;
```

priority_queue는 힙을 구현해 놓았다. 기본 Maxheap이고 MinHeap을 사용하려면 아래와 같이 추가 인자를 전달할 필요가 있다.
```cpp
priority_queue<int, vector<int>, greater<int>> MinHeap;
```

