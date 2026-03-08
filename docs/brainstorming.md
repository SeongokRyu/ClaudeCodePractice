# Claude Code Practice - Brainstorming

## 목표

Claude Code를 효율적으로 활용하기 위한 실습 과제 모음을 만든다.
단순한 사용법 가이드가 아니라, 직접 해보면서 체득할 수 있는 Practice 중심으로 구성한다.

---

## 참고 자료 분석 (docs/references/)

| # | 자료 | 특징 | Practice에 활용할 점 |
|---|------|------|---------------------|
| 01 | [shanraisshan/claude-code-best-practice](references/01-shanraisshan-best-practice.md) | Command→Agent→Skill 패턴, 날씨 시스템 예제 | Orchestration 패턴, 설정 레퍼런스 |
| 02 | [Claude Code 마스터 가이드 2026](references/02-claude-master-guide-2026.md) | 28섹션, 120+팁, 한국어 | 황금 원칙 10가지, 7대 실수, 프롬프트 템플릿 20개 |
| 03 | [AI Native Camp](references/03-ai-native-camp.md) | 비개발자 7일 캠프, Skill로 커리큘럼 | "Skill로 배우는" 접근법, 점진적 구조 |
| 04 | [WikiDocs 클로드 코드 가이드](references/04-wikidocs-claude-code-guide.md) | 25챕터 종합 레퍼런스 | 기능별 체계적 가이드, 트러블슈팅 |
| 05 | [Anthropic 공식 문서](references/05-anthropic-official-docs.md) | 공식 Best Practices, Agent SDK | 7가지 핵심 원칙, 실패 패턴 |
| 06 | [업무 자동화](references/06-task-automation.md) | headless mode, CI/CD, Hooks, 배치 처리 | 자동화 패턴, 스크립팅, 스케줄링 |
| 07 | [멀티 에이전트 시스템](references/07-multi-agent-systems.md) | Agent SDK, Subagents, Agent Teams, 6가지 패턴 | 프로덕션 멀티에이전트 구축 |
| 08 | [Harness Engineering](references/08-harness-engineering.md) | 결정론적 제어, 거버넌스, 컨텍스트 엔지니어링 | 프로덕션급 에이전트 제어 체계 |
| 09 | [Markdown 설정 파일 가이드](references/09-markdown-config-files.md) | .claude/ 전체 구조, 모든 .md 설정 파일 | 프로젝트 구성 레퍼런스 |
| 10 | [Claude Cowork](references/10-claude-cowork.md) | Desktop GUI 에이전트, 비개발자용 | 비개발자 트랙, Agent SDK 공통 기반 |

### 자료에서 공통적으로 강조하는 핵심 원칙
1. **Explore → Plan → Implement → Commit** (모든 자료에서 반복)
2. **검증 수단 제공** = 단일 최고 레버리지 행동 (Anthropic 공식)
3. **컨텍스트 윈도우 관리** = 성능의 핵심 (/clear, /compact)
4. **CLAUDE.md는 짧게, 핵심만** (200줄 이하)
5. **Hooks = 결정론적** vs CLAUDE.md = 확률적
6. **서브에이전트로 컨텍스트 보호**
7. **신뢰하되 검증** (Trust but Verify)

---

## 기본 개념 / 용어 정리 (입문자용)

> Practice를 시작하기 전에 알아야 할 핵심 용어들. "이게 뭔데?"에서 시작하는 사람을 위한 설명.

### Claude Code란?

**Claude Code**는 Anthropic이 만든 **터미널(CLI) 기반 AI 코딩 에이전트**다.
채팅창에서 대화하듯 자연어로 지시하면, Claude가 코드를 읽고, 수정하고, 명령을 실행한다.
VS Code, JetBrains 같은 IDE 안에서도 쓸 수 있고, 터미널에서 직접 실행할 수도 있다.

### 기본 용어

