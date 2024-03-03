```cpp
    vector<bool> PrimeNumbers(MAXN , true);
    PrimeNumbers[0] = PrimeNumbers[1] = false;
    for(int i = 2; i * i < MAXN; ++i)
    {
        if(PrimeNumbers[i])
        {
            for(int j = i; i * j < MAXN; ++j) PrimeNumbers[i * j] = false;
        }
    }
```
 자꾸 구현해놓고 맞는지 헷갈려서 확인용으로 기록.