[참조](https://www.froyok.fr/blog/2021-09-ue4-custom-lens-flare/)
![[프로젝트 환경]]
- 기존 렌즈 플레어
![[Pasted image 20240404162820.png]]


# Overview of the Custom Lens Flare Pass
![[Pasted image 20240415191738.png]]
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

# 4. 엔진 렌더링 패스 수정
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
if (bLensFlareEnabled)
{	
	Bloom = AddLensFlaresPass(GraphBuilder, View, Bloom, HalfResSceneColor, *LensFlareSceneDownsampleChain);	// TyT
}
```

**PostProcessLensFlares.cpp**의 최상단부 `#include` 밑에, 아래 코드를 추가해 delegate를 선언해 준다.
```cpp
// TyT
DECLARE_MULTICAST_DELEGATE_FourParams(FPP_LensFlares, FRDGBuilder&, const FViewInfo&, const FLensFlareInputs&, FLensFlareOutputsData&);
RENDERER_API FPP_LensFlares PP_LensFlares;
// TyT
```

비교를 용의하게 하기 위해, 콘솔 변수를 추가해 이전 버전의 렌즈 플레어와 커스텀 렌즈 플레어를 변환 가능하게 설정한다.
```cpp
TAutoConsoleVariable<int32> CVarLensFlareQuality(
	TEXT("r.LensFlareQuality"),
	2,
	TEXT(" 0: off but best for performance\n")
	TEXT(" 1: low quality with good performance\n")
	TEXT(" 2: good quality (default)\n")
	TEXT(" 3: very good quality but bad performance"),
	ECVF_Scalability | ECVF_RenderThreadSafe);

// TyT
// Console var to switch between the lens-flare methods
TAutoConsoleVariable<int32> CVarLensFlareMethod(
	TEXT("r.LensFlareMethod"),
	1,
	TEXT(" 0: Original lens-flare method\n")
	TEXT(" 1: Custom lens-flare method"),
	ECVF_RenderThreadSafe);
// TyT
```

파일의 하단부에 `AddLensFlaresPass()` 함수에 파라미터를 추가해 주고, 함수를 수정해 준다.
```cpp
FScreenPassTexture AddLensFlaresPass(
	FRDGBuilder& GraphBuilder,
	const FViewInfo& View,
	FScreenPassTexture Bloom,
	FScreenPassTextureInput HalfSceneColor,		// TyT
	const FSceneDownsampleChain& SceneDownsampleChain)
{
	[...]
	
	FLensFlareInputs LensFlareInputs;
	LensFlareInputs.Bloom = Bloom;
	LensFlareInputs.HalfSceneColor = HalfSceneColor;	// TyT
	LensFlareInputs.Flare = SceneDownsampleChain.GetTexture(LensFlareDownsampleStageIndex);
	
	[...]

	// If a bloom output texture isn't available, substitute the half resolution scene color instead, but disable bloom
	// composition. The pass needs a primary input in order to access the image descriptor and viewport for output.
	if (!Bloom.IsValid())
	{
		LensFlareInputs.Bloom = SceneDownsampleChain.GetFirstTexture();
		LensFlareInputs.bCompositeWithBloom = false;
	}
	
	// TyT
	int32 UseCustomFlare = CVarLensFlareMethod.GetValueOnRenderThread();
	
	FLensFlareOutputsData Outputs;
	Outputs.Texture = nullptr;
	Outputs.Rect = FIntRect(0, 0, 0, 0);
	
	if (UseCustomFlare != 0)
	{
		PP_LensFlares.Broadcast(GraphBuilder, View, LensFlareInputs, Outputs);
	}
	
	if (UseCustomFlare == 0 || Outputs.Texture == nullptr)
	{
		return AddLensFlaresPass(GraphBuilder, View, LensFlareInputs);
	}
	else
	{
		return FScreenPassTexture(Outputs.Texture, Outputs.Rect);
	}
	//return AddLensFlaresPass(GraphBuilder, View, LensFlareInputs);
	// TyT
```
위 코드는 다음과 같은 일을 한다.
- cvar value를 얻는다.(콘솔 변수)
- 렌즈 플레어 패스 결과를 위한 구조체를 생성한다.
- cvar이 0이 아니면, 델리게이트에 연결된 함수를 실행하도록 요청한다.
- cvar이 0이거나 델리게이트에서 invalid한 값이 return되면, 기존 렌즈 플레어 패스를 실행한다.
- 그 외에는 커스텀 렌즈 플레어 패스의 결과를 기반으로 특수한 텍스처를 반환한다.


==디버그 목적으로 이전 버전과 커스텀 버전을 둘다 가능하게 만들었지만, 사용되지도 않는 셰이더 컴파일 등 최적화에 문제가 있으니 기존 버전을 제거하는 것이 도움이 될 수도 있음==

# 5. Custom Subsystem
서브시스템은 엔진 자체에서 관리되는 싱글톤으로, 게임 코드 어디서든 쉽게 검색이 가능함. 그중 엔진 서브시스템은 엔진이 시작되고 종료될 때 함께 시작되고 중지된다.

플러그인에서 EngineSubsystem을 상속하는 새 클래스를 만든다.
**PostProcessSubsystem.h**
```cpp
#pragma once

#include "CoreMinimal.h"
#include "Subsystems/EngineSubsystem.h"
#include "PostProcess/PostProcessLensFlares.h"
#include "PostProcessSubsystem.generated.h"

DECLARE_MULTICAST_DELEGATE_FourParams(FPP_LensFlares, FRDGBuilder&, const FViewInfo&, const FLensFlareInputs&, FLensFlareOutputsData&);
extern RENDERER_API FPP_LensFlares PP_LensFlares;

class UPostProcessLensFlareAsset;

UCLASS()
class CUSTOMPOSTPROCESS_API UPostProcessSubsystem : public UEngineSubsystem
{
	GENERATED_BODY()
	
public:
    // Init function to setup the delegate and load the data asset
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;

    // Used for cleanup
    virtual void Deinitialize() override;

private:
    // The reference to the data asset storing the settings
    UPROPERTY(Transient)
    UPostProcessLensFlareAsset* PostProcessAsset;

    // Called by engine delegate Render Thread
    void RenderLensFlare(
        FRDGBuilder& GraphBuilder,
        const FViewInfo& View,
        const FLensFlareInputs& Inputs,
        FLensFlareOutputsData& Outputs
    );

    // Threshold prender pass
    FRDGTextureRef RenderThreshold(
        FRDGBuilder& GraphBuilder,
        FRDGTextureRef InputTexture,
        FIntRect& InputRect,
        const FViewInfo& View
    );

    // Ghosts + Halo render pass
    FRDGTextureRef RenderFlare(
        FRDGBuilder& GraphBuilder,
        FRDGTextureRef InputTexture,
        FIntRect& InputRect,
        const FViewInfo& View
    );

    // Glare render pass
    FRDGTextureRef RenderGlare(
        FRDGBuilder& GraphBuilder,
        FRDGTextureRef InputTexture,
        FIntRect& InputRect,
        const FViewInfo& View
    );

    // Sub-pass for blurring
    FRDGTextureRef RenderBlur(
        FRDGBuilder& GraphBuilder,
        FRDGTextureRef InputTexture,
        const FViewInfo& View,
        const FIntRect& Viewport,
        int BlurSteps
    );

    // Cached blending and sampling states
    // which are re-used across render passes
    FRHIBlendState* ClearBlendState = nullptr;
    FRHIBlendState* AdditiveBlendState = nullptr;

    FRHISamplerState* BilinearClampSampler = nullptr;
    FRHISamplerState* BilinearBorderSampler = nullptr;
    FRHISamplerState* BilinearRepeatSampler = nullptr;
    FRHISamplerState* NearestRepeatSampler = nullptr;
};

```
- 엔진의 버전과 연결하기 위해 델리게이트를 다시 선언. 그 다음 줄에서 extern 정의를 통해 객체를 선언
- `UPostProcessLensFlareAsset` 전방선언
- `Initialize()`와 `Deinitialize()`은 서브시스템의 기본 함수. 몇가지 설정을 위해 오버라이딩 해준다.
- `PostProcessAsset`은 콘텐츠 브라우저에서 가져올 렌더링 매개변수에 대한 참조.
- `RenderLensFlare(), RenderThreshold(), RenderFlare(), RenderGlare() RenderBlur()`는 각각 다른 패스를 렌더링하는 데 사용할 다양한 렌더링 함수.
- FRHIBlendState와 FRHISamplerState는 다양한 패스에서 사용될 여러 매개변수.

**PostProcessSubsystem.cpp**
```cpp
#include "PostProcessSubsystem.h"
#include "PostProcessLensFlareAsset.h"

#include "RenderGraph.h"
#include "ScreenPass.h"
#include "PostProcess/PostProcessLensFlares.h"
#include "DataDrivenShaderPlatformInfo.h"
#include "SceneRendering.h"

namespace
{
    // TODO_SHADER_SCREENPASS

    // TODO_SHADER_RESCALE

    // TODO_SHADER_DOWNSAMPLE

    // TODO_SHADER_KAWASE

    // TODO_SHADER_CHROMA

    // TODO_SHADER_GHOSTS

    // TODO_SHADER_HALO

    // TODO_SHADER_GLARE

    // TODO_SHADER_MIX
}

void UPostProcessSubsystem::Initialize( FSubsystemCollectionBase& Collection )
{
    Super::Initialize( Collection );

    //--------------------------------
    // Delegate setup
    //--------------------------------
    FPP_LensFlares::FDelegate Delegate = FPP_LensFlares::FDelegate::CreateLambda(
        [this]( FRDGBuilder& GraphBuilder, const FViewInfo& View, const FLensFlareInputs& Inputs, FLensFlareOutputsData& Outputs )
    {
        RenderLensFlare(GraphBuilder, View, Inputs, Outputs);
    });

    ENQUEUE_RENDER_COMMAND(BindRenderThreadDelegates)([Delegate](FRHICommandListImmediate& RHICmdList)
    {
        PP_LensFlares.Add(Delegate);
    });

    //--------------------------------
    // Data asset loading
    //--------------------------------
    FString Path = "PostProcessLensFlareAsset'/CustomPostProcess/DefaultLensFlare.DefaultLensFlare'";

    PostProcessAsset = LoadObject<UPostProcessLensFlareAsset>( nullptr, *Path );
    check(PostProcessAsset);
}

void UPostProcessSubsystem::Deinitialize()
{
    ClearBlendState = nullptr;
    AdditiveBlendState = nullptr;
    BilinearClampSampler = nullptr;
    BilinearBorderSampler = nullptr;
    BilinearRepeatSampler = nullptr;
    NearestRepeatSampler = nullptr;
}
```
namespace는 기존 엔진쪽과 출동 없이 전역 셰이더를 선언하는 데 사용됨. 여기서의 TODO는 다음 단계에서 작성됨.
 `Initialize()`는 두가지 큰 작업을 수행함.
1. delegate 설정이 이루어 진다. 엔진에 의해 브로드캐스트가 트리거될때 내부 함수가 호출되도록 정의하는 곳이다. 이는 람다를 사용해 델리게이트 객체를 빌드하고, ENQUEUE_RENDER_COMMAND를 사용하여 모든 것ㅇ르 등록하는 곳이다.
2. 다음으로 데이터 에셋을 로드한다. 이 함수가 생성자의 일부가 아니기 때문에 FObjectFinder 대신, LoadObject() 도우미를 사용하여 에셋을 로드한다. 여기서 경로를 자신의 경로로 대체해야 한다.
==여기서 델리게이트를 설정하고 연결하는 방법이 ThreadSafe하지 않을 수 있다는 말이 있다. 작성자가 직적 이 문제와 관련된 크래시를 보진 않았지만, 그대로 제품에 사용하긴 적합하지 않을 수 있다는 점에 유의하자.
이 문제에 대한 해결법으로 제안된 것은, 렌더링 코드를 서브 클래스로 이동하고 `CreateShared()`로 만든 ThreadSafe한 포인터(TSharedPtr)에 저장하는 것이다.==

# 6. Utility Functions
유틸리티 함수들은 PostProcessSubsystem.cpp에 그대로 작성되었다.(헤더x)

이 함수는 서브 영역 크기를 계산하고 버퍼를 다시 크기 조정하는 비율을 출력한다. 이것은 threshold패스중에 유용하다. 대부분의 코드는 엔진 자체에서 복사하여 붙여넣은 것.
```cpp
FVector2D GetInputViewportSize( const FIntRect& Input, const FIntPoint& Extent )
{
    // Based on
    // GetScreenPassTextureViewportParameters()
    // Engine/Source/Runtime/Renderer/Private/ScreenPass.cpp

    FVector2D ExtentInverse = FVector2D(1.0f / Extent.X, 1.0f / Extent.Y);

    FVector2D RectMin = FVector2D(Input.Min);
    FVector2D RectMax = FVector2D(Input.Max);

    FVector2D Min = RectMin * ExtentInverse;
    FVector2D Max = RectMax * ExtentInverse;

    return (Max - Min);
}
```

다음은 가장 중요한 함수인데, 실제로 렌더 그래프에 등록될 draw다.
```cpp
// The function that draw a shader into a given RenderGraph texture
template<typename TShaderParameters, typename TShaderClassVertex, typename TShaderClassPixel>
inline void DrawShaderPass(
        FRDGBuilder& GraphBuilder,
        const FString& PassName,
        TShaderParameters* PassParameters,
        TShaderMapRef<TShaderClassVertex> VertexShader,
        TShaderMapRef<TShaderClassPixel> PixelShader,
        FRHIBlendState* BlendState,
        const FIntRect& Viewport
    )
{
    const FScreenPassPipelineState PipelineState(VertexShader, PixelShader, BlendState);

    GraphBuilder.AddPass(
        FRDGEventName( TEXT("%s"), *PassName ),
        PassParameters,
        ERDGPassFlags::Raster,
        [PixelShader, PassParameters, Viewport, PipelineState] (FRHICommandListImmediate& RHICmdList)
    {
        RHICmdList.SetViewport(
            Viewport.Min.X, Viewport.Min.Y, 0.0f,
            Viewport.Max.X, Viewport.Max.Y, 1.0f
        );

        SetScreenPassPipelineState(RHICmdList, PipelineState);

        SetShaderParameters(
            RHICmdList,
            PixelShader,
            PixelShader.GetPixelShader(),
            *PassParameters
        );

        DrawRectangle(
            RHICmdList,                             // FRHICommandList
            0.0f, 0.0f,                             // float X, float Y
            Viewport.Width(),   Viewport.Height(),  // float SizeX, float SizeY
            Viewport.Min.X,     Viewport.Min.Y,     // float U, float V
            Viewport.Width(),                       // float SizeU
            Viewport.Height(),                      // float SizeV
            Viewport.Size(),                        // FIntPoint TargetSize
            Viewport.Size(),                        // FIntPoint TextureSize
            PipelineState.VertexShader,             // const TShaderRefBase VertexShader
            EDrawRectangleFlags::EDRF_Default       // EDrawRectangleFlags Flags
        );
    });
}
```
- `FScreenPassPipelineState`: 렌더링 방법을 정의하는데 사용. 스텐실 마스크를 설정하는 데 사용될 수 있음. 지금은 블렌딩 모드를 변경하는 데만 사용.
- `AddPass()`: 이에 연결된 람다 함수를 통해 패스를 등록하는데 사용
- `FRDGEventName()`: 패스에 이름을 지정하는데 사용. 그래픽 디버거(ex. RenderDoc)에 표시됨.
- `RHICmdList`: RHI에 명령을 보내는 데 사용. 이 경우 SetViewport()를 사용해 대상 버퍼의 어느 영역이 그려질 지 정의함.
- `SetShaderParameters()`: 셰이더 매개변수는 미리 정의된 다음 이 함수를 통해 전달됨.
- `DrawRectangle()`: 최종 함수. 직접 메시 데이터를 구축하지 않고도 버퍼에 쿼드를 그릴 수 있도록 도와주는 함수. 전달된 모든 정보는 쿼드를 어디에 그리고 어느 크기로 그려야 하는지를 정의하는 데만 사용. 쿼드의 크기는 UV크기와 독립적이며, 예를 들어 버퍼의 하위 영역을 그릴 때 유용하다. 이 경우 쿼드 크기와 UV가 다르지 않다.(항상 전체 버퍼를 업데이트 하기 때문)

### DrawRectangle()
이 함수는 **SceneFilterRendering.cpp**.에 정의되어 있고, **SceneFilterRendering.h**에 아래와 같이 
위 코드에서 해당 함수를 사용하기 위해서, 헤더파일또는 소스코드에서 이 함수가 존재함을 알려주자.
```cpp
extern RENDERER_API void DrawRectangle(
    FRHICommandList& RHICmdList,
    float X,
    float Y,
    float SizeX,
    float SizeY,
    float U,
    float V,
    float SizeU,
    float SizeV,
    FIntPoint TargetSize,
    FIntPoint TextureSize,
    const TShaderRef<FShader>& VertexShader,
    EDrawRectangleFlags Flags = EDRF_Default,
    uint32 InstanceCount = 1
);
```
# 7. 메인 렌더링 함수
먼저 몇가지 툴을 추가한다. 렌더링 프로세스 단계를 건너뛰는데 사용될 몇 가지 콘솔 변수를 추가한다. 그리고 `DECLARE_GPU_STAT`를 사용하여 새로운 GPU 통계 이벤트를 추가한다. 이를 통해 엔진의 라이브 GPU프로파일러를 통해 효과의 렌더링 시간을 볼 수 있다.
```cpp
TAutoConsoleVariable<int32> CVarLensFlareRenderBloom(
    TEXT("r.LensFlare.RenderBloom"),
    1,
    TEXT(" 0: Don't mix Bloom into lens-flare\n")
    TEXT(" 1: Mix the Bloom into the lens-flare"),
    ECVF_RenderThreadSafe);

TAutoConsoleVariable<int32> CVarLensFlareRenderFlarePass(
    TEXT("r.LensFlare.RenderFlare"),
    1,
    TEXT(" 0: Don't render flare pass\n")
    TEXT(" 1: Render flare pass (ghosts and halos)"),
    ECVF_RenderThreadSafe);

TAutoConsoleVariable<int32> CVarLensFlareRenderGlarePass(
    TEXT("r.LensFlare.RenderGlare"),
    1,
    TEXT(" 0: Don't render glare pass\n")
    TEXT(" 1: Render flare pass (star shape)"),
    ECVF_RenderThreadSafe);

DECLARE_GPU_STAT(LensFlaresTyT)
```

이제 렌더링 함수로 넘어간다.
```cpp
void UPostProcessSubsystem::RenderLensFlare(
    FRDGBuilder& GraphBuilder,
    const FViewInfo& View,
    const FLensFlareInputs& Inputs,
    FLensFlareOutputsData& Outputs
)
{
    check(Inputs.Bloom.IsValid());
    check(Inputs.HalfSceneColor.IsValid());

    if (PostProcessAsset == nullptr)
    {
        return;
    }

    RDG_GPU_STAT_SCOPE(GraphBuilder, LensFlaresTyT)
    RDG_EVENT_SCOPE(GraphBuilder, "LensFlaresTyT");
	[...]
}
```
`check`는 invaild data에 대해서는 렌더링 패스를 실행하지 않기 위해서다. 데이터 에셋 또한 vaild한지 체크해 준다.
그리고 GPU state event를 등록해 준다. 이 부분은 `RenderLensFlare()`가 실질적으로 렌더링 쓰레드에서 실행되기 때문에 이곳에 작성해 준다.

다음은 몇몇 변수를 설정하는데, 이 부분은 실제로 다른 렌더링 함수에서 사용되는 것을 재사용 하는 것 이다.
```cpp
	[...]
	const FScreenPassTextureViewport BloomViewport(Inputs.Bloom);
    const FVector2D BloomInputViewportSize = GetInputViewportSize( BloomViewport.Rect, BloomViewport.Extent );

    const FScreenPassTextureViewport SceneColorViewport(Inputs.HalfSceneColor);
    const FVector2D SceneColorViewportSize = GetInputViewportSize( SceneColorViewport.Rect, SceneColorViewport.Extent );

    // Input
    FRDGTextureRef InputTexture = Inputs.HalfSceneColor.Texture;
    FIntRect InputRect = SceneColorViewport.Rect;

    // Outputs
    FRDGTextureRef OutputTexture = Inputs.HalfSceneColor.Texture;
    FIntRect OutputRect = SceneColorViewport.Rect;

    // States
    if( ClearBlendState == nullptr )
    {
        // Blend modes from:
        // '/Engine/Source/Runtime/RenderCore/Private/ClearQuad.cpp'
        // '/Engine/Source/Runtime/Renderer/Private/PostProcess/PostProcessMaterial.cpp'
        ClearBlendState = TStaticBlendState<>::GetRHI();
        AdditiveBlendState = TStaticBlendState<CW_RGB, BO_Add, BF_One, BF_One>::GetRHI();

        BilinearClampSampler = TStaticSamplerState<SF_Bilinear, AM_Clamp, AM_Clamp, AM_Clamp>::GetRHI();
        BilinearBorderSampler = TStaticSamplerState<SF_Bilinear, AM_Border, AM_Border, AM_Border>::GetRHI();
        BilinearRepeatSampler = TStaticSamplerState<SF_Bilinear, AM_Wrap, AM_Wrap, AM_Wrap>::GetRHI();
        NearestRepeatSampler = TStaticSamplerState<SF_Point, AM_Wrap, AM_Wrap, AM_Wrap>::GetRHI();
    }

    // TODO_RESCALE

    ////////////////////////////////////////////////////////////////////////
    // Render passes
    ////////////////////////////////////////////////////////////////////////
    FRDGTextureRef ThresholdTexture = nullptr;
    FRDGTextureRef FlareTexture = nullptr;
    FRDGTextureRef GlareTexture = nullptr;

    ThresholdTexture = RenderThreshold(
        GraphBuilder,
        InputTexture,
        InputRect,
        View
    );

    if( CVarLensFlareRenderFlarePass.GetValueOnRenderThread() )
    {
        FlareTexture = RenderFlare(
            GraphBuilder,
            ThresholdTexture,
            InputRect,
            View
        );
    }

    if( CVarLensFlareRenderGlarePass.GetValueOnRenderThread() )
    {
        GlareTexture = RenderGlare(
            GraphBuilder,
            ThresholdTexture,
            InputRect,
            View
        );
    }

    // TODO_MIX

    ////////////////////////////////////////////////////////////////////////
    // Final Output
    ////////////////////////////////////////////////////////////////////////
    Outputs.Texture = OutputTexture;
    Outputs.Rect    = OutputRect;

} // End RenderLensFlare()
```
`FScreenPassTextureViewport`와 `FVector2D`는 입력 버퍼 속성을 계산하는 데 사용된다. 이를 `FRDGTextureRef OutputTexture`가 따라서 `Outputs`구조체에 저장되고 엔진으로 다시 전달되는 출력 텍스처다. `FRDGTextureRef`는 단순히 RDG 텍스처에 대한 포인터다.

다음은 다양한 States를 초기화 한다. 이들은 렌더 스레드를 통해서만 사용 가능한 RHI에 액세스 해야 하기 때문에 여기에서 초기화 된다.

나머지는 작성된 대로 렌더링 된다.
___

남은 렌더함수는 잠시 두고, 다음 단계로 넘어간다.
```cpp
FRDGTextureRef UPostProcessSubsystem::RenderThreshold(
    FRDGBuilder& GraphBuilder,
    FRDGTextureRef InputTexture,
    FIntRect& InputRect,
    const FViewInfo& View
)
{
    // TODO_THRESHOLD

    // TODO_THRESHOLD_BLUR

    return FRDGTextureRef();
}

FRDGTextureRef UPostProcessSubsystem::RenderFlare(
    FRDGBuilder& GraphBuilder,
    FRDGTextureRef InputTexture,
    FIntRect& InputRect,
    const FViewInfo& View
)
{
    // TODO_FLARE_CHROMA
    
    // TODO_FLARE_GHOST
    
    // TODO_FLARE_HALO
    return FRDGTextureRef();
}

FRDGTextureRef UPostProcessSubsystem::RenderGlare(
    FRDGBuilder& GraphBuilder,
    FRDGTextureRef InputTexture,
    FIntRect& InputRect,
    const FViewInfo& View
)
{
    // TODO_GLARE
    return FRDGTextureRef();
}

FRDGTextureRef UPostProcessSubsystem::RenderBlur(
    FRDGBuilder& GraphBuilder,
    FRDGTextureRef InputTexture,
    const FViewInfo& View,
    const FIntRect& Viewport,
    int BlurSteps
)
{
    // TODO_BLUR
    return FRDGTextureRef();
}
```

# 8. Common Shader
==이전 단계에서 남겨둔 TODO를 하나씩 해결한다==

이제 common shader를 설정해야 한다. 버퍼에 렌더링 하기 위해 최소 버텍스, 픽셀 셰이더가 필요하다. 픽셀 셰이더는 다른 패스와는 좀 다르겠지만, 버텍스 셰이더는 대부분의 패스에 대해 거의 동일하다. 왜냐하면 단순히 사각형을 렌더링 하기 때문이다.

**TODO_SHADER_SCREENPASS**
```cpp
// RDG buffer input shared by all passes
BEGIN_SHADER_PARAMETER_STRUCT(FCustomLensFlarePassParameters, )
    SHADER_PARAMETER_RDG_TEXTURE(Texture2D, InputTexture)
    RENDER_TARGET_BINDING_SLOTS()
END_SHADER_PARAMETER_STRUCT()

// The vertex shader to draw a rectangle.
class FCustomScreenPassVS : public FGlobalShader
{
public:
    DECLARE_GLOBAL_SHADER(FCustomScreenPassVS);

    static bool ShouldCompilePermutation(const FGlobalShaderPermutationParameters&)
    {
        return true;
    }

    FCustomScreenPassVS() = default;
    FCustomScreenPassVS(const ShaderMetaType::CompiledShaderInitializerType& Initializer)
        : FGlobalShader(Initializer)
    {}
};
IMPLEMENT_GLOBAL_SHADER(FCustomScreenPassVS, "/CustomShaders/ScreenPass.usf", "CustomScreenPassVS", SF_Vertex);     // CustomPostProcess.cpp에서 매핑한 경로가 /CustomShaders이므로 잘 확인하고 작성할 것
```
`BEGIN_SHADER_PARAMETER_STRUCT`매크로로 셰이더 파라미터를 정의한다. `END_SHADER_PARAMETER_STRUCT`가 나올때까지 연관된 속성 목록이다.
`SHADER_PARAMETER_RDG_TEXTURE`는 RDG버퍼를 위한 입력 텍스처다. 렌더 타겟이나 다른 텍스처2D는 다른 매크로를 사용한다. `RENDER_TARGET_BINDING_SLOTS`은 버퍼가 셰이더에 첨부될 수 있도록 보조 매개변수를 추가한다. 자세한 정보는
- Engine/Source/Runtime/RenderCore/Public/ShaderParameterMacros.h
에서 매크로 정의를 찾을 수 있다.

글로벌 셰이더는 기본적으로 FGlobalShader에서 상속된 C++클래스다. 그런 다음 셰이더 프로그램을 컴파일 하는 데 사용할 실제 HLSL 파일을 지정하기 위해 `MPLEMENT_GLOBAL_SHADER`매크로를 사용한다. 이 매크로는 네가지 인수를 갖는다.
- C++ 클래스: 바로 위에서 생성한 클래스
- 심볼릭 경로: 모듈에서 정의한 심볼릭 경로에 따른 usf파일의 위치
- 함수 이름: 로드하려는 셰이더 파일의 함수 이름.
- 셰이더 유형: 다른 언어와 마찬가지로 Vertex 셰이더, Pixel 셰이더 등을 로드하는지를 지정. enum타입이다.
___
셰이더 파일을 작성한다.

ScreenPass.usf
```hlsl
#include "Shared.ush"

void CustomScreenPassVS(
    in float4 InPosition : ATTRIBUTE0,
    in float2 InTexCoord : ATTRIBUTE1,
    out noperspective float4 OutUVAndScreenPos : TEXCOORD0,
    out float4 OutPosition : SV_POSITION)
{
    DrawRectangle(InPosition, InTexCoord, OutPosition, OutUVAndScreenPos);
}
```

# 9. Rescale Pass
코드 단순화를 위해, 메인 렌더링 패스 시작부분에 선택적 렝더링 패스를 추가하여 부분 영역 렌더링을 보상(?)한다.
기본적으로  코드는 영역과 동일한 크기의 버퍼에 부분 영역의 복사본을 만든다. 그렇게 하면, UV를 조정할 필요가 없어진다.

에디터에서는 시각적 결과와 성능이 동일하게 유지되므로, 렌더링 크기가 변경되지 않는 한 동일하다. 전체화면으로의 전환이나 뷰포트 크기를 조정하는 경우, 버퍼 재할당으로 약간의 버벅임이 발생할 수 있지만, 받아들일만 하다.

**TODO_SHADER_RESCALE**
```CPP
#if WITH_EDITOR
    // Rescale shader
    class FLensFlareRescalePS : public FGlobalShader
    {
    public:
        DECLARE_GLOBAL_SHADER(FLensFlareRescalePS);
        SHADER_USE_PARAMETER_STRUCT(FLensFlareRescalePS, FGlobalShader);

        BEGIN_SHADER_PARAMETER_STRUCT(FParameters, )
            SHADER_PARAMETER_STRUCT_INCLUDE(FCustomLensFlarePassParameters, Pass)
            SHADER_PARAMETER_SAMPLER(SamplerState, InputSampler)
            SHADER_PARAMETER(FVector2f, InputViewportSize)
        END_SHADER_PARAMETER_STRUCT()

            static bool ShouldCompilePermutation(const FGlobalShaderPermutationParameters& Parameters)
        {
            return IsFeatureLevelSupported(Parameters.Platform, ERHIFeatureLevel::SM5);
        }
    };
    IMPLEMENT_GLOBAL_SHADER(FLensFlareRescalePS, "/CustomShaders/Rescale.usf", "RescalePS", SF_Pixel);
#endif
```
`#if WITH_EDITOR`는 프로젝트가 출시될때 컴파일시 제거되는 것을 의미한다.

이전 단계에서 보여준 것 처럼, `FGlobalShader`를 상속하는 새 클래스를 선언하여 시작한다.
- `SHADER_PARAMETER_STRUCT_INCLUDE`: 처음에 만들었던 셰이더 구조체(`FCustomLensFlarePassParameters`)를 참조한다. 여기서는 버퍼 텍스처 입력을 추가하기 위해 사용.
- `SHADER_PARAMETER_SAMPLER`: 새 샘플러 파라미터를 선언.
- `SHADER_PARAMETER`: 주어진 유형의 매개변수를 선언하고 그 이름을 지정. HLSL에서 float2로 사용될 FVector2D를 사용.
- `IMPLEMENT_GLOBAL_SHADER`: 이번에는 픽셀 셰이더 이므로 ,`SF_Pixel`을 사용함을 알 수 있음.
___
**Rescale.usf**
```hlsl
#include "Shared.ush"

void RescalePS(
    in noperspective float4 UVAndScreenPos : TEXCOORD0,
    out float4 OutColor : SV_Target0 )
{
    float2 UV = UVAndScreenPos.xy * InputViewportSize;
    OutColor.rgb = Texture2DSample( InputTexture, InputSampler, UV ).rgb;
    OutColor.a = 0;
}
```
`InputViewportSize`의 도움으로 영역 크기를 기반으로 UV를 재조정하여 버퍼를 채운다.
___
이제 셰이더를 사용하는 코드를 추가해 보자.

**TODO_RESCALE**
```
#if WITH_EDITOR
    if( SceneColorViewport.Rect.Width()  != SceneColorViewport.Extent.X
    ||  SceneColorViewport.Rect.Height() != SceneColorViewport.Extent.Y )
    {
        const FString PassName("LensFlareRescale");

        // Build target buffer
        FRDGTextureDesc Desc = Inputs.HalfSceneColor.Texture->Desc;
        Desc.Reset();
        Desc.Extent     = SceneColorViewport.Rect.Size();
        Desc.Format     = PF_FloatRGB;
        Desc.ClearValue = FClearValueBinding(FLinearColor::Transparent);
        FRDGTextureRef RescaleTexture = GraphBuilder.CreateTexture(Desc, *PassName);

        // Setup shaders
        TShaderMapRef<FCustomScreenPassVS> VertexShader(View.ShaderMap);
        TShaderMapRef<FLensFlareRescalePS> PixelShader(View.ShaderMap);

        // Setup shader parameters
        FLensFlareRescalePS::FParameters* PassParameters = GraphBuilder.AllocParameters<FLensFlareRescalePS::FParameters>();
        PassParameters->Pass.InputTexture       = Inputs.HalfSceneColor.Texture;
        PassParameters->Pass.RenderTargets[0]   = FRenderTargetBinding(RescaleTexture, ERenderTargetLoadAction::ENoAction);
        PassParameters->InputSampler            = BilinearClampSampler;
        PassParameters->InputViewportSize = FVector2f(SceneColorViewportSize);

        // Render shader into buffer
        DrawShaderPass(
            GraphBuilder,
            PassName,
            PassParameters,
            VertexShader,
            PixelShader,
            ClearBlendState,
            SceneColorViewport.Rect
        );

        // Assign result before end of scope
        InputTexture = RescaleTexture;
    }
#endif
```
영역 크기(Rect)와 버퍼 크기(Extent)가 일치하지 않으면 크기를 다시 조정한다.

실제 렌더링 코드에는 세가지 주요 블록이 있다.
- **Texture Creation**: 우리는 실제로 텍스처/버퍼를 빌드하지 않고, RDG가 하도록 지시한다. RDG가 컴파일할 때, 새로운 버퍼를 생성하거나 재사용한다. **GraphBuilder**는 명령을 등록할 수 있는 RDG의 인스턴스이고, **GraphBuilder.CreateTexture()** 는 텍스처를 빌드 하게 해주는 함수다. 우리는 버퍼가 가질 속성의 Description을 설명해 주면 된다.
  기존 버퍼의 Description을 재사용해 몇가지 설정을 재조정하는 것으로 성능을 향상시키는 것이 가능하다. 그것이 **HalfSceneColor**를 사용해 하는 코드다. 이것은 올바른 렌더링 플래그가 설정된 Description을 가지고 있기 때문에 수정할 필요가 없다.
- **Shader parameters**: 다음은 버텍스와 픽셀 셰이더 인스턴스를 생성한다. 이것은 **TShaderMapRef**를 채우는 셰이더 클래스를 사용해서 이루어 진다.
  그리고 실제 파라미터는 **GraphBuilder**를 사용해서 우리가 원하는 값을 할당할 수 있다.
- **Draw**: 마지막으로 **DrawShaderPass()** 를 호출하여 **GraphBuilder**에 렌더링을 요청한다. 이 함수가 어떻게 작동하는지는 **Utility fuction step**에서 다시 확인해 볼 수 있다.

==`FRenderTargetBinding`==및 매개변수 할당에 대해 좀더 자세히 설명하자면 셰이더에서 보았듯이, 우리는 버퍼 입력 자체가 참조되는 매개변수 구조체를 참조한다. 이것은 또한 결과를 버퍼를 정의하고 어디에 그릴지를 정의하는 곳이다. 이것이 `PassParameters->Pass.`를  사용해 구조체 파라미터에 접근하는 이유다.
**InputTexture**는 우리가 읽기를 원하는 텍스처이고, **RenderTargets\[0\]** 버퍼는 우리가 쓰기를 원하는 버퍼다. **FRenderTargetBinding**은 어떤 버퍼에 쓰기를 할 것인지와 그 방법을 지정하는 특수한 객체로, **ERenderTargetLoadAction**을 사용하여 버퍼를 덮어쓸지 아니면 누적할지(additive blending)를 지정할 수 있다.
대부분의 경우에서 작성자는 **ENoAction**을 사용하는데, 우리는 RGB값만 렌더링하고 셰이더는 누적을 필요가 없기 때문이다. 그래서 Clear나 Load할 필요가 없다.

마지막으로 새로생성된 버퍼를 **InputTexture**에 변수에 할당하여 다음 패스에서 사용할 수 있도록 한다.
___
# 10. Downsample and Threshold Pass
다운 샘플링과 약간의 블러 패스는 에일리어싱을 해결해 준다.
![[Pasted image 20240415192100.png]]
(**No custom filtering** vs **Downsampling** vs **Downsampling+Blur**, gif로 보면 확실히 티가난다.)

모든 후속 효과는 임계값 패스를 기반으로 구축된다. 따라서 이 임계값 패스를 잘 구축하는 것이 중요하다.
___
임계값 결과를 블러 처리하는 것은 좋은 효과를 볼 수 없다.
이전 **Activision**의 **Call of Duty: Advanced Warfare**에서 비슷한 문제를 겪은 블룸 생성에 대한 발표가 있었다.

그들은 블룸을 원래 입력 버퍼를 여러 번 축소하여 생성한다. 어느 순간 픽셀정보가 맞거나 틀린다. 그래서 카메라를 움직일 때 엘리어싱 문제로 깜박임이 발생한다. 그들의 해결책은 이동 중에도 최종 값을 안정화하기 위해 이웃 픽셀을 특정 가중치로 평균화하는 것이었다.
![[Pasted image 20240415191326.png]]
___
이제 위 방식을 기반으로 하는 다운샘플 패스를 만들어 보자

**TODO_SHADER_DOWNSAMPLE**
```cpp
// Downsample shader
class FDownsamplePS : public FGlobalShader
{
public:
    DECLARE_GLOBAL_SHADER(FDownsamplePS);
    SHADER_USE_PARAMETER_STRUCT(FDownsamplePS, FGlobalShader);

    BEGIN_SHADER_PARAMETER_STRUCT(FParameters, )
        SHADER_PARAMETER_STRUCT_INCLUDE(FCustomLensFlarePassParameters, Pass)
        SHADER_PARAMETER_SAMPLER(SamplerState, InputSampler)
        SHADER_PARAMETER(FVector2f, InputSize)
        SHADER_PARAMETER(float, ThresholdLevel)
        SHADER_PARAMETER(float, ThresholdRange)
    END_SHADER_PARAMETER_STRUCT()

        static bool ShouldCompilePermutation(const FGlobalShaderPermutationParameters& Parameters)
    {
        return IsFeatureLevelSupported(Parameters.Platform, ERHIFeatureLevel::SM5);
    }
};
IMPLEMENT_GLOBAL_SHADER(FDownsamplePS, "/CustomShaders/DownsampleThreshold.usf", "DownsampleThresholdPS", SF_Pixel);
```