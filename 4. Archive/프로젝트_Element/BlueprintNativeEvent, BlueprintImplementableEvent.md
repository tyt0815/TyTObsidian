---
[참고](https://hyo-ue4study.tistory.com/42)
UFUNCTION()구문에 들어갈 수 있는 키워드

# BlueprintNativeEvent
- C++에서 상속 작성 가능
- 상속할시에 함수명_Implementation 을 붙여서 상속및 구현
- **주의할 점으로 UInterface에서 선언할땐 _Implementation함수를 선언하지 않아도 됬는데 UActorComponent에서는 둘다 선언해야 했음. UInterface에서만 예외적인 것 같으니 주의**
# BlueprintImplementableEvent
- 블루프린트에서만 상속 가