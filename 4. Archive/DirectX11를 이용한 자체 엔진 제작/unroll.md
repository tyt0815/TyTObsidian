
```hlsl
[unroll] 
for (int i = 0; i < 4; ++i)
{ // 루프 본문 // ... }
```
위와같이 루프문 위에 작성한다. 이는 컴파일시 루프문을 풀어서 컴파일하는 구문이고, 루프횟수가 상수일때 자원이 많이드는 점프문을 없앨 수 있다. 루프횟수가 상수이며 적을때 사용하자.