| 용어 | 설명 |
|------|------|
| **CLI** | Command Line Interface. 마우스가 아닌 텍스트 명령으로 컴퓨터를 조작하는 방식. 터미널/콘솔이라고도 부른다. |
| **프롬프트 (Prompt)** | Claude에게 보내는 지시/질문 텍스트. "이 파일의 버그를 찾아줘" 같은 것. |
| **토큰 (Token)** | AI가 텍스트를 처리하는 최소 단위. 한글 한 글자 ≈ 2~3토큰, 영어 한 단어 ≈ 1토큰 정도. 비용과 성능에 직결된다. |
| **컨텍스트 윈도우** | Claude가 한 번에 기억할 수 있는 대화의 총량 (토큰 수). 윈도우가 차면 성능이 떨어진다. Claude Code 활용의 핵심 제약. |
| **세션 (Session)** | Claude Code와의 하나의 대화 단위. `claude` 명령으로 시작, `/clear`로 초기화, `--resume`으로 이전 세션 이어가기. |
| **컴팩션 (Compaction)** | 대화가 길어지면 이전 내용을 자동 요약해서 컨텍스트를 확보하는 것. `/compact`로 수동 실행 가능. ~80%차면 자동 트리거. |

### Claude Code의 도구 (Tools)

Claude Code는 사용자 지시를 수행하기 위해 내부적으로 **도구(Tool)**를 호출한다.

| 도구 | 하는 일 | 비유 |
|------|---------|------|
| **Read** | 파일 내용을 읽는다 | 파일 열어보기 |
| **Edit** | 파일의 특정 부분을 수정한다 | 찾아 바꾸기 |
| **Write** | 새 파일을 만들거나 전체를 덮어쓴다 | 새 파일 저장 |
| **Glob** | 파일 이름 패턴으로 검색한다 (`*.ts`, `src/**/*.py`) | 파일 탐색기에서 검색 |
| **Grep** | 파일 내용에서 텍스트를 검색한다 | Ctrl+Shift+F (전체 검색) |
| **Bash** | 터미널 명령을 실행한다 (`uv sync`, `git status` 등) | 터미널에 직접 타이핑 |
| **Agent** | 별도의 하위 에이전트를 띄워 독립 작업을 수행한다 | 동료에게 일 맡기기 |

### 설정 및 커스터마이징

| 용어 | 설명 |
|------|------|
| **CLAUDE.md** | 프로젝트 루트에 놓는 설정 파일. Claude가 매 세션 시작 시 자동으로 읽는 "프로젝트 헌법". 코딩 규칙, 빌드 명령어, 주의사항 등을 적는다. |
| **CLAUDE.local.md** | CLAUDE.md의 개인용 버전. Git에 올리지 않는 나만의 설정. |
| **Hooks** | Claude의 특정 행동(파일 수정, 명령 실행 등) 전후에 자동 실행되는 스크립트. CLAUDE.md의 규칙은 무시될 수 있지만, Hooks는 **100% 강제 실행**된다. |
| **Skills** | `.claude/skills/SKILL.md`에 정의하는 재사용 가능한 워크플로우. 특정 작업 패턴을 Claude에게 가르치는 매뉴얼. |
| **Commands** | `.claude/commands/`에 정의하는 슬래시 명령어. `/my-command`로 호출. |
| **MCP** | Model Context Protocol. Claude가 외부 도구/서비스(DB, Slack, Figma 등)와 통신하는 표준 규격. 플러그인처럼 기능을 확장한다. |
| **.claudeignore** | Claude가 무시할 파일/폴더 목록. `.gitignore`와 같은 문법. `node_modules/`, `dist/` 등 불필요한 파일을 제외해서 토큰을 절약한다. |

### 워크플로우 관련

