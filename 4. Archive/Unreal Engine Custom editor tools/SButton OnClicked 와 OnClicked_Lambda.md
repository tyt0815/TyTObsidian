현재 보는 강의와 버전 차이때문인지는 몰라도 같은 방식으로 사용하면 컴파일이 안된다.

```cpp
FReply SMyClass::OnButtonClicked(int Param);
```

```cpp
SNew(SButton)
.OnClicked(this, &SMyClass::OnButtonClicked, Param);     // 컴파일 x
```

아래와 같이 람다를 사용하여 우회해 주자

```cpp
SNew(SButton)
.OnClicked_Lambda([this, Param]()
	{
		return OnButtonClicked(Param);
	}
);
```

참고삼아 OnClicked의 정의를 살펴보자면 언리얼 엔진 5.5.4기준
```cpp
// SButton.h Line 77

/** Called when the button is clicked */
SLATE_EVENT( FOnClicked, OnClicked )
```

이고 `FOnClicked`는 
```cpp
// SlateDelegates.h Line 19

/**
 * A delegate that is invoked when widgets want to notify a user that they have been clicked.
 * Intended for use by buttons and other button-like widgets.
 */
DECLARE_DELEGATE_RetVal( 
	FReply, 
	FOnClicked )
```
로 원래 FOnClicked의 경우 파라미터를 받지 않고 FReply를 반환하는 델리게이트임을 알 수 있다.