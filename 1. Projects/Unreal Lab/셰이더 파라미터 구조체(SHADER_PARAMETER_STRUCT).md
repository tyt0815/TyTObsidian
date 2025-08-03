---
셰이더 코드에 버퍼들을 묶기 위해서 정의해야하는 구조체
```cpp
BEGIN_SHADER_PARAMETER_STRUCT(FMyShaderParameterStruct,)
	SHADER_PARAMETER_RDG_TEXTURE(Texture2D, InTexture)
	SHADER_PARAMETER(FVector2f, ViewportSize)
	SHADER_PARAMETER_SAMPLER(SamplerState, InputSampler)
	SHADER_PARAMETER_STRUCT_REF(FViewUniformShaderParameters, ViewUniformBuffer)
	SHADER_PARAMETER_RDG_UNIFORM_BUFFER(FSceneTextureUniformParameters, SceneTexturesUniformBuffer)

	RENDER_TARGET_BINDING_SLOTS()
END_SHADER_PARAMETER_STRUCT()
```
위와 같은 구조로 선언을 할 수 있으며 그 사이에 파라미터를 선언한다.

- `SHADER_PARAMETER`: float,FVector2f와 같은 기본 자료형을 묶을 수 있다.
- `SHADER_PARAMETER_RDG_TEXTURE`: Texture묶을때 사용 할 수 있다.
- `SHADER_PARAMETER_SAMPLER`: SamplerState를 묶을 수 있다.
- `SHADER_PARAMETER_STRUCT_REF`: TUniformBufferRef타입의 유니폼 버퍼 구조체를 묶을 수 있다.
- `SHADER_PARAMETER_RDG_UNIFORM_BUFFER`: TRDGUniformBufferRef타입의 유니폼 버퍼 구조체를 묶을 수 있다.
- `RENDER_TARGET_BINDING_SLOTS`: 렌더 타겟 슬롯을 바인딩 할 수 있다.
