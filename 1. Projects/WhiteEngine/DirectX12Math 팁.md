[DirectX 문서](https://learn.microsoft.com/ko-kr/windows/win32/dxmath/pg-xnamath-internals)
# XMVECTOR
**XMVECTOR**는 16바이트 경계에 alignment가 일어나므로 클래스의 멤버변수로 활용할땐
- **XMFLOAT2**
- **XMFLOAT3**
- **XMFLOAT4**
를 사용하고, 연산시에는 **XMVECTOR**로 변환해서 사용한다.

## 매개변수 XMVECTOR
**XMVECTOR**  인스턴스를 인수로 해서 함수를 호출할때 **XMVECTOR** 값이 스택이 아닌 SSE/SSE2 레지스터를 통해서 함수에 전달되게 해야 한다. 그런 식으로 전달 가능한 인수의 개수는 플랫폼과 컴파일러 마다 다르다. **XMVECTOR** 매개변수 전달에 대한 규칙을 요약하면 아래와 같다.
- 함수 이름 앞에 **XM_CALLCONV** 호출 규약 지시자를 붙인다
- 처음 세 **XMVECTOR** 매개변수에는 반드시 **FXMVECTOR** 형식을 지정한다
- 넷째 **XMVECTOR** 매개변수에는 반드시 **GXMVECTOR** 형식을 지정한다
- 다섯째와 여섯째 **XMVECTOR** 매개변수에는 반드시 **HXMVECTOR** 형식을 지정한다.
- 그 이상의 **XMVECTOR** 매개변수에는 반드시 **CXMVECTOR**형식을 지정한다.
매개변수의 위치와 상관없이, **XMVECTOR**의 갯수에 따라 적용해 주면 된다.

생성자에서는 조금 다른 규칙을 적용함을 주의한다.
- **XM_CALLCONV** 호출 규약 지시자를 사용하지 않는다.
- 처음 세 **XMVECTOR**는 **FXMVECTOR**를 사용하고, 나머지는 모두 **CXMVECTOR**를 사용한다

## 상수 벡터
상수벡터를 포함한 중괄호 초기화 구문에서는 **XMVECTORF32** 형식을 사용해야 한다.
```cpp
const XMVECTORF32 Vector = {0.5f, 0.5f, 0.5f, 0.5f};
```

## 상등 비교
부동 소수점는 항상 오차를 동반하기 때문에, 상등 판정을 할때는 **Epsilon(입실론)** 을 오차범위를 지정해 상등을 비교한다.
```cpp
XMFINLINE bool XM_CALLCONV XMVector3NearEqual(
	FXMVECTOR U,
	FXMVECTOR V,
	FXMVECTOR Epsilon
);
```

# XMMATRIX
**XMVECTOR**와 마찬가지로, **XMMATRIX**를 사용할때도 **XMFLOAT4X4**를 멤버변수로 사용하는 것이 추천된다.
