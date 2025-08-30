# 공통 용어 정리
[[1. Projects/정보 보안 논문 맛보기/용어 정리/Exploit|Exploit]]
# 1. 논문 기본 정보
- 제목(Title): [Sugar: Secure GPU Acceleration in Web Browser](https://dl.acm.org/doi/pdf/10.1145/3296957.3173186)
- 저자(Authors): Zhihao Yao, Zongheng Ma, Yingtong Liu, Ardalan Amiri Sani, Aparna Chandramowlishwara
- 학회/저널(Venue): ASPLOS
- 발표/출판 연도: 2018

# 2. 연구 배경 (Background & Motivation)
## 2.1. 이 연구가 다루는 분야는?
- GPU acceleration
- Web browser
- Virtualization
- Systems security
## 2.2. 기존 연구/기술의 한계는 무엇인가?
- WebGL에서 셰이더 프로그래밍을 통해 [[1. Projects/정보 보안 논문 맛보기/용어 정리/DMA|DMA]]을 이용해 메인 메모리에 직접적으로 접근이 가능해 진다. 그로 인해 브라우저의 웹 앱 [[1. Projects/정보 보안 논문 맛보기/용어 정리/Sandbox|샌드박스]] 기능이 약화된다.
- WebGL의 [[1. Projects/정보 보안 논문 맛보기/용어 정리/Trusted Computing Base(TCB)|TCB]] 범위가 너무 넓어서 보안에 취약하다
- Microsoft는 WebGL의 보안 문제 때문에 초기에는 브라우저에 도입하지 않았다
- WebGL은 ad hoc(필요에 따라 그때그때)방식으로 취약점에 대응해 왔다.
	- WebGL을 브라우저내에서 GPU Process라 불리는 분리된 프로세스에 isolate 했다.
	- WebGL API가 호출될때 런타임 security check을 수행함.
		- [[1. Projects/정보 보안 논문 맛보기/용어 정리/Graphics plane|Graphics plane]]의 취약점이 발견되면 security check를 추가한다.
		- 브라우저 WebGL 구현부의 취약점은 직접 패치(보안 업데이트)를 수행한다.
	- untested GPU 디바이스 드라이버와 라이브러리는 blacklist로 만들어 WebGL 접근을 허용하지 않는다.
	- 위 세개의 solutions의 문제점
		- GPU Process 분리는 WebGL 구현체를 샌드박스할 수 있지만, 악성 웹으로 부터 OS의 [[1. Projects/정보 보안 논문 맛보기/용어 정리/Graphics plane|Graphics plane]]을 보호할 순 없음.
		- 보안 체크와 취약점 패치는 제로데이 취약점을 방어할 수 없음
		- 블랙리스트는 화이트 리스트 시스템에 대해서는 무용지물임
- 현재 모든 앱(네이티브 + 웹 앱)과 시스템 서비스(OS Window Manager등)은 단일 물리적 그래픽 플레인(single physical graphics plane, 물리적 GPU, 커널의 device driver 포함)을 사용한다. -> 웹앱에 상당한 크기의 TCB를 노출한다.

## 2.3. 왜 이 문제가 중요한가?(실제 응용/산업적 가치 등)
- 이전에 비해 웹 브라우저(또는 웹 앱)의 활용도가 강력해짐
- 파워포인트, 스프레드 시트 같이 기존에 네이티브 앱을 사용 해야 하던 앱들 조차 웹에서 사용이 가능하도록 서비스가 변화중
- 그 중 다양한 웹 앱이 GPU 가속을 사용하기 시작했으며, 그 중심에 WebGL이 있다.
- WebGL은 상위 100개의 웹사이트에서 53% 비율로 사용되고 있으며, 사용자들이 사용하는 브라우저의 96%는 WebGL을 지원하는 브라우저이다.


# 3. 문제 정의 (Problem Definition)
## 3.1. 연구에서 해결하려는 핵심 문제는?
WebGL의 보안 문제
## 3.2. 수학적/기술적으로 어떻게 정의되는가?
기존 방식들은 TCB 영역을 너무 많이 노출해 보안 문제를 해결하기 어렵다

# 4. 제안 방법 (Proposed Method)
## 4.1. 핵심 아이디어 한 줄 요약
GPU 가상화 기술을 활용하여 웹 앱이 가상 그래픽 플레인을 사용하도록 하는 것이다.
## 4.2. 방법론 전체 흐름(Flow)

## 4.3. 주요 기법/모델/알고리즘 설명

# 5. 실험 및 결과 (Experiments & Results)
## 5.1. 사용한 데이터 셋 / 환경

## 5.2. 비교 대상 (Baseline)

## 5.3. 주요 평가 지표 (Metrics)

## 5.4. 핵심 결과

## 5.5. 성능 향상 포인트 요약

# 6. 결론 및 기여 (Conclusion & Contributions)
## 6.1. 논문의 핵심 기여 요약
## 6.2. 한계점 (Limitations)

## 6.3. 향후 연구 가능성 (Future Work)

# 7. 개인 코멘트 (My Comments)
## 7.1.내가 이해한 핵심

## 7.2. 발표할 때 강조하고 싶은 부분

## 7.3. 내가 느낀 장점/단점

## 7.4. 내 연구/관심 분야와의 연관성
