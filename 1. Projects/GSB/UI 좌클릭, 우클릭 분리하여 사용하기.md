---
dg-publish: true
---

```cpp
virtual FReply NativeOnPreviewMouseButtonDown(const FGeometry& InGeometry, const FPointerEvent& InMouseEvent) override;


if (InMouseEvent.IsMouseButtonDown(EKeys::LeftMouseButton))
{
	OnItemSlotLeftClicked.Broadcast(this);
}
else if (InMouseEvent.IsMouseButtonDown(EKeys::RightMouseButton))
{
	OnItemSlotRightClicked.Broadcast(this);
}
return FReply::Handled();
```

위와 같이 `NativeOnPreviewMouseButtonDown`함수를 오버라이딩 하면 된다. `NativeMouseButtonDown` 함수도 있는데 OnPreview를 사용한 이유는 UButton을 디자인적으로 활용하기 위해서이다. OnPreview 함수는 UButton의 OnClicked 이벤트 이전에 처리되지만, 후자의 함수 경우 OnClicked 이벤트 이후에 처리되며, OnClicked 이벤트가 처리되면 `NativeMouseButtonDown`함수는 호출되지 않게 된다.