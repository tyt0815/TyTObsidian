[[4. Archive/Unreal Lab/셰이더 파라미터 구조체(SHADER_PARAMETER_STRUCT)]]내용을 참고하여
```cpp
SHADER_PARAMETER_RDG_UNIFORM_BUFFER(FSceneTextureUniformParameters, SceneTexturesUniformBuffer)
```
를 통해 셰이더 파라미터 구조체를 구성한다.

```cpp
FSceneViewExtensionBase::PrePostProcessPass_RenderThread(FRDGBuilder& GraphBuilder, const FSceneView& InView, const FPostProcessingInputs& Inputs)
```
위 메소드를 사용한다 가정할때, 파라미터는 아래와 같이 바인딩 할 수 있다.
```cpp
Params->SceneTexturesUniformBuffer = Inputs.SceneTextures;
```

셰이더 코드에서는 다음 헤더파일을 포함시킨다.
```
#include "/Engine/Private/Common.ush"      // 필수 헤더
#include "/Engine/Public/Platform.ush"     // 필수 헤더
#include "/Engine/Private/SceneTexturesCommon.ush"   // SceneTextures를 사용할때 필요한 버퍼
```

SceneTexturesCommon.ush를 참고하여 함수를 골라서 사용하면 된다. 아래는 SceneColor를 얻는 방법이다.
```
float3 SceneColor = CalcSceneColor(UV);
```