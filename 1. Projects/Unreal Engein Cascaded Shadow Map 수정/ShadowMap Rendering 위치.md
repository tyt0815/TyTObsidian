
- DefferedShadingRenderer.cpp
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

	...
}
```
