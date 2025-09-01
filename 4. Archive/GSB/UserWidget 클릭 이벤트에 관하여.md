# UButton의 OnClicked와 UUserWidget의 MouseButtonDown 이벤트
UButton에 자체적인 OnClicked 델리게이트가 존재하고, UUserWidget은 C++기준으로 
NativeOnPreviewMouseButtonDown, NativeOnMouseButtonDown 함수가 존재한다.
이벤트 호출 순서는 
1. NativeOnPreviewMouseButtonDown
2. OnClicked
3. NativeOnMouseButtonDown
이며, OnClicked가 클릭 이벤트를 가로채기 때문에, OnClicked가 존재하는 경우, 3. NativeOnMouseButtonDown는 실행되지 않는다.
[[4. Archive/GSB/UI 좌클릭, 우클릭 분리하여 사용하기]]


# DragDrop과 ButtonDown, ButtonUp
```cpp
FReply UGSBConstructableFacilitySlot::NativeOnPreviewMouseButtonDown(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent)
{
	Super::NativeOnPreviewMouseButtonDown(InGeometry, InMouseEvent);

	return UWidgetBlueprintLibrary::DetectDragIfPressed(InMouseEvent, this, EKeys::LeftMouseButton).NativeReply;
}
```

위 함수와 같이 작성하면 드래그 이벤트를 호출할 수 있다. `NativeOnDragDetected`함수가 호출이 가능해지는데, 이때 드래그 없이 클릭만 하면 호출되지 않는다.

드래그 없이 클릭만 했을때, `NativeOnMouseButtonUp`이 호출되는데 반대로 드래그가 호출된 경우 이 버튼 업 함수는 호출되지 않는다. 대신 `NativeOnDrop`이 호출된다.
