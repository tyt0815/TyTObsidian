[[InteractiveActor]] 와 TriggerActor, ReactToTriggerActor를 인터페이스로 구현하면서 알아낸것
# 1. 인터페이스지만 함수구현 가능
C++은 인터페이스를 지원하지 않지만, pure함수 등을 이용하며 클래스를 다중상속해 인터페이스처럼 사용할 수 있다. 언리얼 인터페이스는 인터페이스클래스를 따로 사용하지만, 어차피 C++클래스를 상속하는 것 이기 때문에 몇가지를 제외하면 클래스 상속하듯 사용할 수 있다.
1. **UFUNCTION()** 은 **BlueprintImplementableEvent** or **BlueprintNativeEvent** 만 사용할 수 있다. 일반 함수는 제약없음
2. 코드에서 함수를 구현하려면 **BlueprintNativeEvent** 가 선언된 **UFUNCTION()** 함수의 **Implementation** 함수로 구현해야 한다.
3. **UPROPERTY()** 는 사용 불가능

# 2. 인터페이스 함수 호출
[언리얼엔진 공식문서: 인터페이스](https://docs.unrealengine.com/5.3/ko/interfaces-in-unreal-engine/)

해당 페이지의 가장 아래쪽에 보면 아래와 같은 코드가 있다.
```cpp
    bool bIsImplemented = OriginalObject->GetClass()->
	    ImplementsInterface(UReactToTriggerInterface::StaticClass()); 

    bIsImplemented = OriginalObject->Implements<UReactToTriggerInterface>(); 

    IReactToTriggerInterface* ReactingObjectA = 
	    Cast<IReactToTriggerInterface>(OriginalObject); 
```
이중 세번째 코드인 객체를 인터페이스로 캐스팅하는 경우, 블루프린트가 직접 인터페이스를 상속한 객체는 nullptr을 반환하게 된다. 따라서 `UReactToTriggerInterface`를 사용하는 코드를 사용할 수 있도록 하자. 그렇게 되면 자동적으로 함수 호출은 아래와 같이 하게 된다.
```cpp
IReactToTriggerInterface::Execute_ReactToTrigger(OriginalObject);
```