| 용어 | 설명 |
|------|------|
| **Plan Mode** | Shift+Tab으로 진입. 코드를 수정하지 않고 계획만 세우는 읽기 전용 모드. 먼저 Plan → 승인 후 Implement. |
| **서브에이전트 (Subagent)** | Claude가 내부적으로 띄우는 하위 에이전트. 복잡한 조사 작업을 별도 컨텍스트에서 수행해서 메인 대화의 컨텍스트를 보호한다. |
| **Agent Teams** | 여러 Claude 인스턴스가 팀으로 협업하는 기능 (실험적). 팀원끼리 직접 소통하며 독립 작업. |
| **Worktree** | Git worktree를 활용해 격리된 브랜치에서 동시에 여러 작업을 수행하는 것. `claude --worktree feature-auth` |
| **체크포인트** | Claude가 작업 중 자동으로 만드는 저장 지점. Esc+Esc 또는 `/rewind`로 이전 상태로 되돌릴 수 있다. |
| **HANDOFF.md** | 세션을 넘길 때 작성하는 인수인계 문서. 다음 세션이 바로 이어받을 수 있도록 시도한 것, 성공/실패, 남은 작업을 기록. |

### 핵심 슬래시 명령어

| 명령어 | 하는 일 |
|--------|---------|
| `/init` | CLAUDE.md 자동 생성 (프로젝트 분석 기반) |
| `/clear` | 현재 대화 초기화 (새 세션 시작) |
| `/compact` | 대화 내용 압축 (컨텍스트 확보) |
| `/rewind` | 이전 체크포인트로 되돌리기 |
| `/model` | 사용 모델 변경 (opus/sonnet/haiku) |
| `/permissions` | 권한 설정 (허용할 도구/도메인) |
| `/sandbox` | OS 수준 격리 활성화 |
| `/cost` | 현재 세션 비용 확인 |

### 핵심 단축키

| 단축키 | 동작 |
|--------|------|
| Shift+Tab | 모드 순환 (Normal → Auto-accept → Plan) |
| Esc | 현재 작업 중단 |
| Esc+Esc | 체크포인트 목록 / 되돌리기 |
| Ctrl+G | Plan을 에디터에서 편집 |

### 프로젝트 설정 파일 체계 (.claude/ 디렉토리)

Claude Code를 프로젝트에 맞게 커스터마이징하려면 여러 종류의 markdown/json 설정 파일을 사용한다.
잘 구성된 `.claude/` 디렉토리는 Claude의 성능과 일관성을 크게 높인다.

**단계별 구성 (아무것도 없는 상태에서 시작)**

```
Level 1 — 최소 (모든 프로젝트)
  CLAUDE.md                      ← /init으로 자동 생성. 프로젝트 규칙.

Level 2 — 표준 (팀 프로젝트)
  CLAUDE.md
  CLAUDE.local.md                ← 개인 설정 (gitignore)
  .claude/settings.json          ← 권한, 훅 설정
  .claude/rules/*.md             ← 경로별 규칙 (프론트/백엔드 등)
  .mcp.json                      ← 외부 도구 연결

Level 3 — 고급 (자동화된 프로젝트)
  + .claude/agents/*.md          ← 커스텀 서브에이전트 (reviewer, tester 등)
  + .claude/skills/*/SKILL.md    ← 재사용 워크플로우 (deploy, review 등)

Level 4 — 프로덕션 (엔터프라이즈)
  + 관리 정책 CLAUDE.md          ← 조직 전체 규칙 (무시 불가)
  + Plugin 디렉토리               ← 팀별 확장 패키지
  + agent-memory/                 ← 에이전트가 세션 간 학습
```

> 상세 필드와 예시는 [Markdown 설정 파일 가이드](references/09-markdown-config-files.md) 참조.

### Claude Cowork — 비개발자용 AI 에이전트

| | Claude Code | Cowork |
|---|-------------|--------|
| 인터페이스 | 터미널 CLI | Claude Desktop GUI |
| 대상 | 개발자 | 지식 노동자 (마케터, 기획자, 분석가 등) |
| 작업 영역 | 코드베이스 | 문서, 스프레드시트, 프레젠테이션 |
| 공통 기반 | Claude Agent SDK | Claude Agent SDK |

**Cowork**는 2026.01에 출시된 Claude Desktop 앱의 에이전트 모드다.
Claude Code와 **동일한 Agent SDK** 위에 구축되었지만, 코드가 아닌 문서/파일 작업에 특화되어 있다.
로컬 폴더에 접근 권한을 주고 자연어로 작업을 지시하면, 격리된 VM에서 자율 실행한다.

