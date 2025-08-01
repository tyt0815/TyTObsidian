---
dg-publish: true
---

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

**ShadowRendering.h**에 새로운 셰이더 파라미터 바인딩 클래스를 만들어 준다. 
`class TShadowProjectionPS`클래스를 그대로 복사하여 새로운 클래스를 만들어 아래 `ModifyCompilationEnvironment()`함수에만 새 코드를 추가해 준다.
```cpp
static void ModifyCompilationEnvironment(const FGlobalShaderPermutationParameters& Parameters, FShaderCompilerEnvironment& OutEnvironment)
{
	FShadowProjectionPixelShaderInterface::ModifyCompilationEnvironment(Parameters, OutEnvironment);
	OutEnvironment.SetDefine(TEXT("SHADOW_QUALITY"), Quality);
	OutEnvironment.SetDefine(TEXT("SUBPIXEL_SHADOW"), (uint32)(SubPixelShadow ? 1 : 0));
	OutEnvironment.SetDefine(TEXT("USE_FADE_PLANE"), (uint32)(bUseFadePlane ? 1 : 0));
	OutEnvironment.SetDefine(TEXT("USE_TRANSMISSION"), (uint32)(bUseTransmission ? 1 : 0));
	OutEnvironment.SetDefine(TEXT("USE_CUSTOM_FILTER"), 1);	// TyT

	const bool bMobileForceDepthRead = MobileUsesFullDepthPrepass(Parameters.Platform);
	OutEnvironment.SetDefine(TEXT("FORCE_DEPTH_TEXTURE_READS"), (uint32)(bMobileForceDepthRead ? 1 : 0));
}
```
