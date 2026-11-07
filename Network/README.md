# Network (컴퓨터 통신)

컴퓨터통신 수업(2026-2학기)에서 배운 네트워크 내용을 주차별로 정리한 복습 기록

- 교재: 『컴퓨터 네트워크』
- 실습 환경: Wireshark, Cisco Packet Tracer, Windows PowerShell / CMD

각 주차는 두 파일로 나뉜다.
- `weekNN.md`: 개념 요약
- `weekNN-deep-dive.md`: 실제로 틀렸던 것 → 처음 생각 → 원리 → 깨달음

## 주차별 목차

| 주차 | 주제 | 교재 | 헷갈린 것 & 해결 |
|---|---|---|---|
| [1주차](week01.md) | 네트워크 구성요소, 패킷, 주소 3종(MAC·IP·포트), OSI 7계층, 캡슐화 | 1장 | [deep-dive](week01-deep-dive.md) |
| [2주차](week02.md) | 회선/패킷 교환, 대역폭/처리량, 지연 4종·지터, ISP/IX/CDN, 진단 명령어 | 1장 | [deep-dive](week02-deep-dive.md) |
| [3주차](week03.md) | 응용 계층, 소켓, P2P, DNS(캐시·TTL·리졸버·레코드), URL, HTTP 기본·쿠키/세션 | 2장 | [deep-dive](week03-deep-dive.md) |
| [4주차](week04.md) | 웹 캐시(ETag·304), HTTPS/TLS(인증서·DH·SNI), HTTP/1.1→2→3(QUIC), 이메일 | 2장 | [deep-dive](week04-deep-dive.md) |
| [5주차](week05.md) | 전송 계층, 포트 범위, 다중화/역다중화, 5-튜플, UDP 헤더·체크섬, TCP vs UDP | 3장 | [deep-dive](week05-deep-dive.md) |
| [6주차](week06.md) | TCP 헤더, 3-way/4-way 핸드셰이크, Seq/ACK·재전송, 흐름 제어(rwnd)·혼잡 제어(cwnd) | 3장 | [deep-dive](week06-deep-dive.md) |
| — | 중간고사 (1~3장, 서술형: OSI·TCP/IP 계층과 PDU, TCP 연결·전송 과정, UDP 특징, HTTP 버전별 차이) | | |
| [7주차](week07.md) | 네트워크 계층(포워딩/라우팅), IPv4 헤더·TTL·ICMP, MTU·단편화, 서브넷 계산·CIDR·VLSM, LPM, ARP·DHCP·NAT | 4장 | [deep-dive](week07-deep-dive.md) |
