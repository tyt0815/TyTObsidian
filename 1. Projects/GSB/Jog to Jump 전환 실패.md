![[1. Projects/GSB/Attachments/Pasted image 20250411110345.png]]
위 사진과 같이 공중을 걷고 있다.

![[1. Projects/GSB/Attachments/Pasted image 20250411110429.png]]

# 원인
여러번 돌려가며 분석해본 결과, 왼발이 앞에 있을때 점프하는것과 오른발이 앞에 있을때 점프하는것에서 차이가 왔었다.
![[1. Projects/GSB/Attachments/Pasted image 20250411112710.png]]
![[1. Projects/GSB/Attachments/Pasted image 20250411112747.png]]
왼다리가 앞에 있을때 점프하면 바로 점프 자세로 전환한다.

![[1. Projects/GSB/Attachments/Pasted image 20250411112831.png]]
![[1. Projects/GSB/Attachments/Pasted image 20250411112901.png]]
오른다리가 앞에 있을때 점프하면 공중에 뜨고도 한참을 걷는다.

# 부분 해결
기본적으로 에셋을 만들수는 없기 때문에 극약처방 느낌으로 Jump Database에 BaseCost를 -1을 해주어서 공중에 뜨면 점프 애니메이션이 선택받기 쉽게 해 주었다.
그럼에도 불구하고, 앞으로 달리다 점프하는것 외에 좌, 우, 후방으로 달리다 점프하는 것은 아직도 전환이 잘 안된다. 그 이유는 스키마가 데이터베이스를 평가하는데 있어서 속도와 위치를평가하는데 수직방향(Z축)의 속도와 위치만 평가하는 것이 불가능하기 때문에 이것은 무조건 추가적인 에셋이 필요한 부분이다.