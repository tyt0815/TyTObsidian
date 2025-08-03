---
```cpp
UFUNCTION(BlueprintNativeEvent, BlueprintCallable, Category = Trigger)
void Trigger(AActor* TriggeringActor, UPARAM(ref) TArray<AActor*>& TriggerTargets);
virtual void Trigger_Implementation(AActor* TriggeringActor, TArray<AActor*>& TriggerTargets);
```
위에 보이는 것 처럼 `UPARAM(ref)` 을 레퍼런스 앞에 선언해 주면 된다. BlueprintNativeEvent의 경우 Implementation함수에는 `UPARAM(ref)` 을 선언하지 않아도 된다.(하면 안되는지는 아직 모름)