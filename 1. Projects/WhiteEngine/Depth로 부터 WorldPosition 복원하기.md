
```hlsl
// NDC 공간 기준 좌표계 -> View 좌표계
float3 TransformNDCToView(in float2 TexC, float Depth, in float4x4 InvProj)
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
```