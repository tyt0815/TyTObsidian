```hlsl
// Screen좌표 -> View 좌표계
float3 TransformScreenToView(in float2 TexC, float Depth, in float4x4 InvProj)
{
    float4 NDCPosition = float4(TexC * 2 - 1.0f, Depth, 1.0f);
    NDCPosition.y *= -1;
    float4 ViewPosition = mul(NDCPosition, InvProj);
    ViewPosition /= ViewPosition.w;
    return ViewPosition.xyz;
}

// View 좌표계 -> World 좌표계
float3 TransformViewToWorld(in float3 ViewPosition, in float4x4 InvView)
{
    float4 WorldPosition = mul(float4(ViewPosition, 1.0f), InvView);
    return WorldPosition.xyz;
}

// Screen좌표계 -> World 좌표계
float3 TransformScreenToWorld(in float2 TexC, float Depth, in float4x4 InvProj, in float4x4 InvView)
{
    float3 ViewPosition = TransformScreenToView(TexC, Depth, InvProj);
    return TransformViewToWorld(ViewPosition, InvView);
}
```

여기서 개인적으로 이해가 안갔던 부분은 `TransformScreenToView`함수이다.
우리가 좌표계를 게산할때는 보통 아래와 같은 과정이다.
Local ->(WorldMat) -> World -> (ViewMat) -> View -> (ProjMat) -> Clip -> NDC -> Viewport
여기서 Clip 부터 Viewport 좌표계까지는 하드웨어에서 진행해 준다.
중요한 점은 `TransformScreenToView`함수를 보면 Clip에서 InvProj를 하여 뷰포트를 구하는 것이 아니라 NDC에서 InvProj를 하고 그 결과값의 w성분으로 나눠준다. 이것은 행렬 계산을 해보면 이해할 수 있다.
![[Attachments/KakaoTalk_20250409_202908867.jpg]]
요약을 하자면 View를 Z성분으로 나눈 벡터(V)에 Proj를 곱해주면 NDC가 나온다.
V는 View가 되려면 View의 Z성분을 곱해주어야 하는데 이 값은 V의 w의 역수이다. 따라서 
V = NDC * InvProj
View = V * View.z = V / V.w
가 성립한다.