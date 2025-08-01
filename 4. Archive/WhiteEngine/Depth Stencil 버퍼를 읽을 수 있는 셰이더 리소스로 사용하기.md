---
dg-publish: true
---

텍스처를 셰이더에서 읽을땐  SRV에 묶을 필요가 있다
하지만 뎁스 스텐실에서 사용하는 포맷인 `DXGI_FORMAT_D24_UNORM_S8_UINT`는 SRV에서 읽을 수 없다. 따라서 아래와 같이 해준다.

# 리소스 생성
리소스를 생성할때 `D3D12_RESOURCE_DESC::Format`을 `DXGI_FORMAT_R24G8_TYPELESS`로 해준다. 즉 사용처가 정해지지 않았다고 선언하는 것이다.
주의할 점은 `D3D12_CLEAR_VALUE::Format`은 `DXGI_FORMAT_D24_UNORM_S8_UINT`로 해주어야 정상적으로 `ClearDepthStencil`을 실행할 수 있다.
```cpp
D3D12_RESOURCE_DESC DepthStencilDesc;
ZeroMemory(&DepthStencilDesc, sizeof(D3D12_RESOURCE_DESC));
DepthStencilDesc.Dimension = D3D12_RESOURCE_DIMENSION_TEXTURE2D;
DepthStencilDesc.Alignment = 0;
DepthStencilDesc.Width = mWidth;
DepthStencilDesc.Height = mHeight;
DepthStencilDesc.DepthOrArraySize = 1;
DepthStencilDesc.MipLevels = 1;
DepthStencilDesc.Format = DXGI_FORMAT_R24G8_TYPELESS;
DepthStencilDesc.SampleDesc.Count = 1;
DepthStencilDesc.SampleDesc.Quality = 0;
DepthStencilDesc.Layout = D3D12_TEXTURE_LAYOUT_UNKNOWN;
DepthStencilDesc.Flags = D3D12_RESOURCE_FLAG_ALLOW_DEPTH_STENCIL;

OptClear.Format = DXGI_FORMAT_D24_UNORM_S8_UINT;
OptClear.DepthStencil.Depth = 1.0f;
OptClear.DepthStencil.Stencil = 0;
std::unique_ptr<FTexture> Texture = std::make_unique<FTexture>();
mDepthStencilTexture = Texture.get();
Texture->Name = std::string("RenderTargetDepth_") + std::to_string(sRenderTargetCount);
THROW_IF_FAILED(
	Device->CreateCommittedResource(
		&DefaultHeapProperties,
		D3D12_HEAP_FLAG_NONE,
		&DepthStencilDesc,
		D3D12_RESOURCE_STATE_COMMON,
		&OptClear,
		IID_PPV_ARGS(Texture->Resource.GetAddressOf())
	)
);
```

# DSV 생성
DSV를 생성할때에는 `D3D12_CLEAR_VALUE::Format`의 값과 같이 포맷을 설정해 준다.
```CPP
D3D12_DEPTH_STENCIL_VIEW_DESC DepthStencilViewDesc;
ZeroMemory(&DepthStencilViewDesc, sizeof(D3D12_DEPTH_STENCIL_VIEW_DESC));
DepthStencilViewDesc.Format = DXGI_FORMAT_D24_UNORM_S8_UINT;
DepthStencilViewDesc.ViewDimension = D3D12_DSV_DIMENSION_TEXTURE2D;
DepthStencilViewDesc.Flags = D3D12_DSV_FLAG_NONE;
DepthStencilViewDesc.Texture2D.MipSlice = 0;

Device->CreateDepthStencilView(
	mDepthStencilTexture->Resource.Get(),
	&DepthStencilViewDesc,
	mDSVHeap->GetCPUDescriptorHandleForHeapStart()
);
```

여기까지 하면 뎁스 스텐실에 쓰는것은 문제 없다.
# SRV 생성
이제 SRV를 생성할때는 포맷을 다르게 설정해 주어야 한다.
`D3D12_SHADER_RESOURCE_VIEW_DESC::Format`을 `DXGI_FORMAT_R24_UNORM_X8_TYPELESS`로 해서 뎁스는 읽고, 스텐실은 읽지 못하게 해준다.
```
D3D12_SHADER_RESOURCE_VIEW_DESC SRVDesc = {};
SRVDesc.Shader4ComponentMapping = D3D12_DEFAULT_SHADER_4_COMPONENT_MAPPING;
SRVDesc.ViewDimension = D3D12_SRV_DIMENSION_TEXTURE2D;
SRVDesc.Texture2D.MostDetailedMip = 0;
SRVDesc.Texture2D.ResourceMinLODClamp = 0.0f;
ID3D12Resource* TextureBuffer = Texture->Resource.Get();
SRVDesc.Texture2D.MipLevels = TextureBuffer->GetDesc().MipLevels;
SRVDesc.Format =	;

GetDXResourceManagerPtr()->GetDevicePtr()->CreateShaderResourceView(
	TextureBuffer,
	&SRVDesc,
	GetTexture2DCPUDescriptorHandle(Texture->SRVHeapIndex)
);
```

이제 뎁스 스텐실의 뎁스를 읽을 수 있다.
```hlsl
DepthStencilTexture.Sample(gsamLinearWrap, Texc).r
```
위와 같이 r값을 읽어오면 된다.