> 이 Practice는 개발자 대상 Claude Code에 집중하지만, Agent SDK를 이해하면 Cowork도 자연히 이해할 수 있다.
> 상세 내용은 [Claude Cowork](references/10-claude-cowork.md) 참조.

---

## Practice 카테고리 (자료 기반 재설계)

### 1. Foundation - 핵심 워크플로우 체득

| # | Practice | 핵심 학습 포인트 | 출처 | 난이도 |
|---|----------|-----------------|------|--------|
| 01 | 황금 워크플로우 | Explore→Plan→Implement→Commit 사이클 | 공식, 마스터가이드 | ★☆☆ |
| 02 | 프롬프팅 기법 | 검증 수단 제공, 인터뷰 기법, 구조화된 프롬프트 | 공식, 마스터가이드 | ★☆☆ |
| 03 | 컨텍스트 관리 | /clear, /compact, HANDOFF.md, 세션 관리 | 공식, 마스터가이드 | ★☆☆ |
| 04 | Git 워크플로우 | 커밋, 브랜치, PR 생성, 안전한 Git 습관 | 마스터가이드 | ★☆☆ |

### 2. Configuration - 환경 설정 마스터

| # | Practice | 핵심 학습 포인트 | 출처 | 난이도 |
|---|----------|-----------------|------|--------|
| 05 | CLAUDE.md 작성법 | /init, 포함/제외 기준, 200줄 이하, 모노레포 | 공식, shanraisshan | ★★☆ |
| 06 | Hooks 설정 | 보호 파일 차단, 자동 포맷, 알림, exit code | 마스터가이드 | ★★☆ |
| 07 | MCP 서버 연동 | Context7, Playwright, Chrome DevTools 설정 | shanraisshan, 마스터가이드 | ★★☆ |
| 08 | Skills 만들기 | SKILL.md 작성, 재사용 가능한 워크플로우 정의 | AI Native Camp, shanraisshan | ★★☆ |

### 3. Workflow Patterns - 실무 패턴 습득

| # | Practice | 핵심 학습 포인트 | 출처 | 난이도 |
|---|----------|-----------------|------|--------|
| 09 | TDD 워크플로우 | 테스트 → 구현 → 리팩토링, Ralph Loop | 마스터가이드 | ★★☆ |
| 10 | 버그 디버깅 | 15가지 디버깅 전략, 근본 원인 분석 | 마스터가이드 | ★★☆ |
| 11 | 코드 리뷰 | AI 코드 리뷰 8가지 패턴, 신뢰 레벨 확대 | 마스터가이드 | ★★☆ |
| 12 | 멀티 파일 리팩토링 | 대규모 변경, 의존성 추적, 안전한 리팩토링 | 공식 | ★★★ |

### 4. Advanced - 고급 활용

| # | Practice | 핵심 학습 포인트 | 출처 | 난이도 |
|---|----------|-----------------|------|--------|
| 13 | 서브에이전트 활용 | 컨텍스트 보호, Writer/Reviewer, 병렬 작업 | 공식, 마스터가이드 | ★★★ |
| 14 | Worktree 병렬 개발 | claude --worktree, 독립 브랜치 동시 개발 | 마스터가이드 | ★★★ |
| 15 | Command→Agent→Skill | Orchestration 패턴 설계 및 구현 | shanraisshan | ★★★ |
| 16 | 멀티세션 워크플로우 | 8가지 패턴 (경쟁 프로토타입, TDD Ping-Pong 등) | 마스터가이드 | ★★★ |

### 5. Anti-patterns & Troubleshooting

| # | Practice | 핵심 학습 포인트 | 출처 | 난이도 |
|---|----------|-----------------|------|--------|
| 17 | 7대 실수 체험 | 의도적으로 안티패턴 경험 후 올바른 방법 학습 | 마스터가이드 | ★★☆ |
| 18 | 보안 체크리스트 | 슬롭스쿼팅, OWASP Top 10, 보안 품질 게이트 | 마스터가이드, 공식 | ★★☆ |

