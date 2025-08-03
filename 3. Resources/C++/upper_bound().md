---
# upper_bound() 
**Created at : 2023-10-19 22:37**

입력된 값을 초과하는 숫자가 배열에서 처음 등장하는 위치를 반환. 오름차순 정렬이 되어 있어야 한다.

```cpp
#include <iostream>

#include <algorithm>

#include <vector>

using namespace std;

  

int main() {

  

    vector<int> arr = { 1,2,3,4,5,6 };

    cout << "upper_bound(3) : " << upper_bound(arr.begin(), arr.end(), 3) - arr.begin();

  
  

    return 0;

}

  

/*

upper_bound(3) : 3

*/
```

# 관련 문서
[[lower_bound()]]