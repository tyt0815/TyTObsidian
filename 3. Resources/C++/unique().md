---
dg-publish: true
---

# unique() 
**Created at : 2023-10-19 22:05**

`#include <algorithm>`
unique함수는 vector내에 존재하는 중복되는 원소들을 제거해 준다.
```cpp
#include <iostream>
#include <algorithm>
#include <vector>

using namespace std;

int main()
{
    vector<int> a;
    a.resize(5);

    a[0] = a[1] = 1;
    a[2] = 2;
    a[3] = a[4] = 3;

    cout << "### Origin ###" << endl;
    vector<int>::iterator Iter = a.begin();
    for(;Iter != a.end(); ++Iter)
    {
        cout << *Iter << ' ';
    }
    cout << endl << endl;

    cout << "### Apply unique ###" << endl;
    unique(a.begin(), a.end());
    Iter = a.begin();
    for(;Iter != a.end(); ++Iter)
    {
        cout << *Iter << ' ';
    }

    return 0;
}

/*
### Origin ###
1 1 2 3 3

### Apply unique ###
1 2 3 3 3
*/
```
주의 할 점으로는 적용되는 vector가 정렬되어 있어야 한다는 점.
적용된 vector값을 출력한 것을 보면 알지만 중복을 제거하고 없어진 만큼의 부분은 중복값중 임의로 채우는 듯 하다. 
unique함수는 return값으로 중복을 제거하고 난 다음의 Iterator를 반환(위 예제로 치면 2번째 인덱스의 Iterator를 반환)하기 때문에 이를 이용해서 [[vector erase()]]를 같이 사용하면 vector의 사이즈까지 조절 할 수 있다.

# 관련 문서
[[unique()]]
[[18870]]