### 6. Task Automation - 업무 자동화

| # | Practice | 핵심 학습 포인트 | 출처 | 난이도 |
|---|----------|-----------------|------|--------|
| 19 | Headless Mode 기초 | `claude -p`, 파이프 입력, JSON 출력, 도구 제한 | 공식, 자동화 | ★★☆ |
| 20 | Git Hooks + Claude | pre-commit 보안 검사, 자동 커밋 메시지, post-commit 자동화 | 자동화 | ★★☆ |
| 21 | GitHub Actions 자동화 | claude-code-action으로 PR 자동 리뷰, 이슈 트리아지 | 자동화 | ★★★ |
| 22 | 배치 처리와 Fan-Out | `/batch`, `xargs -P`로 병렬 처리, 결과 집계 | 자동화 | ★★★ |
| 23 | 스케줄링과 Cron | `/loop`, Desktop 예약, GitHub Actions schedule, 야간 자율 작업 | 자동화 | ★★★ |

### 7. Multi-Agent Systems - 멀티 에이전트 시스템 구축

| # | Practice | 핵심 학습 포인트 | 출처 | 난이도 |
|---|----------|-----------------|------|--------|
| 24 | Agent SDK 입문 | Python/TS로 첫 에이전트 구축, query() 호출, 도구 설정 | 멀티에이전트 | ★★★ |
| 25 | 커스텀 서브에이전트 설계 | `.claude/agents/` 정의, 역할별 도구/모델 분리 | 멀티에이전트 | ★★★ |
| 26 | Writer/Reviewer 패턴 | 구현 에이전트 + 리뷰 에이전트 협업 파이프라인 구축 | 멀티에이전트 | ★★★ |
| 27 | Agent Teams 실습 | 팀 생성, 공유 태스크 리스트, 팀원 간 직접 소통 | 멀티에이전트 | ★★★ |
| 28 | Scatter-Gather 연구 시스템 | Lead + 다수 연구 서브에이전트 → 종합 보고서 | 멀티에이전트 | ★★★ |
| 29 | 프로덕션 멀티에이전트 파이프라인 | Command→Agent→Skill 3계층, 역할별 에이전트, Agent Memory | 멀티에이전트, shanraisshan | ★★★ |

### 8. Harness Engineering - 에이전트 제어 체계

| # | Practice | 핵심 학습 포인트 | 출처 | 난이도 |
|---|----------|-----------------|------|--------|
| 30 | 결정론적 가드레일 | Hooks로 파일 보호, 위험 명령 차단, 자동 포맷 강제 | 하네스 | ★★★ |
| 31 | 컨텍스트 엔지니어링 | 프롬프트가 아닌 정보 환경 설계, 최소 고신호 토큰 선별 | 하네스 | ★★★ |
| 32 | 샌드박싱과 권한 제어 | `/sandbox`, 파일시스템/네트워크 격리, 도구 화이트리스트 | 하네스, 공식 | ★★★ |
| 33 | 품질 게이트 파이프라인 | 검증 게이트, 자동 테스트, LLM-as-judge, 출력 밸리데이션 | 하네스 | ★★★ |
| 34 | 에이전트 모니터링과 로깅 | 구조화 로깅, 에러 핸들링, 실시간 모니터링, 장애 복구 | 하네스 | ★★★ |

---

## Practice Session 구축 가이드

### 전체 로드맵 (5단계)

```
Phase 1: Foundation (Practice 01-04)          ← 1~2일
  "Claude Code가 뭔지, 어떻게 대화하는지"
  순수 대화형. 코드 없이도 가능.

Phase 2: Configuration (Practice 05-08)       ← 2~3일
  "나만의 Claude Code 환경 구축"
  CLAUDE.md, Hooks, MCP, Skills 직접 설정.

Phase 3: Workflow Patterns (Practice 09-18)   ← 3~5일
  "실무에서 매일 쓰는 패턴들"
  TDD, 디버깅, 코드 리뷰, 리팩토링 + 안티패턴.

Phase 4: Automation (Practice 19-23)          ← 2~3일
  "반복 작업을 Claude에게 맡기기"
  headless mode, CI/CD, 배치 처리, 스케줄링.

Phase 5: Multi-Agent & Harness (Practice 24-34) ← 5~7일
  "프로덕션급 AI 에이전트 시스템"
  Agent SDK, 멀티에이전트, 거버넌스, 모니터링.
```

