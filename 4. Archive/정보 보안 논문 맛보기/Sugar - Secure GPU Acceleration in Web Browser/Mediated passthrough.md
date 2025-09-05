[[4. Archive/정보 보안 논문 맛보기/Sugar - Secure GPU Acceleration in Web Browser/Direct passthrough]]
[[4. Archive/정보 보안 논문 맛보기/Sugar - Secure GPU Acceleration in Web Browser/Full emulation]]

- 위 두 방식의 **중간** 접근법.
- 하드웨어 자원은 **직접 접근(passthrough)** 하지만,  
    가상화 계층이 **중재(mediated)** 해서 안전성과 격리를 보장.
- VM(또는 웹앱 프로세스)은 **가상의 GPU(vGPU)** 를 사용하는데,  
    실제 접근은 가상화 계층이 trap 해서 에뮬레이션하거나 조정.