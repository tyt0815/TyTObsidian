에이펙스 레전드의 호라이즌의 스킬 Q(중력리프트) 와 비슷하게 구현하고 싶었다.

# AddForce 함수
AddForce만 사용해 구현하여 위로 상승하게 하는 경우, 말 그대로 힘을 가하는 경우이기 때문에 속력을 일정하게 유지할 수 없다. 즉 계속해서 가속해 속도가 올라가다 가장 위에서 멈추지 못하고 튕겨져 나가게 된다.

# CharacterMovementComponent의 Velocity
Velocity는 FVector형식의 멤버변수인데 Get, Set을 통하여 접근하지않고 바로 접근(public)이 가능하다. 다만 이 변수를 직접적으로 변경하게 될 경우, Z축 의 경우 중력 영향인지 바로 움직이지 않는다. 즉 이미 Z축방향으로 운동중인 경우에만 설정한 Velocity에 맞게 속력이 나오게 된다. 따라서 AddForce와 조합해서 사용하기로 했다.

```cpp
void ATornado::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	InitActorsToIgnore();
	while (true)
	{
		FHitResult HitResult;
		BoxTrace(HitResult);
		if (HitResult.GetActor() == nullptr) break;
		if (HitResult.GetActor() == GetOwner())
		{
			ACharacter* Character = Cast<ACharacter>(HitResult.GetActor());
			if (Character)
			{
				if (!IsTopLocation(Character))
				{
					if (Character->GetCharacterMovement()->Velocity.Z < 1)
						Character->GetCharacterMovement()->AddForce(FVector::ZAxisVector * 100000.0f); // 대략적으로 캐릭터가 Z방향으로 움직이게 하는 최소 힘이 100000정도 됨
					Character->GetCharacterMovement()->Velocity.Z = UpSpeed;
				}
				else
					Character->GetCharacterMovement()->Velocity.Z = TopSpeed;
			}
		}
	}
}
```