### 각 Phase의 Practice 세션 구조

#### Phase 1-3: 대화형 실습 (30분~1시간)

```
1. 개념 소개 (5분)
   - 왜 이것이 중요한지 한 문단으로 설명
   - 이 Practice에서 배울 것 3가지

2. 준비된 환경에서 실습 (15~30분)
   - src/에 미리 준비된 코드가 있음
   - CHALLENGE.md의 단계별 과제를 따라감
   - 예: "이 코드의 버그를 찾아달라고 Claude에게 요청해보세요"

3. 자유 실습 (10~15분)
   - 배운 패턴을 자신의 프로젝트에 적용
   - 변형 과제 시도

4. 체크리스트 자가 점검 (5분)
   - [ ] 핵심 명령어/패턴을 사용해봤는가?
   - [ ] 결과를 검증했는가?
   - [ ] 안티패턴을 인식할 수 있는가?
```

#### Phase 4: 자동화 실습 (1~2시간)

```
1. 시나리오 설명 (10분)
   - 실제 업무 시나리오 제시
   - 예: "매일 PR을 리뷰하는 데 2시간을 쓰고 있다"

2. 수동 → 자동화 변환 (30~45분)
   - 먼저 수동으로 해보기
   - 같은 작업을 claude -p로 자동화
   - 스크립트/Actions로 패키징

3. 통합 테스트 (15~30분)
   - 실제 PR/커밋에서 자동화 동작 확인
   - 엣지 케이스 처리

4. 프로덕션 체크리스트 (10분)
   - [ ] 에러 핸들링이 있는가?
   - [ ] 비용이 통제되는가? (--max-turns)
   - [ ] 시크릿이 안전하게 관리되는가?
```

#### Phase 5: 멀티에이전트 & 하네스 실습 (2~4시간)

```
1. 아키텍처 설계 (30분)
   - 어떤 에이전트가 필요한지 도식화
   - 에이전트 간 소통 방식 결정
   - 도구/권한/모델 배분

2. 에이전트 정의 & 구현 (1~2시간)
   - .claude/agents/, skills/, commands/ 작성
   - 또는 Agent SDK로 프로그래밍
   - 단일 에이전트부터 시작 → 점진적 확장

3. 하네스 구축 (30~60분)
   - Hooks로 가드레일 설정
   - 품질 게이트 추가
   - 로깅/모니터링 설정

4. 통합 실행 & 검증 (30분)
   - 전체 파이프라인 end-to-end 실행
   - 장애 시나리오 시뮬레이션
   - 결과물 품질 평가

5. 회고 (15분)
   - 단일 에이전트 대비 개선점
   - 토큰 비용 분석
   - 개선할 점
```

### Practice 세션 설계 원칙

1. **항상 "왜"부터**: 도구 사용법이 아니라 "이것이 왜 필요한지"부터 시작
2. **준비된 환경**: 설정에 시간 낭비하지 않도록 `src/`에 실습 코드 준비
3. **실패 먼저 경험**: 안티패턴을 먼저 해보고, 왜 안 되는지 이해한 뒤 올바른 방법 학습
4. **점진적 복잡도**: 각 Phase 내에서도 쉬운 것 → 어려운 것 순서
5. **실제 산출물**: 연습이 끝나면 자신의 프로젝트에 바로 쓸 수 있는 것이 남아야 함
6. **자가 검증**: 체크리스트로 스스로 학습 정도를 확인

---

## 설계 결정 (Plan)

### Q1. 각 Practice의 적절한 소요 시간은?

**결정: Phase별 차등 시간**

