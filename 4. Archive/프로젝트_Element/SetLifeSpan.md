---
AActor클래스의 함수.
설정된 시간 이후 자동으로 Destroy해줌.
```cpp
void AActor::SetLifeSpan( float InLifespan )
{
	// Store the new value
	InitialLifeSpan = InLifespan;
	// Initialize a timer for the actors lifespan if there is one. Otherwise clear any existing timer
	if ((GetLocalRole() == ROLE_Authority || GetTearOff()) && IsValidChecked(this) && GetWorld())
	{
		if( InLifespan > 0.0f)
		{
			GetWorldTimerManager().SetTimer( TimerHandle_LifeSpanExpired, this, &AActor::LifeSpanExpired, InLifespan );
		}
		else
		{
			GetWorldTimerManager().ClearTimer( TimerHandle_LifeSpanExpired );		
		}
	}
}
```

EndMagicAfter라는 함수로 SetLifeSpan과 같은 기능을 하는 함수를 만들었었는데, 모두 교체
