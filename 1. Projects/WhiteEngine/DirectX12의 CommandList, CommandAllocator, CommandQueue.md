# CommandList
- 명령을 저장하는 객체
- Reset메소드를 통해 기존 명령들을 비우고 CommandAllocator로 부터 새로운 명령공간을 할당받을 수 있음.
- 이전과 다른 CommandAllocator로 리셋을 하는 경우 이전CommandAllocator에서 기록한 명령을 지우지 않고 새로운 공간을 할당 받을 수 있음. 즉 GPU가 명령을 마치는 것을 기다릴 필요 없이 바로 다음 명령 작성에 들어 갈 수 있음.
- 따라서 여러개의 CommandList를 사용하는 것은 비효율적. 다만 멀티 스레딩을 사용하는 경우 스레드간 명령제출에 간섭이 없게 하기 위해 스레드마다 CommadList를 갖게 하는게 좋음
# CommandAllocator
- CommandList에 명령을 저장할 공간을 할당해줌
- 위에 언급된 바와 같이 같은 CommandList에 공간을 할당하더라도 다른 CommandAllocator가 할당되면 다른 공간에 할당됨
# CommandQueue