| Phase | Practice당 시간 | 근거 |
|-------|----------------|------|
| Phase 1: Foundation | **20~30분** | 개념 체득 중심. 코드 없이 대화형으로 가능. 짧게 반복이 효과적. |
| Phase 2: Configuration | **30~45분** | 설정 파일 직접 작성. 시행착오 시간 필요. |
| Phase 3: Workflow | **45~60분** | 실제 코드 위에서 실습. TDD/디버깅은 루프 돌릴 시간 필요. |
| Phase 4: Automation | **60~90분** | 수동→자동 변환 과정 포함. CI/CD는 설정+검증 시간 필요. |
| Phase 5: Multi-Agent & Harness | **90~120분** | 아키텍처 설계+구현+검증. 가장 복잡. 서브 과제로 분할. |

**원칙**: "한 번에 끝내야 한다"는 압박 없이, **중단 가능한 체크포인트**를 과제 안에 배치.
각 Practice의 CHALLENGE.md에 "여기까지 하면 최소 목표 달성" 마커를 둔다.

---

### Q2. 프로그래밍 언어를 하나로 통일할지, 다양하게 할지?

**결정: TypeScript 기본 + Python 보조 (Phase 5)**

| Phase | 언어 | 이유 |
|-------|------|------|
| Phase 1~4 | **TypeScript** | Claude Code 자체가 TS 기반. 웹 생태계 예제 풍부. `uv run`, `pytest`, `ruff` 등 도구 체인 활용 자연스러움. |
| Phase 5 | **TypeScript + Python** | Agent SDK가 양쪽 모두 지원. 실무에서 Python 사용 비중 높음. 둘 다 경험하는 것이 가치 있음. |

**이유**:
- Claude Code의 도구들 (Bash, Read, Edit 등)은 언어 무관하지만, 실습 코드가 있어야 효과적
- 하나로 통일하면 환경 설정 부담 최소화 (`uv`만 있으면 시작, `pyproject.toml`로 의존성 관리)
- Phase 5의 Agent SDK는 Python 예제가 더 풍부하고, 데이터/ML 엔지니어 타겟에 Python이 자연스러움

**사전 요구**: uv, Python 3.10+, Git.

---

### Q3. 초보자도 바로 시작할 수 있도록 사전 준비 가이드가 필요한가?

**결정: YES — `docs/getting-started.md` 별도 작성**

포함할 내용:
```
1. 환경 확인 (3분)
   - uv 설치 확인: uv --version
   - Python 3.10+ 설치 확인: python --version
   - Git 설치 확인: git --version
   - 에디터: VS Code 권장 (Claude Code 확장 지원)

2. Claude Code 설치 (5분)
   - curl -fsSL https://claude.ai/install.sh | bash  (macOS/Linux)
   - irm https://claude.ai/install.ps1 | iex           (Windows)
   - claude --version 으로 확인

3. 인증 설정 (3분)
   - claude 실행 → 로그인 안내 따라가기
   - API 키 또는 Claude 구독 필요

4. 첫 대화 (5분)
   - mkdir practice-test && cd practice-test
   - claude
   - "안녕, 이 디렉토리에 hello.ts 파일을 만들어줘"
   - 동작 확인 후 /clear

5. 이 Practice 레포 클론 (2분)
   - git clone <repo-url>
   - cd ClaudeCodePractice
```

**원칙**: 설치부터 첫 대화까지 **15분 이내**에 완료 가능해야 한다.

---

### Q4. Practice 간 의존 관계를 둘지, 독립적으로 할지?

**결정: Phase 간은 순차, Phase 내는 독립 (하이브리드)**

```
Phase 1 ──→ Phase 2 ──→ Phase 3 ──→ Phase 4 ──→ Phase 5
(순차)      (순차)      (순차)      (순차)      (순차)

Phase 내부:
┌─ Practice 01 (필수 선행)
├─ Practice 02 (독립)
├─ Practice 03 (독립)
└─ Practice 04 (독립)
```

**구체적 의존 관계**:

