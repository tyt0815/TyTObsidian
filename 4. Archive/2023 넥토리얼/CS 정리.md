---
dg-publish: true
---

# CS 정리 
**Created at : 2023-10-28 21:26**

1. 자료구조
2. 컴퓨터 구조
3. 운영체제
4. 알고리즘
5. 인공지능/딥러닝
6. 그래픽스

# 1. 자료구조
## 1.1. sort
### 1.1.1. Shell Sort
gap을 설정해 gap 마다 솔트 -> gap을 계속해서 줄여나가서 최종적으로 1로 만듦
gap은 홀수가 좋음
### 1.1.2. Quick Sort
- Devide and Conquer
가장 왼쪽을 피봇으로 정함.
가장 왼쪽을 i, 가장 오른쪽을 j로 해서 피봇보다 작은 i와 피봇보다 큰 j를 찾음.
둘을 정렬함.
i<j인 동안 반복
가장 왼쪽과 j-1, 가장 j+1과 가장 오른쪽을 다시 quick sort를 반복함.
O(n^2)
최적을땐 T(n)
### 1.1.3. Heap Sort
크기가 n인 배열일때, n/2부터 시작함.(즉 리프노드의 부모노드부터)
n/2 노드가 root라 했을때, heap을 만족하게 만듦.
그렇게 아래에서부터 계속해서 위로 올라감
### 1.1.4. Bubble Sort
```cpp
#define SWAP(x, y, t) t=x; x=y; y=t;
void bubble_sort(int list[], int n)
{
	int i, j, temp;
	for(i = n - 1; i > 0; ++i)
	{
		 for(j = 0; j < i; ++j)
		 {
			 if(list[j] > list[j + 1])
				 SWAP(list[j], list[j+1], temp);
		 }
	}
}
```
## 1.2. Hash

Bucket과 Slot으로 구성
각 버킷마다 슬롯이 있음.
버킷이 겹치면 collision, slot이 꽉차서 더이상 넣을 수 없으면 overflow
slot이 여러개 일 수 있기 때문에 1대1함수는 아님.
# 2. 컴퓨터 구조
## 2.1. 레지스터와 메모리
![[Attachments/Pasted image 20231030172144.png]]
## 2.2. 숫자
2의 보수