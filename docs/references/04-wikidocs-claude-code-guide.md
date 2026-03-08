# 클로드 코드 가이드 (WikiDocs)

- **URL**: https://wikidocs.net/book/19104
- **특징**: 한국어 종합 레퍼런스. 25개 챕터. 체계적인 기능별 가이드.
- **전체 내용**: `wikidocs_19104_full.md` (685KB) 별도 저장

---

## 목차 및 핵심 내용

| # | 챕터 | URL | 핵심 내용 |
|---|------|-----|----------|
| 00 | 퀵 레퍼런스 | wikidocs.net/331427 | 빠른 참조 카드 |
| 01 | 소개 | wikidocs.net/331389 | Claude Code 개요 |
| 02 | 설치 및 설정 | wikidocs.net/331390 | 플랫폼별 설치 가이드 |
| 03 | 기본 사용법 | wikidocs.net/331391 | 기본 조작 방법 |
| 04 | 설정 시스템 | wikidocs.net/331392 | 설정 파일, 환경 변수 |
| 05 | 권한 시스템 | wikidocs.net/331393 | 퍼미션 모드, 샌드박스 |
| 06 | 슬래시 명령어 | wikidocs.net/331394 | /clear, /compact, /model 등 |
| 07 | 키보드 단축키 | wikidocs.net/331395 | Shift+Tab, Ctrl+G 등 |
| 08 | MCP 서버 | wikidocs.net/331396 | MCP 개념, 설정, 활용 |
| 09 | 훅 (Hooks) | wikidocs.net/331397 | 라이프사이클 이벤트 자동화 |
| 10 | 서브에이전트 | wikidocs.net/331398 | 하위 에이전트 활용 |
| 11 | 스킬 (Skills) | wikidocs.net/331399 | SKILL.md 작성법 |
| 12 | IDE 연동 | wikidocs.net/331400 | VS Code, JetBrains 통합 |
| 13 | CI/CD 통합 | wikidocs.net/331401 | GitHub Actions, GitLab |
| 14 | CLI 레퍼런스 | wikidocs.net/331402 | 전체 CLI 플래그 |
| 15 | 고급 기능 | wikidocs.net/331403 | Extended Thinking, 파이프 등 |
| 16 | 베스트 프랙티스 | wikidocs.net/331404 | 효율적 사용 패턴 |
| 17 | 트러블슈팅 | wikidocs.net/331405 | 문제 해결 가이드 |
| 18 | 플러그인 시스템 | wikidocs.net/331406 | 플러그인 설치/개발 |
| 19 | 실전 워크플로우 | wikidocs.net/331407 | 실무 활용 시나리오 |
| 20 | 클라우드 실행 | wikidocs.net/331408 | 웹 기반 Claude Code |
| 21 | 보안과 프라이버시 | wikidocs.net/331409 | 보안 고려사항 |
| 별1 | 창시자의 워크플로우 | wikidocs.net/331801 | Claude Code 창시자 인터뷰 |
| 별2 | 스피너 동사 모음 | wikidocs.net/331745 | 재미 요소 |
| 별99 | 전체 변경 이력 | wikidocs.net/332223 | 업데이트 로그 |

---

## Practice 설계에 참고할 핵심 챕터

### 베스트 프랙티스 (Ch.16)
- Explore → Plan → Implement → Commit 워크플로우
- 컨텍스트 윈도우 관리 전략
- 효과적인 프롬프팅 패턴

### 실전 워크플로우 (Ch.19)
- 코드베이스 탐색
- 버그 수정 워크플로우
- 리팩토링 패턴
- 테스트 주도 개발
- PR 생성 및 코드 리뷰

### 트러블슈팅 (Ch.17)
- 일반적인 문제와 해결 방법
- 성능 최적화 팁

### 고급 기능 (Ch.15)
- Extended Thinking 활용
- Unix 파이프라인 연동
- 세션 관리 (resume, continue)
- Git Worktree 병렬 작업
