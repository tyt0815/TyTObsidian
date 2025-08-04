5.5버전의 엔진 C++에서 MaterialExpression을 포함한 몇몇 설정은 직접적인 접근이 불가능 하고 `UMaterialEditorOnlyData`를 통해서 우회해서 접근해야 한다. 정확히 몇 버전부터 변경되었는지는 잘 모른다.

- 구버전
```cpp
// UMaterial* Material

Material->Expressions.Add(TextureSampleNode);
```

- 5.5버전
```cpp
UMaterialEditorOnlyData* MaterialEditorOnlyData = Material->GetEditorOnlyData();
MaterialEditorOnlyData->ExpressionCollection.Expressions.Add(TextureSampleNode);
```

그 밖에도 UMaterial 객체에서 직접 접근가능하던 것이 불가능하게 바뀌었다면 UMaterialEditorOnlyData를 통해 우회가능한지 살펴보자