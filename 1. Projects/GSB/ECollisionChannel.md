---
dg-publish: true
---


![[../../4. Archive/WhiteEngine/Attachments/Pasted image 20250413210933.png]]
새로 추가한 ObjectType은 프로젝트 폴더의 Config/DefaultEngine.ini 파일에서 정보를 확인할 수 있다.

![[../../4. Archive/WhiteEngine/Attachments/Pasted image 20250413220131.png]]

해당하는 이넘값을 가져와 사용하면 된다.

참고로 라인 트레이싱은 `ECollisionResponse::ECR_Block`으로 해야 인식한다.