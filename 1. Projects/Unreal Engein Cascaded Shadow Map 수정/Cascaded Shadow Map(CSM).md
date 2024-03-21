- SceneManagement.h
```cpp
// 952번째 줄
class FShadowCascadeSettings
{
	public:
	// The following 3 floats represent the view space depth of the split planes for this cascade.
	// SplitNear <= FadePlane <= SplitFar

	// The distance from the camera to the near split plane, in world units (linear).
	float SplitNear;

	// The distance from the camera to the far split plane, in world units (linear).
	float SplitFar;

	// in world units (linear).
	float SplitNearFadeRegion;

	// in world units (linear).
	float SplitFarFadeRegion;
	...
}
```
해당 코드를 보면 언리얼 엔진은 3케스케이디드 섀도우 맵임을 알 수 있다. 이부분을 아래 영상을 참고하여 8 케스케이디드로 수정해 본다.
[유나이트 서울 2020 - 원신 콘솔 플랫폼 개발 경험 및 렌더링 파이프라인 기술 소개 Track3-1](https://www.youtube.com/watch?v=00QugD5u1CU&list=PLh5wglWuOGseWAY_9bTjJvvLvtapUW_Sj&index=1&t=753s)

수정해야 하는 부분 목록
```
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Private\Components\DirectionalLightComponent.cpp(946): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[188/3952] Compile [x64] Module.Renderer.18.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[189/3952] Compile [x64] Module.Renderer.19.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[190/3952] Compile [x64] Module.Kismet.5.cpp
1>[191/3952] Compile [x64] Module.Renderer.22.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.cpp(998): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.cpp(1408): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.cpp(1408): error C2660: 'SetDepthBoundsTest': 함수는 3개의 인수를 사용하지 않습니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\RHI\Public\RHIUtilities.h(615): note: 'SetDepthBoundsTest' 선언을 참조하십시오.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.cpp(1408): note: 인수 목록 '(FRHICommandList, const float, const FMatrix)'을(를) 일치시키는 동안
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowSetup.cpp(4252): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowSetup.cpp(4300): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\SceneOcclusion.cpp(611): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\SceneOcclusion.cpp(611): error C2737: 'SplitNear': const 개체를 초기화해야 합니다
1>[196/3952] Compile [x64] Module.Renderer.9.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\Lumen\LumenSceneDirectLighting.cpp(887): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[197/3952] Compile [x64] Module.Renderer.3.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\DistanceFieldShadowing.cpp(798): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\DistanceFieldShadowing.cpp(1048): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\DistanceFieldShadowing.cpp(1116): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\DistanceFieldShadowing.cpp(1116): error C2660: 'SetDepthBoundsTest': 함수는 3개의 인수를 사용하지 않습니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\RHI\Public\RHIUtilities.h(615): note: 'SetDepthBoundsTest' 선언을 참조하십시오.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\DistanceFieldShadowing.cpp(1116): note: 인수 목록 '(FRHICommandList, float, const FMatrix)'을(를) 일치시키는 동안
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\DistanceFieldShadowing.cpp(1158): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\DistanceFieldShadowing.cpp(1158): error C2660: 'SetDepthBoundsTest': 함수는 3개의 인수를 사용하지 않습니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\RHI\Public\RHIUtilities.h(615): note: 'SetDepthBoundsTest' 선언을 참조하십시오.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\DistanceFieldShadowing.cpp(1158): note: 인수 목록 '(FRHICommandList, float, const FMatrix)'을(를) 일치시키는 동안
1>[198/3952] Compile [x64] Module.Renderer.23.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowSetupMobile.cpp(445): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[199/3952] Compile [x64] Module.Renderer.16.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[200/3952] Compile [x64] Module.MovieSceneTracks.3.cpp
1>[201/3952] Compile [x64] Module.Renderer.27.cpp
1>[202/3952] Compile [x64] Module.Renderer.4.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[203/3952] Compile [x64] Module.Renderer.11.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[204/3952] Compile [x64] Module.MovieSceneTracks.2.cpp
1>[205/3952] Compile [x64] Module.Renderer.10.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[206/3952] Compile [x64] Module.Renderer.25.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[207/3952] Compile [x64] Module.Renderer.21.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[208/3952] Compile [x64] Module.Renderer.14.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[209/3952] Compile [x64] Module.Renderer.12.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[210/3952] Compile [x64] Module.Renderer.24.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[211/3952] Compile [x64] Module.Renderer.8.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[212/3952] Compile [x64] Module.Renderer.5.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[213/3952] Compile [x64] Module.Renderer.6.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[214/3952] Compile [x64] Module.Renderer.7.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[215/3952] Compile [x64] Module.Renderer.15.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[216/3952] Compile [x64] Module.Renderer.26.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[217/3952] Compile [x64] Module.Renderer.13.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
1>[218/3952] Compile [x64] Module.Renderer.2.cpp
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Renderer\Private\ShadowRendering.h(1138): error C2039: 'SplitNear': 'FShadowCascadeSettings'의 멤버가 아닙니다.
1>C:\Users\user\Documents\TyT\UnrealEngine\5.3.2\Engine\Source\Runtime\Engine\Public\LightSceneProxy.h(19): note: 'FShadowCascadeSettings' 선언을 참조하십시오.
```

# 참조
[New shading models and changing the GBuffer](https://dev.epicgames.com/community/learning/tutorials/2R5x/unreal-engine-new-shading-models-and-changing-the-gbuffer)
