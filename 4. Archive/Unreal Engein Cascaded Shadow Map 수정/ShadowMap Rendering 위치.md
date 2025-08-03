---
- DeferredShadingRenderer.cpp
```cpp
// 2465번째 줄
void FDeferredShadingSceneRenderer::Render(FRDGBuilder& GraphBuilder)
{
	...
	// 3521번째 줄
	RenderShadowDepthMaps(GraphBuilder, InstanceCullingManager, ExternalAccessQueue);
	...
}
```
- ShadowDepthRendering.cpp
```cpp
// 1660번째 줄
void FSceneRenderer::RenderShadowDepthMaps(FRDGBuilder& GraphBuilder, FInstanceCullingManager &InstanceCullingManager, FRDGExternalAccessQueue& ExternalAccessQueue)
{
	...
	// 1685번째 줄
	RenderShadowDepthMapAtlases(GraphBuilder);
	...
}
```
```cpp
// 1527번째 줄
void FSceneRenderer::RenderShadowDepthMapAtlases(FRDGBuilder& GraphBuilder)
{
	...
	
	...
}
```

