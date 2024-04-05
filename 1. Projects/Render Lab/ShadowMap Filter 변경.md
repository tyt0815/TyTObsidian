**ShadowRendering.cpp**에서 콘솔 변수를 추가해 준다.
```cpp
static TAutoConsoleVariable<int32> CVarFilterMethod(
	TEXT("r.Shadow.FilterMethod"),
	0,
	TEXT("Chooses the shadow filtering method.\n")
	TEXT(" 0: Uniform PCF (default)\n")
	TEXT(" 1: PCSS (experimental)\n")
	TEXT(" 2: TyT Custom Filter\n"),	// TyT
	ECVF_RenderThreadSafe);
```