| Practice | 선행 필수 | 이유 |
|----------|----------|------|
| 01 (황금 워크플로우) | 없음 | 모든 것의 기초 |
| 05 (CLAUDE.md) | 01 완료 | 워크플로우를 알아야 규칙 작성 가능 |
| 09~18 (Workflow) | 05 완료 | CLAUDE.md가 있는 프로젝트에서 실습해야 의미 있음 |
| 19~23 (Automation) | 01, 05 완료 | headless mode는 기본 이해 전제 |
| 24~29 (Multi-Agent) | 05, 08, 13 완료 | Skills와 Subagent 기초 이해 필요 |
| 30~34 (Harness) | 06, 24 완료 | Hooks 기초 + Agent SDK 이해 필요 |

**각 Practice README.md에 명시**:
```markdown
## 사전 요구
- [x] Practice 01 (황금 워크플로우) 완료
- [x] Practice 05 (CLAUDE.md) 완료
```

---

### Q5. AI Native Camp처럼 Skill 기반 커리큘럼으로 만들지?

**결정: 문서 기반 메인 + Skill 보조 (하이브리드)**

**문서 기반을 메인으로 선택한 이유**:
- Skill 기반은 Claude Code가 설치되어 있어야 커리큘럼 자체를 볼 수 있음
- GitHub에서 README를 바로 읽을 수 없어 접근성이 낮음
- 기여자가 PR을 보낼 때 markdown이 더 리뷰하기 쉬움

**Skill을 보조로 활용하는 방법**:
```
practice-01-golden-workflow/
├── README.md           # 메인 커리큘럼 (GitHub에서 바로 읽기)
├── CHALLENGE.md        # 실습 과제
├── src/                # 실습 코드
└── .claude/
    └── skills/
        └── practice-01/
            └── SKILL.md  # "이 Practice를 Claude와 함께 진행하기"
```

**SKILL.md 역할**: `/practice-01` 실행하면 Claude가 튜터 모드로 전환되어 단계별로 안내.
AI Native Camp의 "Skill을 만드는 법을 Skill로 배운다" 접근법을 Phase 2 Practice 08에서 활용.

---

### Q6. 비개발자 트랙을 별도로 둘지?

**결정: NO — 이 레포는 개발자 전용. 비개발자는 Cowork 안내.**

**이유**:
- Claude Cowork가 이미 비개발자 전용 에이전트로 출시됨 (2026.01)
- 비개발자에게 터미널 기반 Claude Code를 가르치는 것은 비효율적
- 하나의 레포에서 두 트랙을 관리하면 복잡도만 증가

**대신**:
- `docs/for-non-developers.md`에 Cowork 안내 + 추천 자료 링크를 한 페이지로 작성
- Practice 01 README.md에 "비개발자라면 → Cowork 추천" 안내 한 줄 추가

**타겟 사용자 명확화**:
> 이 Practice는 **프로그래밍 경험이 있는 개발자**가 Claude Code를 실무에 효과적으로
> 활용하기 위한 실습 과제입니다. 코딩 경험이 없다면 [Claude Cowork](https://claude.com/product/cowork)를 추천합니다.

---

## 각 Practice 폴더 구조 (안)

```
practice-XX-이름/
├── README.md        # 목표, 배경, 학습 포인트
├── CHALLENGE.md     # 실습 과제 (단계별)
├── src/             # 실습용 소스 코드
├── tests/           # 테스트 코드 (필요 시)
└── solution/        # 참고 솔루션 (선택)
```

---

## 추가 콘텐츠 아이디어 (자료에서 발굴)

- **치트시트**: Claude Code 주요 명령어/단축키/패턴 요약
- **안티패턴 모음**: 7대 실수 + 5가지 실패 패턴 상세
- **프롬프트 템플릿 20개**: 마스터 가이드에서 발췌 (복사해서 바로 사용)
- **프로젝트 레시피 12개**: SaaS, CLI, Chrome 확장 등 실전 프로젝트 가이드
- **비용 최적화 가이드**: 10가지 전략
- **비교 실험**: 같은 작업을 프롬프트만 다르게 해서 결과 비교
- **황금 원칙 10가지 포스터**: 한눈에 볼 수 있는 원칙 요약
