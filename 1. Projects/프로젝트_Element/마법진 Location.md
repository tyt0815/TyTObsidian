# Character Front 마법진
- [x] ChracterFront 마법진 구현 ✅ 2024-01-21
기본공격시 마법진을 생성할 위치를 계산한다.
기본적으로 공중에 떠있는 마법진을 계산할것 이다.
기본 아이디어는 이렇다.
![[Pasted image 20240108221938.png]]
사진에서 보이는 바와 같이 캐릭터가 화면정 중앙에 있지 않고 약간 비스듬하게 오른쪽 위에 위치하게 만들 것이다.
![[Pasted image 20240108223420.png]]

![[Pasted image 20240108223405.png]]
그림을 참고하며 설명하자면
1. 카메라의 Forward벡터를 이용하여 임시로 LookAt포인트를 잡는다.
2. ActorLocation이 허리쯤에 있으므로 (0, 0, 1)방향(윗 방향)으로 ZOffset만큼 올려 가슴 위치까지 올린다.
3. 가슴위치에서 LookAt포인트로 향하는 방향 벡터를 계산한다. 
	   (LookAt - ActorLocation + (0, 0, 1) * ZOffset).Nomalize
4. 계산한 방향으로 XOffset만큼 곱해서 가슴 위치에 더해준다.

![[Pasted image 20240108224042.png]]
위와 같이 나오게 된다.

## BugFix
[[캐릭터 회전시 카메라 회전 버그]]

# Fly 마법진
- [x] Fly 마법진 구현 ✅ 2024-01-20
![[Attachments/Pasted image 20240506123850.png]]
![[Attachments/Pasted image 20240506123914.png]]
포탈 마법을 사용할때 사용할 마법진
# Floor 마법진
- [x] Floor 마법진 구현 ✅ 2024-01-20
![[Drawing 2024-01-16 17.20.42.excalidraw]]
![[Drawing 2024-01-16 17.21.28.excalidraw]]
# TopDown 마법
- [x] ~~TopDown 마법~~(취소, Floor마법진으로 통합) ✅ 2024-01-20
![[Drawing 2024-01-16 17.20.42.excalidraw]]
![[Drawing 2024-01-16 17.25.34.excalidraw]]