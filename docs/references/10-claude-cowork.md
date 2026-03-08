# Claude Cowork

---

## 한줄 요약

**Cowork**는 Claude Desktop 앱 안의 **비개발자용 AI 에이전트 모드**다.
Claude Code가 개발자를 위한 것이라면, Cowork는 일반 지식 노동자를 위한 것이다.

---

## 핵심 개념

| 항목 | 내용 |
|------|------|
| **정식 명칭** | Cowork (Claude Desktop 내 모드) |
| **출시일** | 2026.01.12 (Research Preview) |
| **타겟 사용자** | 비개발자 — 마케터, 기획자, 분석가, 법무, HR 등 |
| **핵심 차이** | Claude Code = 터미널 기반, 개발자용 / Cowork = GUI 기반, 지식노동자용 |
| **공통 기반** | Claude Agent SDK (동일 아키텍처) |

---

## Claude Code vs Cowork

| 차원 | Claude Code | Cowork |
|------|-------------|--------|
| 인터페이스 | 터미널 CLI | Claude Desktop GUI |
| 대상 | 개발자 | 지식 노동자 |
| 작업 영역 | 코드베이스 | 문서, 스프레드시트, 프레젠테이션 |
| 실행 환경 | 로컬 터미널 | 격리된 VM (샌드박스) |
| 설정 파일 | CLAUDE.md, .claude/* | 글로벌/폴더별 지침 |
| 확장 | MCP, Skills, Agents, Hooks | Plugins, MCP 커넥터 |
| 팀 협업 | Agent Teams | (아직 미지원) |

---

## 작동 방식

1. Claude Desktop 앱 → **Cowork 탭** 전환
2. 특정 로컬 폴더에 접근 권한 부여
3. 원하는 작업을 자연어로 설명
4. Claude가 계획 수립 → 서브태스크 분해 → 자율 실행
5. 격리된 VM 내부에서 실행 (보안)
6. 완료된 결과물 확인

---

## 주요 기능

- **로컬 파일 직접 접근**: 업로드/다운로드 없이 파일 읽기/수정/생성
- **서브에이전트 조율**: 복잡한 작업을 병렬 워크스트림으로 분해
- **전문 문서 생성**: Excel (수식 포함), PowerPoint, 서식 문서
- **Plugins**: HR, 디자인, 엔지니어링, 재무 분석 등 영역별 확장
- **MCP 커넥터**: Google Drive, Gmail, DocuSign, FactSet 등
- **예약 작업**: 온디맨드 또는 자동 실행
- **브라우저 연동**: Claude in Chrome으로 웹 작업

---

## 출시 타임라인

| 날짜 | 마일스톤 |
|------|---------|
| 2026.01.12 | Research Preview (Max, macOS) |
| 2026.01.16 | Pro 구독자 확대 |
| 2026.01.23 | Team/Enterprise 확대 |
| 2026.01.30 | Agentic Plugins 출시 |
| 2026.02.10 | Windows 지원 |
| 2026.02.24 | Enterprise 커넥터 업데이트 |

---

## 제한사항

- 세션 간 메모리 없음
- 세션 공유 불가
- Desktop 전용 (웹/모바일 미지원)
- 앱 닫으면 세션 종료
- 표준 채팅보다 토큰 소비 많음
- 규정 준수 워크로드 미지원 (아직)
- 파일 삭제는 명시적 허가 필요

---

## Practice에 활용할 점

- Cowork는 현재 Practice 범위 밖 (개발자 대상이 아님)
- 그러나 **동일한 Agent SDK 기반**이므로, Agent SDK를 배우면 Cowork 이해에도 도움
- 비개발자 동료에게 Claude 활용을 설명할 때 참고 자료로 유용
- 향후 "비개발자 트랙" Practice를 만든다면 Cowork 기반으로 설계 가능
