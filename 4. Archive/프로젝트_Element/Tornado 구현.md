---
dg-publish: true
---

에이펙스 레전드의 호라이즌의 스킬 Q(중력리프트) 와 비슷하게 구현하고 싶었다.

# 수정
## 1.2
1.0버전과 같이 AddForce를 통해 구현했다. 1.1의 경우 Tornado가 겹쳐있을때 버그가 발생하기 쉽고, 고치기 는 번거로워 AddForce를 통해 구현한다.
```cpp
void ATornado::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	TArray<AActor*> FlyActorsToIgnore;
	while (true)
	{
		FHitResult HitResult;
		BoxTrace(HitResult, FlyActorsToIgnore);
		if (HitResult.GetActor() == nullptr) break;
		if (HitResult.GetActor() == GetOwner())
		{
			ACharacter* Character = Cast<ACharacter>(HitResult.GetActor());
			if (Character)
			{
				Character->GetCharacterMovement()->Velocity.Z = UpSpeed;
			}
		}
	}
}

void ATornado::BeginBoxOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	ACharacter* Character = Cast<ACharacter>(OtherActor);
	if (Character)
	{
		Character->GetCharacterMovement()->AddForce(10000000.0f * FVector::ZAxisVector);
	}
}
```
## 1.1
### SetMovementMode
아래 방법과 달리 CharacterMovementComponent의 SetMovementMode를 통해 Fly모드로 만들어 구현하는 방식으로 변경. Tornado에 오버랩 될때 Fly로 바꾸고, 오버랩에서 빠져나올때 Walking으로 되돌려 준다.
```cpp
void ATornado::Tick(float DeltaTime)
{
	Super::Tick(DeltaTime);

	TArray<AActor*> FlyActorsToIgnore;
	while (true)
	{
		FHitResult HitResult;
		BoxTrace(HitResult, FlyActorsToIgnore);
		if (HitResult.GetActor() == nullptr) break;
		if (HitResult.GetActor() == GetOwner())
		{
			ACharacter* Character = Cast<ACharacter>(HitResult.GetActor());
			if (Character)
			{
				UCharacterMovementComponent* MovementComponent = Character->GetCharacterMovement();
				if (MovementComponent)
				{
					if (!IsTopLocation(Character))
					{
						MovementComponent->AddInputVector(FVector::ZAxisVector);
					}
					else
					{
						MovementComponent->Velocity.Z = 0.0f;
					}
				}
			}
		}
	}
}

void ATornado::BeginBoxOverlapExec(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex, bool bFromSweep, const FHitResult& SweepResult)
{
	ACharacter* Character = Cast<ACharacter>(OtherActor);
	if (Character)
	{
		UCharacterMovementComponent* MovementComponent = Character->GetCharacterMovement();
		if (MovementComponent)
		{
			MovementComponent->SetMovementMode(EMovementMode::MOVE_Flying);
		}
	}
}

void ATornado::EndBoxOverlap(UPrimitiveComponent* OverlappedComponent, AActor* OtherActor, UPrimitiveComponent* OtherComp, int32 OtherBodyIndex)
{
	ACharacter* Character = Cast<ACharacter>(OtherActor);
	if (Character)
	{
		UCharacterMovementComponent* MovementComponent = Character->GetCharacterMovement();
		if (MovementComponent)
		{
			MovementComponent->SetMovementMode(EMovementMode::MOVE_Walking);
			if (IsTopLocation(Character))
			{
				MovementComponent->AddForce(UpForce * 10000000.0f * FVector::ZAxisVector);
			}
		}
	}
}
```

## 1.0
### AddForce 함수
AddForce만 사용해 구현하여 위로 상승하게 하는 경우, 말 그대로 힘을 가하는 경우이기 때문에 속력을 일정하게 유지할 수 없다. 즉 계속해서 가속해 속도가 올라가다 가장 위에서 멈추지 못하고 튕겨져 나가게 된다.

### CharacterMovementComponent의 Velocity
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
