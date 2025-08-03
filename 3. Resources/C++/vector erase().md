---
# vector erase() 
**Created at : 2023-10-19 22:23**

vector의 erase 메소드주어진 구간의 값을 삭제해 준다.

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

    cout << "### Apply erase ###" << endl;
    a.erase((++a.begin()), a.end());
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

### Apply erase ###
1
*/
```

`a.erase((++a.begin()), a.end());`
이 부분은 1번째 인덱스부터 마지막 인덱스까지 삭제하게 만들었다. 이 부분을 [[unique()]]와 같이 적용하면 unique한 부분만 남기고 나머지는 삭제 할 수 있다.

# 관련 문서
[[unique()]]
[[18870]]

