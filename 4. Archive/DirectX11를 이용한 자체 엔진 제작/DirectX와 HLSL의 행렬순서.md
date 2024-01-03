# 행렬순서와 연산 
**Created at : 2023-09-21 18:05**

DirectX와 HLSL의 행렬저장의 순서가 다르다.
DirectX 라이브러리는 Row-major방식이며 HLSL은 Colomn-major방식이다.
![[Pasted image 20230921180910.png]]
간단히 설명하면
float\[4\]\[4\]에 행렬을 저장한다 할때,
DirectX의 float\[0\]은 a11~a13을 저장하고
HLSL은 a11~a31을 저장한다.
따라서 WVP(World View Projection 또는 MVP) 행렬과 같이 행렬을 HLSL로 넘길때는 항상 XMMatrixTranspose함수로 Transpose해주고 넘기도록 하자. 
~~교재에서는 Effect Framework를 사용하는데 이건 자동으로 Transpose해주는 듯 하다. 이거때매 며칠을 버렸는지~~

