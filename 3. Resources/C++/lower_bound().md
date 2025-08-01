---
dg-publish: true
---

# lower_bound() 
**Created at : 2023-10-19 22:33**

입력된 값보다 크거나 같은 숫자가 배열에서 처음 등장하는 위치를 반환. 오름차순 정렬이 되어 있어야 한다.

```cpp
#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

int main() {

	vector<int> arr = { 1,2,3,4,5,6,6,6 };
	cout << "lower_bound(6) : " << lower_bound(arr.begin(), arr.end(), 6) - arr.begin() << endl;

	return 0;
}

/*
lower_bound(6) : 5
*/
```


# 관련 문서
[[upper_bound()]]
[[18870]]
