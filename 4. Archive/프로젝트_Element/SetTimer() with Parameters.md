	도트힐(HOT)를 구현하기 위해서 딜레이를 갖고 재귀하는 함수를 만들었다. 

함수를 바인딩 하기 위해 함수 UFUNCTION으로 만들어 준다
```cpp
UFUNCTION()
void HealOverTimeCharacter(float Value, int Count, float Delay);
```

아래와 같이 핸들러와 델리게이트를 선언해서 사용하면 된다.
```cpp
void ABaseCharacter::HealOverTimeCharacter(float Value, int Count, float Delay)
{
	if (Count == 0) return;
	HealCharacter(Value);

	FTimerHandle HealHandler;
	FTimerDelegate HOTDelegate;
	HOTDelegate.BindUFunction(this, FName("HealOverTimeCharacter"), Value, Count - 1, Delay);
	GetWorldTimerManager().SetTimer(HealHandler, HOTDelegate, Delay, false);
}[]()
```