# Instanced Static Mesh
동일한 Static Mesh를 여러번 그려야 할때, Mesh 갯수만큼 드로우 콜을 하는 대신, 한번의 드로우콜로 모든 Mesh를 그리는 최적화 기법

# Instanced Static Mesh Component in C++
개인적으로 고생했던 부분인데, 해당 컴포넌트를 C++에서 CreateDefaultSubobject 함수로 생성할 경우, 인스턴스를 추가하면 엄청나게 버그가 걸리며 렌더링이 깨지며 메모리를 미친듯이 잡아먹는다. 퍼포먼스가 어마어마하게 떨어지는 것은 덤. 따라서 해당 컴포넌트는 BP에서만 생성해 사용할 수 있도록 하자.

![[Pasted image 20240306155058.png]]

위와 같이 생성자에서 실행할 함수(`Generate Room`)를 C++로 구현하고, Add Instanced Static Mesh Component함수로 Instanced Static Mesh Component를 만들고 변수로 설정해 준뒤, 함수의 인자로 던져주는 방식으로 하면 정상적으로 작동하게 된다.

# ==Clear Instances==
위 사진을 보면 알겠지만, Clear Instances함수를 실행하게 되면 해당 Instanced Static Mesh Component는 사라지게 된다. 따라서 다시 만들어 주어야 한다.