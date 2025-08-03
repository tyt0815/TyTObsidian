---
기본적으로 C++로 ActorComponent를 만들면 블루프린트에서 상속할 수 없다.
아래는 기본 `UCLASS`다
```
UCLASS(ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
```

아래와 같이 `Blueprintable`메타지정자를 추가해 준다.
```
UCLASS(Blueprintable,  ClassGroup=(Custom), meta=(BlueprintSpawnableComponent) )
```