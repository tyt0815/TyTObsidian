[OpenGL Deferred Rendering](https://learnopengl.com/Advanced-Lighting/Deferred-Shading)
[DirectX Deferred Rendering](https://learn.microsoft.com/en-us/windows/win32/direct3d11/overviews-direct3d-11-render-multi-thread-render)

# GBuffer의 포맷
## Normal 벡터 저장
Normal 벡터를 저장할때 노말 벡터의 값들을 normalize했다고 가정할때 
-1 ~ 1의 범위를 갖기 때문에 R8G8B8A8_UNORM포맷을 사용할 경우 이 포맷의 범위인 0 ~ 1이랑 안맞음.
따라서 아래와 같이 -1 ~ 1값을 0 ~ 1값으로 인코딩후 디코딩해서 사용할 필요가 있음.
```
// 벡터를 normalize하고 0 ~ 1값으로 인코딩
float3 EncodeVector(float3 Vector)
{
    return (normalize(Vector) + 1.0f) / 2.0f;
}

// 0 ~ 1로 인코딩된 벡터를 -1 ~ 1로 디코딩
float3 DecodeVector(float3 EncodedVector)
{
    return EncodedVector * 2 - 1.0f;
}
```

```
float3 EncodedNormalW = EncodeVector(NormalW);
GBufferA = float4(EncodedNormalW, 1.0f);
```

```
float3 WorldNormal = gTexture[gGBufferATextureIndex].Sample(gsamLinearWrap, TexC).rgb;
WorldNormal = DecodeVector(WorldNormal);
```
![[Attachments/Pasted image 20250410115647.png]]
## 줄무늬 현상?
위 사진에서는 잘 안보이겠지만 포워드 셰이딩때와는 달리 특히 스펙큘라 반사부분에 줄무늬 현상이 나타난다.
![[Attachments/Pasted image 20250410122213.png]]

이는 아마도 R8G8B8A8_UNORM포맷의 정밀도 문제인 것으로 추정된다. R16G16B16A16_FLOAT같은 포맷으로 변경해 보자.
![[Attachments/Pasted image 20250410135912.png]]
변경항 후에는 확실히 없어진 모습을 확인할 수 있다.