---
GBuffer를 렌더링 하기 위해 멀티 렌더타겟을 사용함

PipelineState를 생성할때 다음과 같이 해주어야 한다.
```cpp
GBufferPassPipelineStateDesc.NumRenderTargets = 3;
GBufferPassPipelineStateDesc.RTVFormats[0] = mGBuffers->GetFormat();
GBufferPassPipelineStateDesc.RTVFormats[1] = mGBuffers->GetFormat();
GBufferPassPipelineStateDesc.RTVFormats[2] = mGBuffers->GetFormat();
```

렌더 타겟 설정은 [공식 문서](https://learn.microsoft.com/ko-kr/windows/win32/api/d3d12/nf-d3d12-id3d12graphicscommandlist-omsetrendertargets)에 따르면 두가지 방법으로 할 수 있다.

첫번째 방법은 묶으려는 렌더타겟들이 힙내에서 연속적으로 있을 경우 세번째 인자(RTsSingleHandleToDescriptorRange)를 true로 해주고 아래와 같이 작성할 수 있다.
```cpp
D3D12_CPU_DESCRIPTOR_HANDLE GBufferARtv = mGBuffers->GetRTV("GBufferA", 0);
D3D12_CPU_DESCRIPTOR_HANDLE GBufferDsv = mGBuffers->GetDSVHeap()->GetCPUDescriptorHandleForHeapStart();
CommandList->OMSetRenderTargets(3, &GBufferARtv, true, &GBufferDsv);
```
이경우 렌더타겟이 아래 사진과 같이 묶이게 된다
![[Attachments/Pasted image 20250407204852.png]]

두번째 방법은 렌더타겟의 힙내 위치랑 관계없이 작성할 수 있다.
```cpp
D3D12_CPU_DESCRIPTOR_HANDLE GBufferARtv = mGBuffers->GetRTV("GBufferA", 0);
D3D12_CPU_DESCRIPTOR_HANDLE GBufferBRtv = mGBuffers->GetRTV("GBufferB", 0);
D3D12_CPU_DESCRIPTOR_HANDLE GBufferCRtv = mGBuffers->GetRTV("GBufferC", 0);
D3D12_CPU_DESCRIPTOR_HANDLE Rtvs[] = { GBufferARtv, GBufferBRtv, GBufferCRtv };
D3D12_CPU_DESCRIPTOR_HANDLE GBufferDsv = mGBuffers->GetDSVHeap()->GetCPUDescriptorHandleForHeapStart();
CommandList->OMSetRenderTargets(_countof(Rtvs), Rtvs, true, &GBufferDsv);
```
이경우 렌더타겟은 아래 사진과 같이 묶이게 된다.
![[Attachments/Pasted image 20250407205110.png]]

마지막으로 픽셀 셰이더에서의 적용은 아래와 같다.
```hlsl
void MainPS(
    in float4 PosH : SV_Position,
    in float3 NormalW : NORMAL,
    in float2 TexC : TEXCOORD,
    out float4 GBufferA : SV_Target0,
    out float4 GBufferB : SV_Target1,
    out float4 GBufferC : SV_Target2
)
{
...
}
```
위와 같이 SV_Target에 번호를 붙여주면 된다.
