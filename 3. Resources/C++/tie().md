---
dg-publish: true
---

# tie()
**Created at : 2023-10-16 11:34**

![[Pasted image 20231016113415.png]]
출처: https://learn.microsoft.com/ko-kr/cpp/standard-library/basic-ios-class?view=msvc-170#tie

마이크로 소프트 공식 문서에 따르면, 한 스트림이 다른 스트림보다 먼저 처리 되도록 한다고 한다. cin과 cout은 기본적으로 tie되어 있는데 이는 cin이 실행되기전 cout이 flush되고, cout이 실행되기 전 cin이 flush됨을 의미한다.
백준 문제 풀이에서 보통 시간을 절약하기 위해 NULL값을 준다.

![[Pasted image 20231016114408.png]]
추가 자료: https://cplusplus.com/reference/ios/ios/tie/

# 관련 글
[sync_with_stdio()](sync_with_stdio().md)