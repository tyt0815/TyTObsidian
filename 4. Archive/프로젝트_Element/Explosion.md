- [x] 버그픽스: SetTimer 동작 안함 ✅ 2024-02-25
# 문제
```cpp
void AExplosion::BeginBoxOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	...
	FTimerHandle ExplosionTimer;
	GetWorldTimerManager().SetTimer(ExplosionTimer, this, &AExplosion::Explosion, ExplosionDelay);
}
```

위와 같이 BoxOverlap이벤트에 SetTimer가 설정되어 있는데, 액터가 생성된 직후 Overlap이벤트가 발생하면 SetTimer가 제대로 설정되지 않는다.(생성된 직후가 아니면 제대로 작동함.)

# 원인
이유는 구조적인 문제였다. Explosion액터가 생성 -> Delay값 설정 -> Overlap 순서로 설계했는데 생성된 직후에는 Overlap -> Delay값 설정순으로 실행되었다.

# 해결
구조 수정