[참조](https://www.froyok.fr/blog/2021-09-ue4-custom-lens-flare/)
- 기존 렌즈 플레어
![[Pasted image 20240404162820.png]]

# 1. Setting Up a Plugin
새 플러그인을 만들어 준다. 다른 설정은 마음대로 해되, Is Engine Plugin은 체크해제 하도록 하자.
![[Pasted image 20240409122416.png]]
여기서 부터 플러그인의 이름을 **CustomPostProcess**로 하여 글을 진행한다.

생성한 플러그인의 **Bulid.cs**파일(위 사진대로면 **CustomPostProcess.Build.cs**)에 아래 include를 추가해 준다.
```cs
PrivateIncludePaths.AddRange(
	new string[] {
		// ... add other private include paths required here ...
		EngineDirectory + "/Source/Runtime/Renderer/Private"
    }
	);
	

PublicDependencyModuleNames.AddRange(
	new string[]
	{
		"Core",
		// ... add other public dependencies that you statically link with here ...
		"RHI",
		"Renderer",
		"RenderCore",
		"Projects"
	}
	);
```

기본으로 생성된 **CustomPostProcess.h**, **CustomPostProcess.cpp**가 있는데, 소스 코드의 함수에 아래 내용을 추가해 준다.
```cpp
void FCustomPostProcessModule::StartupModule()
{
	FString BaseDir = IPluginManager::Get().FindPlugin(TEXT("CustomPostProcess"))->GetBaseDir();
	FString PluginShaderDir = FPaths::Combine(BaseDir, TEXT("Shaders"));
	AddShaderSourceDirectoryMapping(TEXT("/CustomShaders"), PluginShaderDir);
}
```
`StartupModeul()`에서 플러그인 위치를 검색해 새로 생성한 **Shaders**폴더를 추가한다. 그리고 `AddShaderSourceDirectoryMapping()`을 호출해 엔진이 사용자 정의 셰이더 파일을 로드하기위해 어디를 찾아야 하는지 알 수 있도록 심볼릭 경로를 생성한다.

마지막으로 **CustomPostProcess.uplugin**파일에서 모듈 속성을 아래와 같이 설정해 준다.
```json
"Modules": [
	{
		"Name": "CustomPostProcess",
		"Type": "Runtime",
		"LoadingPhase": "PostConfigInit"
	}
]
```

# 2. Prepping Shaders
플러그인 루트폴더에 **Shaders**폴더를 새로 만들어 준다.
![[Pasted image 20240409124620.png]]

렌더링 패스로 통과시킬 커스텀 셰이더파일들을 저장할 폴더다. 아래 파일들을 생성해 준다.
**.USF**
- Chroma.usf
- DownsampleThreshold.usf
- DualKawaseBlur.usf
- Ghosts.usf
- Glare.usf
- Mix.usf
- Halo.usf
- Rescale.usf
- ScreenPass.usf

**.USH**
- Shared.ush

**Shared.ush**에 아래 코드를 넣어준다.
```hlsl
// Not sure if this one is needed, but the engine
// lens-flare shaders have it too.
#define SCENE_TEXTURES_DISABLED 1

#include "/Engine/Public/Platform.ush"
#include "/Engine/Private/Common.ush"
#include "/Engine/Private/ScreenPass.ush"
#include "/Engine/Private/PostProcessCommon.ush"

Texture2D InputTexture;
SamplerState InputSampler;
float2 InputViewportSize;
```
위 코드들은 공용 변수들이며, 모든 패스에서 사용될 편수들이다. 다른 파일은 뒤에 다루도록 한다.

# 3. Data Asset
해당 글에서 렌즈 플레어는 데이터 에셋과 콘솔 변수로 관리된다. 먼저 데이터 에셋부터 설정한다.

**DataAsset**을 상속하는 새로운 클래스를 만들어 준다.
**PostProcessLensFlareAsset.h**
```cpp
// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "PostProcessLensFlareAsset.generated.h"

USTRUCT(BlueprintType)
struct FLensFlareGhostSettings
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exedre")
    FLinearColor Color = FLinearColor::White;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Exedre")
    float Scale = 1.0f;
};

UCLASS()
class CUSTOMPOSTPROCESS_API UPostProcessLensFlareAsset : public UDataAsset
{
	GENERATED_BODY()
public:
    UPROPERTY(EditAnywhere, Category = "General", meta = (UIMin = "0.0", UIMax = "10.0"))
    float Intensity = 1.0f;

    UPROPERTY(EditAnywhere, Category = "General")
    FLinearColor Tint = FLinearColor(1.0f, 0.85f, 0.7f, 1.0f);

    UPROPERTY(EditAnywhere, Category = "General")
    UTexture2D* Gradient = nullptr;


    UPROPERTY(EditAnywhere, Category = "Threshold", meta = (UIMin = "0.0", UIMax = "10.0"))
    float ThresholdLevel = 1.0f;

    UPROPERTY(EditAnywhere, Category = "Threshold", meta = (UIMin = "0.01", UIMax = "10.0"))
    float ThresholdRange = 1.0f;


    UPROPERTY(EditAnywhere, Category = "Ghosts", meta = (UIMin = "0.0", UIMax = "1.0"))
    float GhostIntensity = 1.0f;

    UPROPERTY(EditAnywhere, Category = "Ghosts", meta = (UIMin = "0.0", UIMax = "1.0"))
    float GhostChromaShift = 0.015f;

    UPROPERTY(EditAnywhere, Category = "Ghosts")
    FLensFlareGhostSettings Ghost1 = { FLinearColor(1.0f, 0.8f, 0.4f, 1.0f), -1.5 };

    UPROPERTY(EditAnywhere, Category = "Ghosts")
    FLensFlareGhostSettings Ghost2 = { FLinearColor(1.0f, 1.0f, 0.6f, 1.0f),  2.5 };

    UPROPERTY(EditAnywhere, Category = "Ghosts")
    FLensFlareGhostSettings Ghost3 = { FLinearColor(0.8f, 0.8f, 1.0f, 1.0f), -5.0 };

    UPROPERTY(EditAnywhere, Category = "Ghosts")
    FLensFlareGhostSettings Ghost4 = { FLinearColor(0.5f, 1.0f, 0.4f, 1.0f), 10.0 };

    UPROPERTY(EditAnywhere, Category = "Ghosts")
    FLensFlareGhostSettings Ghost5 = { FLinearColor(0.5f, 0.8f, 1.0f, 1.0f),  0.7 };

    UPROPERTY(EditAnywhere, Category = "Ghosts")
    FLensFlareGhostSettings Ghost6 = { FLinearColor(0.9f, 1.0f, 0.8f, 1.0f), -0.4 };

    UPROPERTY(EditAnywhere, Category = "Ghosts")
    FLensFlareGhostSettings Ghost7 = { FLinearColor(1.0f, 0.8f, 0.4f, 1.0f), -0.2 };

    UPROPERTY(EditAnywhere, Category = "Ghosts")
    FLensFlareGhostSettings Ghost8 = { FLinearColor(0.9f, 0.7f, 0.7f, 1.0f), -0.1 };


    UPROPERTY(EditAnywhere, Category = "Halo", meta = (UIMin = "0.0", UIMax = "1.0"))
    float HaloIntensity = 1.0f;

    UPROPERTY(EditAnywhere, Category = "Halo", meta = (UIMin = "0.0", UIMax = "1.0"))
    float HaloWidth = 0.6f;

    UPROPERTY(EditAnywhere, Category = "Halo", meta = (UIMin = "0.0", UIMax = "1.0"))
    float HaloMask = 0.5f;

    UPROPERTY(EditAnywhere, Category = "Halo", meta = (UIMin = "0.0", UIMax = "1.0"))
    float HaloCompression = 0.65f;

    UPROPERTY(EditAnywhere, Category = "Halo", meta = (UIMin = "0.0", UIMax = "1.0"))
    float HaloChromaShift = 0.015f;


    UPROPERTY(EditAnywhere, Category = "Glare", meta = (UIMin = "0", UIMax = "10"))
    float GlareIntensity = 0.02f;

    UPROPERTY(EditAnywhere, Category = "Glare", meta = (UIMin = "0.01", UIMax = "200"))
    float GlareDivider = 60.0f;

    UPROPERTY(EditAnywhere, Category = "Glare", meta = (UIMin = "0.0", UIMax = "10.0"))
    FVector GlareScale = FVector(1.0f, 1.0f, 1.0f);

    UPROPERTY(EditAnywhere, Category = "Glare")
    FLinearColor GlareTint = FLinearColor(1.0f, 1.0f, 1.0f, 1.0f);

    UPROPERTY(EditAnywhere, Category = "Glare")
    UTexture2D* GlareLineMask = nullptr;
};

```

**PostProcessLensFlares.h**파일에서, `struct FLensFlareInputs`에 새로운 파라미터를 추가해 준다. 이 구조체는 포스트 프로세스 렌더링 단계에서 렌더링 패스 자체로 몇 가지 설정을 전송하는데 사용된다.
```cpp
struct FLensFlareInputs
{
	static const uint32 LensFlareCountMax = 8;

	// [Required] The bloom convolution texture. If enabled, this will be composited with lens flares. Otherwise,
	// a transparent black texture is used instead. Either way, the final output texture will use the this texture
	// descriptor and viewport.
	FScreenPassTexture Bloom;

	// TyT
	// Scene color at half resolution
	FScreenPassTexture HalfSceneTexture;
	
	// [Required] The scene color input, before bloom, which is used as the source of lens flares.
	// This can be a downsampled input based on the desired quality level.
	FScreenPassTexture Flare;
	[...]
}
```

이 구조체 바로 아래에, 새로운 구조체를 만들어 준다.
```cpp
// TyT
struct FLensFlareOutputsData
{
	FRDGTextureRef Texture;
	FIntRect Rect;
};
// TyT
```
이 구조체는 커스텀 코드에서 포스트 프로세스 렌더링 패스로 데이터를 보내는데 사용된다.

그리고 마지막으로 `AddLensFlaresPass()` 함수에 파라미터를 추가해 준다.
```cpp
// Helper function which pulls inputs from the post process settings of the view.
FScreenPassTexture AddLensFlaresPass(
	FRDGBuilder& GraphBuilder,
	const FViewInfo& View,
	FScreenPassTexture Bloom,
	FScreenPassTexture HalfSceneColor,	// TyT
	const FSceneDownsampleChain& SceneDownsampleChain);
```

이제 **PostProcessing.cpp**에서 `AddLensFlaresPass()`를 호출하는 부분을 수정해 준다.
```cpp

```
