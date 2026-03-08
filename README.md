# Claude Code Practice

Claude Code를 효율적으로 활용하기 위한 실습 과제 모음.

단순한 사용법 가이드가 아니라, **직접 해보면서 체득**할 수 있는 Practice 중심으로 구성했습니다.

> 이 Practice는 **프로그래밍 경험이 있는 개발자** 대상입니다.
> 코딩 경험이 없다면 [Claude Cowork](https://claude.com/product/cowork)를 추천합니다.

## 시작하기

[Getting Started](docs/getting-started.md) 가이드를 따라 15분 안에 환경을 준비하세요.

## 로드맵

34개 Practice를 5단계로 구성했습니다.

| Phase | 주제 | Practice | 소요 시간 |
|-------|------|----------|----------|
| **1. Foundation** | 핵심 워크플로우 체득 | 01-04 | 20~30분/개 |
| **2. Configuration** | 환경 설정 마스터 | 05-08 | 30~45분/개 |
| **3. Workflow Patterns** | 실무 패턴 습득 | 09-18 | 45~60분/개 |
| **4. Automation** | 업무 자동화 | 19-23 | 60~90분/개 |
| **5. Multi-Agent & Harness** | 프로덕션급 에이전트 시스템 | 24-34 | 90~120분/개 |

## Phase 1: Foundation

| # | Practice | 핵심 학습 포인트 | 난이도 |
|---|----------|-----------------|--------|
| 01 | [황금 워크플로우](practices/01-golden-workflow/) | Explore→Plan→Implement→Commit 사이클 | ★☆☆ |
| 02 | [프롬프팅 기법](practices/02-prompting-techniques/) | 검증 수단 제공, 인터뷰 기법, 구조화된 프롬프트 | ★☆☆ |
| 03 | [컨텍스트 관리](practices/03-context-management/) | /clear, /compact, HANDOFF.md, 세션 관리 | ★☆☆ |
| 04 | [Git 워크플로우](practices/04-git-workflow/) | 커밋, 브랜치, PR 생성, 안전한 Git 습관 | ★☆☆ |

## Phase 2: Configuration

| # | Practice | 핵심 학습 포인트 | 난이도 |
|---|----------|-----------------|--------|
| 05 | [CLAUDE.md 작성법](practices/05-claude-md/) | /init, 포함/제외 기준, 200줄 이하 | ★★☆ |
| 06 | [Hooks 설정](practices/06-hooks/) | 보호 파일 차단, 자동 포맷, 알림 | ★★☆ |
| 07 | [MCP 서버 연동](practices/07-mcp-servers/) | Context7, Playwright, Chrome DevTools | ★★☆ |
| 08 | [Skills 만들기](practices/08-skills/) | SKILL.md 작성, 재사용 워크플로우 정의 | ★★☆ |

## Phase 3: Workflow Patterns

| # | Practice | 핵심 학습 포인트 | 난이도 |
|---|----------|-----------------|--------|
| 09 | [TDD 워크플로우](practices/09-tdd-workflow/) | 테스트→구현→리팩토링, Ralph Loop | ★★☆ |
| 10 | [버그 디버깅](practices/10-bug-debugging/) | 15가지 디버깅 전략, 근본 원인 분석 | ★★☆ |
| 11 | [코드 리뷰](practices/11-code-review/) | AI 코드 리뷰 8가지 패턴, 신뢰 레벨 확대 | ★★☆ |
| 12 | [멀티 파일 리팩토링](practices/12-multi-file-refactoring/) | 대규모 변경, 의존성 추적 | ★★★ |
| 13 | [서브에이전트 활용](practices/13-subagents/) | 컨텍스트 보호, Writer/Reviewer, 병렬 작업 | ★★★ |
| 14 | [Worktree 병렬 개발](practices/14-worktree-parallel/) | claude --worktree, 독립 브랜치 동시 개발 | ★★★ |
| 15 | [Command→Agent→Skill](practices/15-orchestration-pattern/) | Orchestration 패턴 설계 및 구현 | ★★★ |
| 16 | [멀티세션 워크플로우](practices/16-multi-session/) | 경쟁 프로토타입, TDD Ping-Pong 등 | ★★★ |
| 17 | [7대 실수 체험](practices/17-anti-patterns/) | 안티패턴 경험 후 올바른 방법 학습 | ★★☆ |
| 18 | [보안 체크리스트](practices/18-security-checklist/) | 슬롭스쿼팅, OWASP Top 10 | ★★☆ |

## Phase 4: Automation

| # | Practice | 핵심 학습 포인트 | 난이도 |
|---|----------|-----------------|--------|
| 19 | [Headless Mode 기초](practices/19-headless-mode/) | claude -p, 파이프 입력, JSON 출력 | ★★☆ |
| 20 | [Git Hooks + Claude](practices/20-git-hooks-claude/) | pre-commit 보안 검사, 자동 커밋 메시지 | ★★☆ |
| 21 | [GitHub Actions 자동화](practices/21-github-actions/) | PR 자동 리뷰, 이슈 트리아지 | ★★★ |
| 22 | [배치 처리와 Fan-Out](practices/22-batch-processing/) | /batch, xargs -P 병렬 처리 | ★★★ |
| 23 | [스케줄링과 Cron](practices/23-scheduling/) | /loop, 야간 자율 작업 | ★★★ |

## Phase 5: Multi-Agent & Harness

| # | Practice | 핵심 학습 포인트 | 난이도 |
|---|----------|-----------------|--------|
| 24 | [Agent SDK 입문](practices/24-agent-sdk-intro/) | Python/TS로 첫 에이전트 구축 | ★★★ |
| 25 | [커스텀 서브에이전트 설계](practices/25-custom-subagents/) | .claude/agents/ 정의, 역할별 분리 | ★★★ |
| 26 | [Writer/Reviewer 패턴](practices/26-writer-reviewer/) | 구현+리뷰 에이전트 협업 파이프라인 | ★★★ |
| 27 | [Agent Teams 실습](practices/27-agent-teams/) | 팀 생성, 공유 태스크 리스트 | ★★★ |
| 28 | [Scatter-Gather 연구 시스템](practices/28-scatter-gather/) | Lead + 연구 서브에이전트 → 보고서 | ★★★ |
| 29 | [프로덕션 멀티에이전트 파이프라인](practices/29-production-pipeline/) | Command→Agent→Skill 3계층 | ★★★ |
| 30 | [결정론적 가드레일](practices/30-deterministic-guardrails/) | Hooks로 파일 보호, 위험 명령 차단 | ★★★ |
| 31 | [컨텍스트 엔지니어링](practices/31-context-engineering/) | 정보 환경 설계, 고신호 토큰 선별 | ★★★ |
| 32 | [샌드박싱과 권한 제어](practices/32-sandboxing/) | /sandbox, 파일시스템/네트워크 격리 | ★★★ |
| 33 | [품질 게이트 파이프라인](practices/33-quality-gates/) | 검증 게이트, LLM-as-judge | ★★★ |
| 34 | [에이전트 모니터링과 로깅](practices/34-monitoring-logging/) | 구조화 로깅, 장애 복구 | ★★★ |

## 핵심 원칙

1. **Explore → Plan → Implement → Commit**
2. **검증 수단 제공** = 단일 최고 레버리지 행동
3. **컨텍스트 윈도우 관리** = 성능의 핵심
4. **CLAUDE.md는 짧게, 핵심만** (200줄 이하)
5. **Hooks = 결정론적** vs CLAUDE.md = 확률적
6. **서브에이전트로 컨텍스트 보호**
7. **신뢰하되 검증** (Trust but Verify)

## 참고 자료

| 자료 | 설명 |
|------|------|
| [Anthropic 공식 Best Practices](https://code.claude.com/docs/en/best-practices) | 공식 가이드 |
| [shanraisshan/claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) | Orchestration 패턴 |
| [Claude Code 마스터 가이드 2026](https://claudeguide-dv5ktqnq.manus.space/) | 28섹션 120+팁 |
| [AI Native Camp](https://github.com/ai-native-camp/camp-1) | Skill 기반 커리큘럼 |
| [WikiDocs 클로드 코드 가이드](https://wikidocs.net/book/19104) | 한국어 종합 레퍼런스 |
