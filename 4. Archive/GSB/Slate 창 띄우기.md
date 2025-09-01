[[4. Archive/GSB/AssetAction 항목 추가하기]]
AssetAction으로 Slate창을 띄워보기로 한다.
```cpp
UCLASS()
class GSBFACILITYEDITORTOOLS_API UGSBFacilityMaterialAssetAction : public UAssetActionUtility
{
	GENERATED_BODY()
public:
	UGSBFacilityMaterialAssetAction();
	
public:
	UFUNCTION(CallInEditor)
	void SetDissolveMaterialFunction();


	/////////////////////////////////////////////////////////////
	// SetDissolveMaterialFunction Slate Tab
	/////////////////////////////////////////////////////////////
private:
	void RegisterSetDissolveMaterialFunctionTab();

	TSharedRef<SDockTab> HandleOnSpawnSetDissolveMaterialFunctionTab(const FSpawnTabArgs& SpawnTabArgs);
};
```


```cpp
UGSBFacilityMaterialAssetAction::UGSBFacilityMaterialAssetAction()
{
	RegisterSetDissolveMaterialFunctionTab();
}

void UGSBFacilityMaterialAssetAction::SetDissolveMaterialFunction()
{
	FGlobalTabmanager::Get()->TryInvokeTab(FName(TEXT("SetDissolveMaterialFunction")));
}

void UGSBFacilityMaterialAssetAction::RegisterSetDissolveMaterialFunctionTab()
{
	FGlobalTabmanager::Get()->RegisterNomadTabSpawner(
		FName("SetDissolveMaterialFunction"), 
		FOnSpawnTab::CreateUObject(this, &UGSBFacilityMaterialAssetAction::HandleOnSpawnSetDissolveMaterialFunctionTab)
	)
		.SetDisplayName(FText::FromString(TEXT("Set Dissolve Material Function")));
}

TSharedRef<SDockTab> UGSBFacilityMaterialAssetAction::HandleOnSpawnSetDissolveMaterialFunctionTab(const FSpawnTabArgs& SpawnTabArgs)
{
	return SNew(SDockTab)
		.TabRole(ETabRole::NomadTab)
		;
}

```

코드를 읽어보면 알다시피, AssetActionUtility의 생성자에서 Slate기반 Tab을 Register하고, AssetAction에서 창을 호출한다.