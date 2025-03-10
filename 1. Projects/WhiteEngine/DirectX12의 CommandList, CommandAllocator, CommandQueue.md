# CommandList
- 명령을 저장하는 객체
- Reset메소드를 통해 기존 명령들을 비우고 CommandAllocator로 부터 새로운 명령공간을 할당받을 수 있음.
- 이전과 다른 CommandAllocator로 리셋을 하는 경우 이전CommandAllocator에서 기록한 명령을 
CommandList는 명령을 저장하는 객체. Reset메소드를 통해 CommandAllocator로 부터 공간을 할당받아 저장하기 때문에 단일 스레드에서 여러개의 CommandList를 사용한다해서 특별한 이점은 없음. 멀티스레드에서는 스레드마다 CommandList가 있어야 스레드간 간섭 없이 명령을 수행하