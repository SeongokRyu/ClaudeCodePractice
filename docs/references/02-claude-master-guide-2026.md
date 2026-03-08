# Claude Code 마스터 가이드 2026

- **URL**: https://claudeguide-dv5ktqnq.manus.space/
- **특징**: 28개 섹션, 120+ 실전 팁, 한국어, 단일 페이지 앱
- **출처**: Anthropic Docs, paddo.dev, Andrej Karpathy, Simon Willison, Reddit 등 20+ 소스
- **최종 업데이트**: 2026.02.25

---

## 28개 섹션 요약

### 초급 섹션

**핵심 철학**
- Intent over Implementation: "무엇을/왜"를 정의하면 AI가 "어떻게"를 처리
- Conductor, not Coder: 지휘자 역할
- Trust but Verify: 신뢰하되 검증
- Context Engineering: 올바른 답이 자명해지도록 환경을 구조화

**황금 워크플로우**: Explore → Plan → Implement → Commit

**CLAUDE.md 작성법**
- 포함: bash 명령어, 스타일 규칙, 테스트 방법, 브랜치 컨벤션, 아키텍처 결정, 환경 변수
- 제외: 코드에서 읽을 수 있는 것, 언어 표준 규칙, 상세 API 문서
- Pro Tip: "이 줄을 제거하면 Claude가 실수할까?" → NO면 삭제

**7대 실수**
1. 맹목적 신뢰 (리뷰 없이 수락)
2. 아키텍처 부재 (스파게티 코드)
3. 라텐트 버그 (엣지 케이스 누락)
4. 기술 부채 과속 (유지보수 능력 초과)
5. 학습 부채 (이해 없이 사용)
6. 스코프 크리프 (범위 비대)
7. 자율 루프 과신 (판단 영역 자동화)

**황금 원칙 10가지**
1. 코드는 무가치하다. 스펙이 핵심이다
2. Plan Before Execute
3. Compact Often (/clear)
4. CLAUDE.md는 짧게
5. Delegate to Subagents
6. Git Worktree로 병렬화
7. CLI > MCP (컨텍스트 효율)
8. Hooks로 강제 (결정론적)
9. Rewind Freely
10. 리뷰/테스트/이해했다면 안전

### 중급 섹션

**컨텍스트 관리**
- LLM 성능 = 컨텍스트 윈도우 관리
- 자동 컴팩션: ~80%에서 트리거
- HANDOFF.md로 세션 간 인수인계

**프롬프팅 기법**
- 검증 수단 제공이 단일 최고 레버리지 행동
- 인터뷰 기법: Claude에게 역질문시켜 스펙 완성
- 구조화된 프롬프팅: 역할 + 컨텍스트 + 제약조건 + 예상 출력 + 검증 기준
- @ 참조로 필요한 파일만 명시적 참조
- 파이프 입력: `cat error.log | claude`

**서브에이전트**
- 메인 컨텍스트 보호하며 멀티태스킹
- haiku/sonnet/opus 작업 복잡도에 맞게
- Worktree 병렬 개발
- Writer/Reviewer 패턴

**보안 체크리스트**
- 슬롭스쿼팅(Slopsquatting) 주의: AI가 존재하지 않는 패키지 추천
- 필수 보안 품질 게이트 8가지

**프로젝트 레시피 12가지**
- SaaS, Chrome 확장, REST API, CLI, React Native, 랜딩페이지, 대시보드, AI 챗봇, VS Code 확장, 자동화 스크립트, Canvas 게임, ETL 파이프라인

**프롬프트 템플릿 20개** (복사해서 바로 사용)

**디버깅 마스터 15가지 전략**
- 핵심: /clear로 오염된 컨텍스트 리셋, Plan Mode로 설계 승인, 최소 단위 변경

### 고급 섹션

**Agent Teams** (Research Preview)
- 멀티 에이전트 팀 협업, Lead agent 조율
- 서브에이전트와 달리 팀원 간 직접 커뮤니케이션

**Hooks 시스템**
- CLAUDE.md = 확률적 / Hooks = 결정론적
- 보호 파일 편집 차단, 자동 포맷, 알림
- Exit code: 0=계속, 2=차단

**멀티세션 워크플로우 8가지 패턴**
1. Writer/Reviewer
2. Specialist 팀 (병렬)
3. 경쟁 프로토타입
4. 단계적 마이그레이션
5. TDD Ping-Pong
6. 야간 자율 작업
7. 리뷰 파이프라인
8. 마이크로서비스 개발

**비용 최적화 10가지**
- 최고의 비용 최적화: CLAUDE.md + 명확한 프롬프트 + /compact

**MCP 실전 활용**
- 주요 서버: Context7, Playwright, GitHub, Supabase, PostgreSQL, Notion, Slack, Figma, Exa

**AI 코드 리뷰 8가지 마스터 패턴**
- 신뢰 레벨 단계적 확대 (Level 1~4)
- "AI가 작성 → 인간이 검증 → 테스트가 증명" 3단계 파이프라인
