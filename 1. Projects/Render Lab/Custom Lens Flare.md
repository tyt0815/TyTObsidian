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
