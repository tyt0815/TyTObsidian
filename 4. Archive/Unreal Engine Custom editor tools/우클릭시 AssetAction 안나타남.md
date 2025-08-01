---
dg-publish: true
---

```cpp
class SUPERMANAGER_API UQuickAssetAction : public UAssetActionUtility
{
	GENERATED_BODY()
	
public:
	UFUNCTION(CallInEditor)
	void TestFunc();
};

```

위와 같이 UAssetActionUtility을 상속한 클래스에 UFUNCTION(CallInEditor)함수를 만들면 에셋을 우클릭하면 DuplicateAssets함수가 나타나야 하는데 안나타날 수 있다.
![[Attachments/Pasted image 20250527110454.png]]

우클릭했는데 다음과 같은 메뉴가 나타나지 않는다면 UQuickAssetAction를 상속하는 블루프린트를 만들어 주면 나타나게 된다.
![[Attachments/Pasted image 20250527110541.png]]
