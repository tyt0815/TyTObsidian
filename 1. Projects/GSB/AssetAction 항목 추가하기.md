---
![[Attachments/Pasted image 20250720171030.png]]
AssetAction은 위 사진과 같이 에셋을 우클릭해서 나온 컨텍스트 메뉴의 엔트리를 추가하는 방법이다.

![[Attachments/Pasted image 20250720171117.png]]
UAssetActionUtility를 상속한 클래스를 만들어 준다.

```cpp
// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "AssetActionUtility.h"
#include "GSBFacilityMaterialAssetAction.generated.h"

/**
 * 
 */
UCLASS()
class GSBFACILITYEDITORTOOLS_API UGSBFacilityMaterialAssetAction : public UAssetActionUtility
{
	GENERATED_BODY()
	
public:
	UFUNCTION(CallInEditor)
	void SetDissolveMaterialFunction();
};

```
위 코드의 함수 선언부분을 주목하자.
```cpp
UFUNCTION(CallInEditor)
	void SetDissolveMaterialFunction();
```
이와 같이 선언하면 항목을 추가할 수 있다. 그리고 함수를 구현하면 된다.
